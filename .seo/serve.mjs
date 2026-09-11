// Сервер для локальных проверок: та же маршрутизация, что у timeweb-server.js (ROUTING CORE), без Express
import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path';
const ROOT = process.argv[2]; const PORT = +process.argv[3] || 8766;
const SRC = fs.readFileSync(path.join(ROOT, 'timeweb-server.js'), 'utf8');
const core = SRC.split('// ==== ROUTING CORE ====')[1].split('// ==== /ROUTING CORE ====')[0];
const { indexFiles, createRouter } = new Function('fs','path', core + '; return { indexFiles, createRouter };')(fs, path);
const CT = {'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.css':'text/css','.json':'application/json','.svg':'image/svg+xml','.png':'image/png','.jpg':'image/jpeg','.webp':'image/webp','.ico':'image/x-icon','.xml':'application/xml; charset=utf-8','.txt':'text/plain; charset=utf-8'};
let route = createRouter(indexFiles(ROOT));
http.createServer((req, res) => {
  const u = new URL(req.url, 'http://x');
  if (u.pathname === '/__reindex') { route = createRouter(indexFiles(ROOT)); res.end('ok'); return; }
  const r = route(u.pathname);
  if (r.redirect) { res.writeHead(301, { Location: r.redirect + (u.search || '') }); return res.end(); }
  if (r.file) { res.writeHead(200, { 'content-type': CT[path.extname(r.file)] || 'application/octet-stream' }); return fs.createReadStream(path.join(ROOT, r.file)).pipe(res); }
  res.writeHead(r.status || 404, { 'content-type': CT['.html'] }); res.end(fs.readFileSync(path.join(ROOT, '404.html')));
}).listen(PORT, () => console.log('prod-like server', ROOT, PORT));
