// Vercel Serverless Function: принимает заявку с формы сайта и шлёт её в Telegram.
//
// БЕЗОПАСНОСТЬ: токен бота и chat_id НЕ хранятся в коде (репозиторий публичный).
// Их нужно задать в Vercel -> Settings -> Environment Variables:
//   TELEGRAM_BOT_TOKEN  -токен из @BotFather
//   TELEGRAM_CHAT_ID    -куда слать заявки (id группы продаж)
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

    // анти-спам honeypot: скрытое поле, которое заполняют только боты
    if (data._gotcha) return res.status(200).json({ ok: true });

    const TOKEN = process.env.TELEGRAM_BOT_TOKEN;
    const CHAT_ID = process.env.TELEGRAM_CHAT_ID;

    if (!TOKEN || !CHAT_ID) {
      return res.status(500).json({
        ok: false,
        error: 'Не заданы переменные окружения TELEGRAM_BOT_TOKEN и/или TELEGRAM_CHAT_ID в настройках Vercel.',
      });
    }

    // ==== определяем, с какого сайта и страницы пришла заявка ====
    // Главный источник истины: заголовок Referer (полный адрес страницы, откуда отправлена форма).
    // Запасной вариант: поле page из тела запроса (без языка сайта).
    const ref = req.headers['referer'] || req.headers['referrer'] || '';
    let refPath = '';
    try { refPath = new URL(ref).pathname || ''; } catch (e) { refPath = ''; }

    // язык / версия сайта
    let siteLabel;
    if (/^\/en(\/|$)/.test(refPath)) siteLabel = 'Зарубежный (EN)';
    else if (/^\/ru(\/|$)/.test(refPath)) siteLabel = 'Российский (копия /ru)';
    else if (refPath) siteLabel = 'Российский (основной)';
    else siteLabel = 'не определён';

    // ключ страницы: из адреса (убираем язык, слэши и .html), иначе из тела запроса
    let slug = refPath
      .replace(/^\/(en|ru)(?=\/|$)/, '')
      .replace(/^\/+/, '')
      .replace(/\/+$/, '')
      .replace(/\.html$/, '');
    if (!slug) slug = (data.page || 'index');

    const pageNames = {
      'index': 'Главная', 'ai-agents': 'AI-агенты', 'bitrix': 'Bitrix24',
      'vector': 'Vector (AI-продажи)', 'intdoc': 'IntDoc (AI-закупки)',
      'vps': 'Серверы и VPS', 'servers': 'Серверы', 'contacts': 'Контакты',
      'partners': 'Партнёрам', 'news': 'Новости', 'openclaw': 'OpenClaw',
      'company': 'О компании', 'keysy': 'Кейсы Keysy', 'keysy/case': 'Кейс Keysy',
      'calculator-agents': 'Калькулятор AI-агентов', 'calculator-agents-app': 'Калькулятор AI-агентов',
      'calculator': 'Калькулятор', 'privacy': 'Политика конфиденциальности', 'terms': 'Пользовательское соглашение',
    };
    const pageName = pageNames[slug] || slug || 'неизвестна';

    // тип формы (из тела запроса)
    const formNames = {
      client: 'Обсудить проект', servers: 'Заявка на сервер', openclaw: 'OpenClaw',
      partner: 'Стать партнёром', contactpage: 'Контакты', contact: 'Контактная форма',
      bitrix: 'Страница Bitrix', vector: 'Страница Vector', intdoc: 'Страница IntDoc',
    };
    const formLabel = data.form ? (formNames[data.form] || data.form) : '';

    // откуда человек перешёл на форму (например, из кейса Keysy): ?from=... в ссылке
    const origin = data.from || data.origin || '';

    // человекочитаемые подписи полей
    const titles = {
      name: 'Имя', company: 'Компания', role: 'Должность',
      phone: 'Телефон', telegram: 'Telegram', method: 'Способ связи', product: 'Продукт',
      automate: 'Что автоматизировать', comment: 'Комментарий', format: 'Формат',
      busy: 'Чем занимается', relevant: 'Был ли актуален',
    };

    // безопасный вывод и кликабельные ссылки
    const esc = (x) => String(x).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    // ник в Telegram -> кликабельная ссылка t.me (нажал и открылся Telegram)
    const tgLink = (v) => { const u = String(v).trim().replace(/^@+/, '').replace(/[^A-Za-z0-9_]/g, ''); return u ? `<a href="https://t.me/${u}">@${u}</a>` : esc(v); };
    // телефон -> кликабельная ссылка wa.me (нажал и открылся WhatsApp с этим номером)
    const waLink = (v) => { const t = esc(String(v).slice(0, 1000)); const d = String(v).replace(/[^0-9]/g, ''); return d ? `<a href="https://wa.me/${d}">${t}</a>` : t; };

    const lines = ['🟦 <b>Новая заявка с сайта MakeBiz</b>', ''];
    lines.push(`<b>Сайт:</b> ${siteLabel}`);
    lines.push(`<b>Страница:</b> ${esc(pageName)}` + (pageNames[slug] ? ` (${esc(slug)})` : ''));
    if (formLabel) lines.push(`<b>Форма:</b> ${esc(formLabel)}`);
    if (origin) lines.push(`<b>Перешёл с:</b> ${esc(origin)}`);
    lines.push('');

    // ==== источник заявки: реклама, utm-метки, переход извне ====
    // Данные собирает /mb-attr.js на стороне сайта и кладёт в поле attr.
    // first -первое касание (откуда человек узнал о нас),
    // last  -последнее касание перед заявкой (по какой рекламе пришёл).
    const attrLines = (() => {
      const a = data.attr;
      if (!a || typeof a !== 'object') return [];
      const cut = (v, n) => esc(String(v == null ? '' : v).slice(0, n || 200));
      const named = {
        utm_source: 'Источник', utm_medium: 'Канал', utm_campaign: 'Кампания',
        utm_content: 'Объявление', utm_term: 'Ключевое слово',
        gclid: 'Google Ads (gclid)', gbraid: 'Google Ads (gbraid)', wbraid: 'Google Ads (wbraid)',
        yclid: 'Яндекс Директ (yclid)', ymclid: 'Яндекс Маркет (ymclid)',
        fbclid: 'Facebook (fbclid)', ttclid: 'TikTok (ttclid)', msclkid: 'Microsoft Ads (msclkid)',
      };
      const one = (t, label) => {
        if (!t || typeof t !== 'object') return [];
        const out = [];
        for (const [k, ru] of Object.entries(named)) {
          if (t[k]) out.push(`   ${ru}: ${cut(t[k])}`);
        }
        if (t.ref) out.push(`   Переход с: ${cut(t.ref, 300)}`);
        if (t.path) out.push(`   Страница входа: ${cut(t.path, 300)}`);
        if (t.ts) {
          const d = new Date(t.ts);
          if (!isNaN(d)) out.push(`   Когда: ${d.toISOString().slice(0, 16).replace('T', ' ')} UTC`);
        }
        return out.length ? [`<b>${label}:</b>`, ...out] : [];
      };
      const first = one(a.first, 'Первое касание');
      const last = one(a.last, 'Последнее касание');
      if (!first.length && !last.length) return [];
      return ['', ...first, ...last];
    })();

    // остальные поля заявки
    const skip = { _gotcha: 1, form: 1, page: 1, from: 1, origin: 1, attr: 1 };
    for (const [k, v] of Object.entries(data)) {
      if (skip[k] || !v) continue;
      let val;
      if (k === 'telegram') val = tgLink(v);
      else if (k === 'phone') val = waLink(v);
      else val = esc(String(v).slice(0, 1000));
      lines.push(`<b>${titles[k] || k}:</b> ${val}`);
    }
    lines.push(...attrLines);
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
