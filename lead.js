// Vercel Serverless Function: принимает заявку с формы и шлёт в Telegram.
// Токен и chat_id хранятся в Environment Variables проекта Vercel — в коде сайта НЕ видны.
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

    // ТОКЕН вписан прямо в код для быстрого старта.
    // ⚠️ РЕКОМЕНДУЕТСЯ перевыпустить токен в @BotFather (/revoke) и вставить новый сюда,
    // т.к. этот токен уже был отправлен в переписке. Заменить — просто в кавычках ниже.
    // Ещё безопаснее: убрать строку и задать переменную окружения TELEGRAM_BOT_TOKEN в Vercel.
    const TOKEN = process.env.TELEGRAM_BOT_TOKEN || '8658216999:AAEHPvwuFw4RDEDYT18kHvjRu58OszbVk0E';

    // CHAT_ID группы MakeBiz (не секретно). Можно переопределить переменной окружения.
    const CHAT_ID = process.env.TELEGRAM_CHAT_ID || '-5262045407';

    if (!TOKEN) return res.status(500).json({ ok: false, error: 'No TELEGRAM_BOT_TOKEN' });

    const titles = {
      form: 'Тип заявки', name: 'Имя', company: 'Компания', role: 'Должность',
      phone: 'Телефон', telegram: 'Telegram', product: 'Продукт',
      automate: 'Что автоматизировать', comment: 'Комментарий', format: 'Формат',
      busy: 'Чем занимается', relevant: 'Был ли актуален',
    };
    const formNames = {
      client: 'Обсудить проект', partner: 'Стать партнёром', contactpage: 'Контакты',
    };
    const lines = ['🟦 <b>Новая заявка с сайта MakeBiz</b>', ''];
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
