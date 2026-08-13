// Vercel Serverless Function: публикация / редактирование / удаление постов в Telegram-канале MakeBiz.
//
// БЕЗОПАСНОСТЬ: токен бота, id канала и секрет доступа НЕ хранятся в коде
// (репозиторий публичный). Задать в Vercel -> Settings -> Environment Variables:
//   TELEGRAM_CHANNEL_BOT_TOKEN  - токен бота канала из @BotFather
//   TELEGRAM_CHANNEL_ID         - @makebizchannel или числовой -100...
//   CHANNEL_POST_SECRET         - произвольный секрет, им защищён вызов
// После добавления/изменения переменных сделать Redeploy.
//
// Вызов (GET или POST). Обязателен параметр key = CHANNEL_POST_SECRET.
// Параметр n (любое уникальное значение) не используется логикой, только для обхода кэша.
//
//   Публикация:      ?key=SECRET&text=...&photo=https://...jpg   (photo необязателен)
//   Удаление:        ?key=SECRET&action=delete&message_id=207
//   Редактирование:  ?key=SECRET&action=edit&message_id=207&text=...
//                    (сам определит, текстовый это пост или подпись под фото)

export default async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  try {
    const q = req.query || {};
    const body = typeof req.body === 'string' ? safeJson(req.body) : (req.body || {});

    const TOKEN = process.env.TELEGRAM_CHANNEL_BOT_TOKEN;
    const CHAT_ID = process.env.TELEGRAM_CHANNEL_ID;
    const SECRET = process.env.CHANNEL_POST_SECRET;

    if (!TOKEN || !CHAT_ID || !SECRET) {
      return res.status(500).json({
        ok: false,
        error: 'Не заданы TELEGRAM_CHANNEL_BOT_TOKEN / TELEGRAM_CHANNEL_ID / CHANNEL_POST_SECRET в настройках Vercel.',
      });
    }

    const key = pick(q.key, body.key);
    if (key !== SECRET) {
      return res.status(401).json({ ok: false, error: 'Неверный или отсутствующий key.' });
    }

    const action = String(pick(body.action, q.action) || 'post').toLowerCase();
    const messageId = pick(body.message_id, q.message_id);
    const text = String(pick(body.text, q.text) || '');
    const photo = String(pick(body.photo, q.photo) || '');
    const preview = String(pick(body.preview, q.preview)) === 'true';

    // ---- Удаление ----
    if (action === 'delete') {
      if (!messageId) return res.status(400).json({ ok: false, error: 'Нужен message_id.' });
      const r = await callTg(TOKEN, 'deleteMessage', { chat_id: CHAT_ID, message_id: Number(messageId) });
      return respond(res, r);
    }

    // ---- Редактирование ----
    if (action === 'edit') {
      if (!messageId) return res.status(400).json({ ok: false, error: 'Нужен message_id.' });
      if (!text.trim()) return res.status(400).json({ ok: false, error: 'Пустой text.' });
      // сначала пробуем как у текстового поста, если это фото - редактируем подпись
      let r = await callTg(TOKEN, 'editMessageText', {
        chat_id: CHAT_ID, message_id: Number(messageId), text, disable_web_page_preview: !preview,
      });
      if (!r.ok) {
        r = await callTg(TOKEN, 'editMessageCaption', {
          chat_id: CHAT_ID, message_id: Number(messageId), caption: text,
        });
      }
      return respond(res, r);
    }

    // ---- Публикация (по умолчанию) ----
    if (!text.trim()) return res.status(400).json({ ok: false, error: 'Пустой text.' });
    let r;
    if (photo) {
      // caption у sendPhoto ограничен 1024 символами
      r = await callTg(TOKEN, 'sendPhoto', { chat_id: CHAT_ID, photo, caption: text });
    } else {
      r = await callTg(TOKEN, 'sendMessage', { chat_id: CHAT_ID, text, disable_web_page_preview: !preview });
    }
    return respond(res, r);
  } catch (e) {
    return res.status(500).json({ ok: false, error: String(e) });
  }
}

async function callTg(token, method, payload) {
  const resp = await fetch(`https://api.telegram.org/bot${token}/${method}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  const raw = await resp.text();
  return { ok: resp.ok && parsedOk(raw), raw };
}

function respond(res, r) {
  if (!r.ok) return res.status(502).json({ ok: false, error: r.raw });
  return res.status(200).json({ ok: true, result: safeJson(r.raw) });
}

function parsedOk(raw) {
  try { return JSON.parse(raw).ok === true; } catch (e) { return false; }
}
function pick(a, b) {
  return a != null && a !== '' ? a : b;
}
function safeJson(s) {
  try { return JSON.parse(s); } catch (e) { return s; }
}
