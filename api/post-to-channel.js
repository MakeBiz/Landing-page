// Vercel Serverless Function: публикация / редактирование / удаление постов в Telegram-канале MakeBiz.
//
// БЕЗОПАСНОСТЬ: токен бота, id канала и секрет доступа НЕ хранятся в коде
// (репозиторий публичный). Задать в Vercel -> Settings -> Environment Variables:
//   TELEGRAM_CHANNEL_BOT_TOKEN  - токен бота канала из @BotFather
//   TELEGRAM_CHANNEL_ID         - @makebizchannel или числовой -100...
//   CHANNEL_POST_SECRET         - произвольный секрет, им защищён вызов
// После изменения переменных сделать Redeploy.
//
// Ответ всегда text/plain (короткая строка), чтобы результат было видно даже
// через простой GET. Обязателен параметр key = CHANNEL_POST_SECRET.
// Параметр n (любое уникальное значение) не используется логикой, только обход кэша.
//
// Публикация из файла (основной способ, короткий URL):
//   ?key=SECRET&post=<slug>
//   где файл telegram-posts/<slug>.json = { "text": "...", "photo": "https://...jpg" }
// Публикация напрямую (короткий текст):
//   ?key=SECRET&text=...&photo=https://...jpg
// Удаление:      ?key=SECRET&action=delete&message_id=207
// Редактирование: ?key=SECRET&action=edit&message_id=207&post=<slug>   (или &text=...)

export default async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  const reply = (code, msg) => {
    res.setHeader('Content-Type', 'text/plain; charset=utf-8');
    return res.status(code).send(msg);
  };

  try {
    const q = req.query || {};
    const body = typeof req.body === 'string' ? safeJson(req.body) : (req.body || {});

    const TOKEN = process.env.TELEGRAM_CHANNEL_BOT_TOKEN;
    const CHAT_ID = process.env.TELEGRAM_CHANNEL_ID;
    const SECRET = process.env.CHANNEL_POST_SECRET;
    if (!TOKEN || !CHAT_ID || !SECRET) {
      return reply(500, 'ERR: не заданы env-переменные TELEGRAM_CHANNEL_BOT_TOKEN / TELEGRAM_CHANNEL_ID / CHANNEL_POST_SECRET');
    }

    const key = pick(q.key, body.key);
    if (key !== SECRET) return reply(401, 'ERR: неверный или отсутствующий key');

    const action = String(pick(body.action, q.action) || 'post').toLowerCase();
    const messageId = pick(body.message_id, q.message_id);
    const slug = String(pick(body.post, q.post) || '');
    const preview = String(pick(body.preview, q.preview)) === 'true';

    // текст и картинку берём либо из файла telegram-posts/<slug>.json, либо из параметров
    let text = String(pick(body.text, q.text) || '');
    let photo = String(pick(body.photo, q.photo) || '');
    if (slug) {
      const proto = (req.headers['x-forwarded-proto'] || 'https').split(',')[0];
      const host = req.headers.host;
      const fr = await fetch(`${proto}://${host}/telegram-posts/${encodeURIComponent(slug)}.json`, { cache: 'no-store' });
      if (!fr.ok) return reply(404, `ERR: файл telegram-posts/${slug}.json не найден (${fr.status})`);
      const data = await fr.json().catch(() => null);
      if (!data) return reply(400, `ERR: telegram-posts/${slug}.json не парсится как JSON`);
      if (data.text != null) text = String(data.text);
      if (data.photo != null && !photo) photo = String(data.photo);
    }

    // ---- Удаление ----
    if (action === 'delete') {
      if (!messageId) return reply(400, 'ERR: нужен message_id');
      const r = await callTg(TOKEN, 'deleteMessage', { chat_id: CHAT_ID, message_id: Number(messageId) });
      return r.ok ? reply(200, `OK: удалено message_id=${messageId}`) : reply(502, `ERR: ${r.desc}`);
    }

    // ---- Редактирование ----
    if (action === 'edit') {
      if (!messageId) return reply(400, 'ERR: нужен message_id');
      if (!text.trim()) return reply(400, 'ERR: пустой text');
      let r = await callTg(TOKEN, 'editMessageText', {
        chat_id: CHAT_ID, message_id: Number(messageId), text, disable_web_page_preview: !preview,
      });
      if (!r.ok) {
        r = await callTg(TOKEN, 'editMessageCaption', { chat_id: CHAT_ID, message_id: Number(messageId), caption: text });
      }
      return r.ok ? reply(200, `OK: отредактировано message_id=${messageId}`) : reply(502, `ERR: ${r.desc}`);
    }

    // ---- Публикация ----
    if (!text.trim()) return reply(400, 'ERR: пустой text');
    let r;
    if (photo) r = await callTg(TOKEN, 'sendPhoto', { chat_id: CHAT_ID, photo, caption: text });
    else r = await callTg(TOKEN, 'sendMessage', { chat_id: CHAT_ID, text, disable_web_page_preview: !preview });
    if (!r.ok) return reply(502, `ERR: ${r.desc}`);
    return reply(200, `OK: опубликовано message_id=${r.messageId}`);
  } catch (e) {
    return reply(500, `ERR: ${String(e)}`);
  }
}

async function callTg(token, method, payload) {
  const resp = await fetch(`https://api.telegram.org/bot${token}/${method}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  const raw = await resp.text();
  let json = null;
  try { json = JSON.parse(raw); } catch (e) {}
  const ok = resp.ok && json && json.ok === true;
  let messageId = null;
  if (ok && json.result && typeof json.result === 'object') messageId = json.result.message_id || null;
  const desc = json && json.description ? json.description : raw;
  return { ok, messageId, desc, raw };
}

function pick(a, b) {
  return a != null && a !== '' ? a : b;
}
function safeJson(s) {
  try { return JSON.parse(s); } catch (e) { return s; }
}
