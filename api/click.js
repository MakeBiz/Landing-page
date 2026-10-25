// Клик по телефону или мессенджеру на makebiztechnologies.com: пересылаем на makebiz.life/api/click,
// там источник клика уходит в Telegram-чат заявок (как у makebiz.life). Ответ браузеру сразу.
export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ ok: false });
  res.status(200).json({ ok: true });
  try {
    const data = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {});
    const ctl = new AbortController(); const timer = setTimeout(() => ctl.abort(), 8000);
    await fetch('https://makebiz.life/api/click', {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, signal: ctl.signal,
      body: JSON.stringify({ type: data.type, attr: data.attr, _site: 'uae',
        _ref: String(req.headers.referer || req.headers.referrer || ''), _ua: String(req.headers['user-agent'] || '') }),
    }).catch(() => {});
    clearTimeout(timer);
  } catch (e) { /* клик не критичен */ }
}
