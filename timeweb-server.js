// MakeBiz: сервер сайта makebiztechnologies.com для Timeweb App Platform.
//
// На Vercel чистые адреса, редиректы и кейсы делал vercel.json, а формы работали
// как функции api/*.js. Timeweb этого не умеет, поэтому здесь Express-сервер,
// который повторяет поведение Vercel:
//   1. cleanUrls и trailingSlash:false: /bitrix отдаёт bitrix.html, а /bitrix.html
//      и /bitrix/ уводят 301 на /bitrix. Папка отдаёт свой index.html (/en),
//      файл важнее одноимённой папки (/keysy это keysy.html, /news это news.html);
//   2. все 301 из vercel.json и шаблон кейса для /keysy/<slug>;
//   3. заголовки безопасности и кэша из vercel.json плюс сжатие (Vercel сжимал сам);
//   4. каждый файл api/<имя>.js работает по адресу /api/<имя>, как на Vercel
//      (сейчас это lead и post-to-channel). Сами эти файлы не меняются.
//
// Файл назван не server.js нарочно: пока домен ещё смотрит на Vercel, тот принял бы
// server.js за Express-приложение и перестал бы раздавать статику живого сайта.
// Запуск на Timeweb: npm start. Переменные окружения описаны в конце файла.

import express from 'express';
import compression from 'compression';
import fs from 'node:fs';
import os from 'node:os';
import crypto from 'node:crypto';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const PORT = Number(process.env.PORT) || 3000;

// Основной адрес сайта. Зеркала и www уводим на него 301 (если их привяжут к приложению).
const CANONICAL_HOST = 'makebiztechnologies.com';
const ALIAS_HOSTS = new Set([
  'www.makebiztechnologies.com',
  'makebiztehnologies.com',       // старый адрес с опечаткой: 301 на основной, путь сохраняется
  'www.makebiztehnologies.com',
]);

// ==== ROUTING CORE ====
// Чистая логика адресов без Express: её же гоняет тест по реальному дереву сайта.

// 301 из vercel.json, один в один
const REDIRECTS = {
  '/openclaw': '/ai-agents',
  '/servers': '/vps',
  '/en/openclaw': '/en/ai-agents',
  '/en/servers': '/en/vps',
  '/keysy/pink-rabbit-agent': '/keysy',
  '/en/keysy/pink-rabbit-agent': '/en/keysy',
  '/ru/keysy/pink-rabbit-agent': '/keysy',
  '/keysy/case': '/keysy',
  '/en/keysy/case': '/en/keysy',
  '/ru/keysy/case': '/keysy',
  '/calculator': '/calculator-agents',   // старая страница «Калькулятор экономики проекта» удалена
};

// rewrites из vercel.json: /keysy/<slug>, /en/keysy/<slug>, /ru/keysy/<slug> отдают шаблон case.html.
// Слаг без точки: отсутствующая картинка или скрипт получает 404, а не страницу кейса.
const CASE_RE = /^\/((?:en\/|ru\/)?keysy)\/([^/.]+)$/;

// Служебное наружу не отдаём: сервер, зависимости, исходники функций, заметки и скрипты для Мака.
// telegram-posts/*.json остаются публичными: их читает api/post-to-channel.js.
function isPrivate(rel) {
  return /(^|\/)\./.test(rel) ||
    /^(node_modules|api|_to_delete)(\/|$)/.test(rel) ||
    /^(timeweb-server\.js|package\.json|package-lock\.json|vercel\.json|lead\.js)$/.test(rel) ||
    /\.(command|md)$/i.test(rel);
}

// Список публичных файлов собирается один раз при старте: сайт между деплоями не меняется.
function indexFiles(root) {
  const out = new Set();
  (function walk(dir, prefix) {
    for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
      if (e.name === 'node_modules' || e.name.startsWith('.')) continue;
      const rel = prefix + e.name;
      if (e.isDirectory()) walk(path.join(dir, e.name), rel + '/');
      else if (e.isFile() && !isPrivate(rel)) out.add(rel);
    }
  })(root, '');
  return out;
}

