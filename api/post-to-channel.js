// Vercel Serverless Function: публикует готовый пост в Telegram-канал MakeBiz.
//
// БЕЗОПАСНОСТЬ: токен бота, id канала и секрет доступа НЕ хранятся в коде
// (репозиторий публичный). Задать в Vercel -> Settings -> Environment Variables:
//   TELEGRAM_CHANNEL_BOT_TOKEN  - токен бота канала из @BotFather
//   TELEGRAM_CHANNEL_ID         - @makebizchannel или числовой -100...
//   CHANNEL_POST_SECRET         - произвольный секрет, им защищён вызов
// После добавления переменных сделать Redeploy.
//
// Вызов (GET или POST). Обязателен параметр key = CHANNEL_POST_SECRET.
//   GET  /api/post-to-channel?key=SECRET&text=...&photo=https://...jpg&n=UNIQUE
//   POST /api/post-to-channel?key=SECRET   body: { "text": "...", "photo": "https://...jpg" }
// Если photo задан - шлётся картинкой с подписью (sendPhoto), иначе текстом (sendMessage).
// Параметр n (любое уникальное значение) не используется логикой, он только для обхода кэша.

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

    const text = String(pick(body.text, q.text) || '');
    const photo = String(pick(body.photo, q.photo) || '');
    // предпросмотр ссылки: по умолчанию выключен, включается preview=true
    const preview = String(pick(body.preview, q.preview)) === 'true';

    if (!text.trim()) {
      return res.status(400).json({ ok: false, error: 'Пустой text.' });
    }

    let apiUrl, payload;
    if (photo) {
      // caption у sendPhoto ограничен 1024 символами
      apiUrl = `https://api.telegram.org/bot${TOKEN}/sendPhoto`;
      payload = { chat_id: CHAT_ID, photo, caption: text };
    } else {
      apiUrl = `https://api.telegram.org/bot${TOKEN}/sendMessage`;
      payload = { chat_id: CHAT_ID, text, disable_web_page_preview: !preview };
    }

    const tgResp = await fetch(apiUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const raw = await tgResp.text();
    if (!tgResp.ok) {
      return res.status(502).json({ ok: false, error: raw });
    }
    return res.status(200).json({ ok: true, result: safeJson(raw) });
  } catch (e) {
    return res.status(500).json({ ok: false, error: String(e) });
  }
}

function pick(a, b) {
  return a != null && a !== '' ? a : b;
}
function safeJson(s) {
  try { return JSON.parse(s); } catch (e) { return s; }
}
