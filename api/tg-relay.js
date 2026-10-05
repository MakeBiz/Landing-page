// Ретранслятор уведомлений в Telegram для сайта makebiz.life.
// Зачем: сервер makebiz.life стоит в московском дата-центре, оттуда api.telegram.org
// недоступен (таймаут), и заявки с сайта не доходили до Telegram. Этот сервер стоит
// во Франкфурте, Telegram отсюда доступен, поэтому makebiz.life шлёт уведомление через него.
// Секретов в коде нет: токен бота приходит в запросе по HTTPS, не пишется в лог и не хранится.
// Умеет только sendMessage, ничего другого через него вызвать нельзя.
const TOKEN_RE = /^\d{6,12}:[A-Za-z0-9_-]{30,60}$/;

export default async function handler(req, res) {
  if (req.method === 'GET') {
    // состояние переменных этого приложения (только да/нет), для диагностики формы дубайского сайта
    return res.status(200).json({ ok: true, env: { telegramToken: !!process.env.TELEGRAM_BOT_TOKEN, telegramChat: !!process.env.TELEGRAM_CHAT_ID } });
  }
  if (req.method !== 'POST') return res.status(405).json({ ok: false, error: 'Method Not Allowed' });
  try {
    const d = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {});
    const token = String(d.token || ''), chat = String(d.chat_id || ''), text = String(d.text || '');
    if (!TOKEN_RE.test(token) || !/^-?\d{5,20}$|^@[A-Za-z0-9_]{4,40}$/.test(chat) || !text || text.length > 4096) {
      return res.status(200).json({ ok: false, error: 'bad request' });
    }
    const ctl = new AbortController();
    const timer = setTimeout(() => ctl.abort(), 8000);
    let r;
    try {
      r = await fetch('https://api.telegram.org/bot' + token + '/sendMessage', {
        method: 'POST', headers: { 'Content-Type': 'application/json' }, signal: ctl.signal,
        body: JSON.stringify({ chat_id: chat, text, parse_mode: d.parse_mode === 'HTML' ? 'HTML' : undefined, disable_web_page_preview: true }),
      });
    } finally { clearTimeout(timer); }
    const j = await r.json().catch(() => ({}));
    return res.status(200).json({ ok: !!j.ok, status: r.status, error: j.ok ? undefined : String(j.description || '').slice(0, 200) });
  } catch (e) {
    return res.status(200).json({ ok: false, error: 'relay: ' + String(e && e.name === 'AbortError' ? 'timeout' : (e && e.message) || e).slice(0, 120) });
  }
}
