// Vercel Serverless Function: принимает заявку с формы и шлёт в Telegram.
//
// БЕЗОПАСНОСТЬ: токен бота и chat_id НЕ хранятся в коде.
// Их нужно задать в настройках проекта Vercel:
//   Settings -> Environment Variables ->
//     TELEGRAM_BOT_TOKEN = <токен от @BotFather>
//     TELEGRAM_CHAT_ID   = <id вашей группы, например -100xxxxxxxxxx>
// После добавления переменных нужно сделать Redeploy.

export default async function handler(req, res) {
  // CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST') return res.status(405).json({ ok: false, error: 'Method Not Allowed' });

  try {
    const data = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {});

    // анти-спам honeypot
    if (data._gotcha) return res.status(200).json({ ok: true });

    const TOKEN = process.env.TELEGRAM_BOT_TOKEN;
    const CHAT_ID = process.env.TELEGRAM_CHAT_ID;

    if (!TOKEN || !CHAT_ID) {
      return res.status(500).json({
        ok: false,
        error: 'Не заданы переменные окружения TELEGRAM_BOT_TOKEN и/или TELEGRAM_CHAT_ID в настройках Vercel',
      });
    }

    const titles = {
      form: 'Тип заявки', name: 'Имя', company: 'Компания', role: 'Должность',
      phone: 'Телефон', telegram: 'Telegram', product: 'Продукт',
      automate: 'Что автоматизировать', comment: 'Комментарий', format: 'Формат',
      busy: 'Чем занимается', relevant: 'Был ли актуален',
    };
    const formNames = {
      client: 'Обсудить проект', partner: 'Стать партнёром', contactpage: 'Контакты',
    };
    const lines = ['\u{1F7E6} <b>Новая заявка с сайта MakeBiz</b>', ''];
    if (data.form) lines.push(`<b>Форма:</b> ${formNames[data.form] || data.form}`);
    for (const [k, v] of Object.entries(data)) {
      if (k === '_gotcha' || k === 'form' || !v) continue;
      lines.push(`<b>${titles[k] || k}:</b> ${String(v).slice(0, 1000)}`);
    }
    const text = lines.join('\n');

    const tgResp = await fetch(`https://api.telegram.org/bot${TOKEN}/sendMessage`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ chat_id: CHAT_ID, text, parse_mode: 'HTML', disable_web_page_preview: true }),
    });
    if (!tgResp.ok) {
      const t = await tgResp.text();
      return res.status(502).json({ ok: false, error: t });
    }
    return res.status(200).json({ ok: true });
  } catch (e) {
    return res.status(500).json({ ok: false, error: String(e) });
  }
}