// route(путь из запроса, как есть) -> { redirect } | { file } | { status }
function createRouter(files) {
  const ruKept = [...files].some((f) => f.startsWith('ru/'));
  return function route(rawPath) {
    if (rawPath.includes('\\') || rawPath.includes('\0')) return { status: 400 };

    // канонический адрес: повторные слэши, хвостовой слэш, .html и /index убираем,
    // /ru/* уводим в корень, если папку ru/ удалили, затем явные 301
    let c = rawPath.replace(/\/{2,}/g, '/');
    if (c.length > 1) c = c.replace(/\/+$/, '') || '/';
    if (c.endsWith('.html')) c = c.slice(0, -5) || '/';
    if (c === '/index') c = '/';
    else if (c.endsWith('/index')) c = c.slice(0, -6) || '/';
    if (!ruKept && (c === '/ru' || c.startsWith('/ru/'))) c = c.slice(3) || '/';
    if (REDIRECTS[c]) c = REDIRECTS[c];
    if (c !== rawPath) return { redirect: c };

    let d;
    try { d = decodeURIComponent(rawPath); } catch (e) { return { status: 400 }; }
    if (d.includes('\0') || /(^|\/)\.\.?(\/|$)/.test(d)) return { status: 400 };

    const rel = d === '/' ? 'index.html' : d.slice(1);
    if (files.has(rel)) return { file: rel };
    if (files.has(rel + '.html')) return { file: rel + '.html' };
    if (files.has(rel + '/index.html')) return { file: rel + '/index.html' };
    const m = CASE_RE.exec(d);
    if (m && files.has(m[1] + '/case.html')) return { file: m[1] + '/case.html' };
    return { status: 404 };
  };
}

// Cache-Control как в vercel.json; остальное как по умолчанию у Vercel
function cacheControlFor(rel, versioned) {
  // Картинки и шрифты меняются редко: месяц в кэше, неделя на фоновое обновление.
  if (/\.(png|jpe?g|gif|webp|avif|svg|ico|woff2?|ttf|otf)$/i.test(rel)) return 'public, max-age=2592000, stale-while-revalidate=604800';
  // Скрипты и стили с версией в адресе (?v=хэш) неизменны: год и immutable.
  // Без версии держим час, иначе правка общего файла неделю не доходит до людей.
  if (/\.(css|js)$/i.test(rel)) {
    return versioned ? 'public, max-age=31536000, immutable' : 'public, max-age=3600, stale-while-revalidate=86400';
  }
  // HTML меняется при каждом деплое: две минуты в кэше плюс фоновое обновление,
  // чтобы переходы по сайту и кнопка «назад» не перекачивали страницу заново.
  return 'public, max-age=120, stale-while-revalidate=600';
}
// ==== /ROUTING CORE ====

const files = indexFiles(ROOT);
const route = createRouter(files);

const app = express();
app.disable('x-powered-by');
app.use(compression());

// заголовки безопасности, на все ответы
app.use((req, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  // Во фрейме сайт могут показывать только он сам и Яндекс Метрика (Вебвизор, карты кликов и скроллинга).
  // Раньше здесь стоял X-Frame-Options: SAMEORIGIN, он не пускал Метрику; frame-ancestors его заменяет.
  res.setHeader('Content-Security-Policy', "frame-ancestors 'self' https://metrika.yandex.ru https://metrika.yandex.by "
    + "https://metrika.yandex.kz https://metrica.yandex.com https://metrica.yandex.com.tr https://webvisor.com https://*.webvisor.com");
  res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');
  res.setHeader('Strict-Transport-Security', 'max-age=31536000');
  res.setHeader('Permissions-Policy', 'camera=(), microphone=(), geolocation=(), payment=(), usb=()');
  next();
});

// www и зеркала -> основной домен
app.use((req, res, next) => {
  const host = String(req.headers.host || '').toLowerCase().replace(/:\d+$/, '');
  if (ALIAS_HOSTS.has(host)) return res.redirect(301, 'https://' + CANONICAL_HOST + req.originalUrl);
  next();
});

