// Тест логики адресов timeweb-server.js на реальном дереве сайта (без Express).
import fs from 'node:fs';
import path from 'node:path';

const SITE = process.argv[2];                       // клон репозитория
const SRC = fs.readFileSync(new URL('../timeweb-server.js', import.meta.url), 'utf8');
const core = SRC.split('// ==== ROUTING CORE ====')[1].split('// ==== /ROUTING CORE ====')[0];
const { indexFiles, createRouter, isPrivate, cacheControlFor, REDIRECTS } =
  new Function('fs', 'path', core + '; return { indexFiles, createRouter, isPrivate, cacheControlFor, REDIRECTS };')(fs, path);

let fails = 0, checks = 0;
const ok = (cond, msg) => { checks++; if (!cond) { fails++; console.log('  FAIL', msg); } };

function run(label, files) {
  console.log(`\n=== ${label}: публичных файлов ${files.size}`);
  const route = createRouter(files);
  const follow = (u) => { const a = route(u); if (!a.redirect) return { first: a, final: a, hops: 0 };
    const b = route(a.redirect); return { first: a, final: b, hops: b.redirect ? 2 : 1 }; };

  // A. sitemap: каждый адрес отдаётся сразу (200, без редиректа)
  const sm = fs.readFileSync(path.join(SITE, 'sitemap.xml'), 'utf8');
  const locs = [...sm.matchAll(/<loc>https:\/\/makebizte(?:c)?hnologies\.com([^<]*)<\/loc>/g)].map((m) => m[1] || '/');
  for (const u of locs) { const r = route(u); ok(r.file, `sitemap ${u} -> ${JSON.stringify(r)}`); }
  console.log(`  sitemap: ${locs.length} адресов`);

  // B. все внутренние ссылки со всех страниц: 200 или один 301 на живую страницу
  const htmls = [...files].filter((f) => f.endsWith('.html'));
  const hrefs = new Set(), assets = new Set();
  for (const f of htmls) {
    const t = fs.readFileSync(path.join(SITE, f), 'utf8');
    for (const m of t.matchAll(/href=["'](\/[^"'#?\s]*)/g)) hrefs.add(m[1]);
    for (const m of t.matchAll(/(?:src|href)=["'](\/[^"'#?\s]+\.(?:js|css|png|jpe?g|svg|ico|webp|json|xml))/g)) assets.add(m[1]);
  }
  let dead = [];
  for (const u of hrefs) { const r = follow(u); if (!r.final.file || r.hops > 1) dead.push(`${u} -> ${JSON.stringify(r)}`); }
  // ссылки на /ru/* изнутри ru/ допустимо уводить в корень, если ru удалена
  ok(dead.length === 0, `битые или многоходовые ссылки:\n    ${dead.join('\n    ')}`);
  console.log(`  внутренних ссылок: ${hrefs.size}, битых: ${dead.length}`);
  let deadA = [...assets].filter((u) => !route(u).file);
  ok(deadA.length === 0, `битые ассеты: ${deadA.join(', ')}`);
  console.log(`  ассетов в разметке: ${assets.size}, битых: ${deadA.length}`);

  // C. 301 из vercel.json: один ход и живая цель
  for (const [from, to] of Object.entries(REDIRECTS)) {
    const r = follow(from);
    ok(r.first.redirect === to && r.final.file && r.hops === 1, `redirect ${from} -> ${JSON.stringify(r)}`);
  }

  // D. чистые адреса для каждой страницы: /x отдаёт, /x.html и /x/ ведут на /x
  for (const f of htmls) {
    let clean = '/' + f.slice(0, -5);
    if (clean === '/index') clean = '/';
    else if (clean.endsWith('/index')) clean = clean.slice(0, -6);
    const direct = route(clean);
    if (REDIRECTS[clean]) continue;               // адреса под 301 проверены выше
    ok(direct.file === f || (f === 'keysy/case.html') || (f.endsWith('/case.html')), `clean ${clean} -> ${JSON.stringify(direct)} (ждали ${f})`);
    const viaHtml = route('/' + f);
    ok(viaHtml.redirect === clean || (f.endsWith('case.html')), `html ${'/' + f} -> ${JSON.stringify(viaHtml)}`);
    if (clean !== '/') ok(route(clean + '/').redirect === clean, `slash ${clean}/`);
  }

  // E. кейсы по слагу
  const slugs = [...fs.readFileSync(path.join(SITE, 'keysy/cases-data.js'), 'utf8').matchAll(/slug\s*:\s*'([^']+)'/g)].map((m) => m[1]);
  for (const s of slugs) {
    const rf = route('/keysy/' + s).file, ef = route('/en/keysy/' + s).file;
    ok(rf === 'keysy/' + s + '.html' || rf === 'keysy/case.html', `case /keysy/${s} -> ${rf}`);
    ok(ef === 'en/keysy/' + s + '.html' || ef === 'en/keysy/case.html', `case /en/keysy/${s} -> ${ef}`);
  }
  ok(route('/keysy/cases-data.js').file === 'keysy/cases-data.js', 'ассет кейсов');
  ok(route('/keysy/missing.png').status === 404, 'нет картинки -> 404, не страница кейса');

  // F. служебное наружу не отдаётся
  for (const u of ['/timeweb-server.js', '/package.json', '/package-lock.json', '/vercel.json', '/api/lead.js', '/api/post-to-channel.js',
    '/api/lead', '/lead.js', '/node_modules/express/package.json', '/.git/config', '/.publish-status', '/README.md', '/CLAUDE.md',
    '/HANDOFF_%D0%94%D0%9B%D0%AF_%D0%9D%D0%9E%D0%92%D0%9E%D0%93%D0%9E_%D0%A7%D0%90%D0%A2%D0%90.md', '/setup-auto-publish.command',
    '/github-login.command', '/_to_delete/_batch-20260730-230558.tar.gz']) {
    const r = follow(u); ok(!r.final.file, `private ${u} -> ${JSON.stringify(r)}`);
  }
  ok(route('/telegram-posts/pochemu-odin-agent.json').file, 'telegram-posts публичны (их читает post-to-channel)');

  // G. безопасность: никаких редиректов на чужой домен и выходов из корня
  for (const u of ['//evil.com/', '///evil.com', '//evil.com/x.html', '/\\evil.com/', '/..%2f..%2fetc/passwd', '/%2e%2e/%2e%2e/etc/passwd',
    '/news/../package.json', '/%2e%2e%2fpackage.json', '/keysy/..%2f..%2fpackage.json', '/news%00.html']) {
    const r = route(u);
    ok(!(r.redirect && /^\/\/|^\\|^[a-z]+:/i.test(r.redirect)), `open redirect ${u} -> ${JSON.stringify(r)}`);
    ok(!(r.file && isPrivate(r.file)), `traversal ${u} -> ${JSON.stringify(r)}`);
    if (r.file) ok(files.has(r.file), `traversal outside ${u}`);
  }
  ok(route('//evil.com/').redirect === '/evil.com', 'схлопывание //');

  // H. кэш-заголовки
  ok(cacheControlFor('og-image.jpg').includes('max-age=2592000'), 'кэш картинок: месяц');
  ok(cacheControlFor('three.min.js', false).includes('max-age=3600'), 'кэш js без версии: час');
  ok(cacheControlFor('mb-attr.js', true).includes('immutable'), 'кэш js с версией: год и immutable');
  ok(cacheControlFor('index.html').includes('max-age=120'), 'кэш html: две минуты');
  return route;
}

const all = indexFiles(SITE);
const route = run('Как сейчас в репозитории (ru/ на месте)', all);
for (const u of ['/', '/en', '/en/', '/keysy', '/en/keysy', '/news', '/en/news', '/ru', '/ru/keysy', '/bitrix', '/keysy/cdek-b2b', '/company.html', '/index.html', '/en/index.html', '/keysy/case.html'])
  console.log('   ', u.padEnd(18), JSON.stringify(route(u)));

const noRu = new Set([...all].filter((f) => !f.startsWith('ru/')));
const r2 = run('Если папку ru/ удалить', noRu);
for (const u of ['/ru', '/ru/', '/ru/bitrix', '/ru/keysy/cdek-b2b', '/ru/keysy/case', '/ru/news'])
  console.log('   ', u.padEnd(18), JSON.stringify(r2(u)));

console.log(`\nпроверок: ${checks}, провалов: ${fails}`);
process.exit(fails ? 1 : 0);