// функции api/*.js, как на Vercel: /api/<имя>, любые методы, тело разобрано в req.body
const parseBody = [
  express.json({ limit: '1mb' }),
  express.urlencoded({ extended: false, limit: '1mb' }),
  express.text({ type: 'text/*', limit: '1mb' }),
];
const apiDir = path.join(ROOT, 'api');
const apiNames = [];
for (const f of fs.existsSync(apiDir) ? fs.readdirSync(apiDir).sort() : []) {
  if (!f.endsWith('.js')) continue;
  const handler = (await import(pathToFileURL(path.join(apiDir, f)).href)).default;
  if (typeof handler !== 'function') continue;
  const name = f.slice(0, -3);
  apiNames.push(name);
  app.all('/api/' + name, parseBody, (req, res, next) => {
    Promise.resolve().then(() => handler(req, res)).catch(next);
  });
}

function sendPage(res, rel, status, next, versioned) {
  res.status(status);
  res.setHeader('Cache-Control', status === 200 ? cacheControlFor(rel, versioned) : 'no-store');
  res.sendFile(rel, { root: ROOT }, (err) => {
    if (err && !res.headersSent) next(err);
  });
}

// страницы, файлы, редиректы
app.use((req, res, next) => {
  if (req.method !== 'GET' && req.method !== 'HEAD') return next();
  const r = route(req.path);
  if (r.redirect) {
    const q = req.originalUrl.indexOf('?');
    return res.redirect(301, r.redirect + (q === -1 ? '' : req.originalUrl.slice(q)));
  }
  if (r.file) return sendPage(res, r.file, 200, next, Object.prototype.hasOwnProperty.call(req.query || {}, 'v'));
  if (r.status === 404 && files.has('404.html')) return sendPage(res, '404.html', 404, next);
  res.status(r.status || 404).type('text/plain').send(r.status === 400 ? 'Bad request' : 'Not found');
});

// остальные методы на страницы сайта
app.use((req, res) => {
  res.status(405).set('Allow', 'GET, HEAD').type('text/plain').send('Method Not Allowed');
});

// ошибки: без стектрейсов наружу
app.use((err, req, res, next) => {
  const status = err.status || err.statusCode || 500;
  if (status >= 500) console.error('[server]', req.method, req.originalUrl, err);
  if (res.headersSent) return;
  if (req.path.startsWith('/api/')) return res.status(status).json({ ok: false, error: status >= 500 ? 'server error' : 'bad request' });
  res.status(status).type('text/plain').send(status >= 500 ? 'Server error' : 'Bad request');
});

// ==== IndexNow: сообщаем Bing и Яндексу об обновлении страниц ====
// Подтверждение владения это файл-ключ в корне сайта, отдельная верификация не нужна.
// Пингуем один раз на деплой: отпечаток считаем от sitemap.xml и запоминаем во временной папке.
async function pingIndexNow() {
  try {
    if (process.env.INDEXNOW === 'off') return;
    const keyFile = [...files].find((f) => /^[a-f0-9]{16,64}\.txt$/.test(f));
    if (!keyFile) return;
    const key = fs.readFileSync(path.join(ROOT, keyFile), 'utf8').trim();
    const sm = fs.readFileSync(path.join(ROOT, 'sitemap.xml'), 'utf8');
    const urlList = [...sm.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]);
    if (!urlList.length) return;
    const stamp = crypto.createHash('sha1').update(sm).digest('hex').slice(0, 12);
    const mark = path.join(os.tmpdir(), 'makebiz-indexnow-' + stamp);
    if (fs.existsSync(mark)) return;
    fs.writeFileSync(mark, '1');
    const host = new URL(urlList[0]).host;
    const r = await fetch('https://api.indexnow.org/indexnow', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json; charset=utf-8' },
      body: JSON.stringify({ host, key, keyLocation: 'https://' + host + '/' + keyFile, urlList }),
    });
    console.log('[indexnow]', r.status, urlList.length, 'адресов');
  } catch (e) {
    console.log('[indexnow] пропущено:', e && e.message);
  }
}

app.listen(PORT, () => {
  console.log(`MakeBiz: порт ${PORT}, файлов ${files.size}, функции: ${apiNames.map((n) => '/api/' + n).join(', ') || 'нет'}`);
  setTimeout(pingIndexNow, 4000);
});

// Переменные окружения (Timeweb, настройки приложения). Значения те же, что были в Vercel:
//   TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID             форма заявок (api/lead.js)
//   TELEGRAM_CHANNEL_BOT_TOKEN, TELEGRAM_CHANNEL_ID,
//   CHANNEL_POST_SECRET                              посты в Telegram-канал (api/post-to-channel.js)
