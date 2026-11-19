'use strict';
/* =====================================================================
   MakeBiz · Local LLM calculator for makebiztechnologies.com
   Port of MakeBiz/localai src/engine.js (v3, September 2026). Formulas are unchanged.
   What differs from localai:
   - money in CFG is in USD: hardware and services in thousands of USD (CFG.unit = 1e3),
     support, subscription and hour rate in plain USD. Starting values = RUB prices / 81
   - AED = USD x 3.6725, applied once in scaleCFG() for the Russian page
   - texts are in T.en / T.ru, the page sets LLM_LANG before this file
   Prices are edited here and only here
   ===================================================================== */
var LG = (typeof LLM_LANG !== 'undefined' && LLM_LANG) || 'en';
var CURR = LG === 'ru' ? 'AED' : 'USD';
const USD_AED = 3.6725;
const CFG = {
  version: '2026.11-ae1', priceDate: { en: 'November 2026', ru: 'ноябрь 2026' }[LG],
  unit: 1e3,                                                                  // hardware and services: thousands of the currency
  eq: { A: [15, 21], B: [27, 40], C: [40, 59], D: [62, 93], E: [117, 185], F: [161, 247] }, // hardware
  asm: { A: 1.2, B: 1.9, C: 1.9, D: 1.9, E: 1.9, F: 3.1 },                   // assembly and test
  asmSp: { S1: 1.9, S2: 1.9, S4: 3.1 },                                       // assembly of speech servers
  speech: { S1: [27, 40], S2: [42, 59], S4: [68, 99] },
  vram: { A: '1×32 GB', B: '1×32 GB ECC', C: '1×48 GB ECC', D: '1×96 GB ECC', E: '2×96 GB', F: '4×96 GB', S1: '1×32 GB', S2: '2×32 GB', S4: '4×32 GB' },
  install: 3.7,                                                               // base installation and setup
  svc: { chat: 0, kb: 2.5, docs: 2.5, sales: 2.5, bot: 1.9, calls: 3.1, voice: 4.3, media: 3.1, code: 1.9, data: 2.5 }, // services per task
  integr: { crm: 2.5, erp: 3.1, tel: 1.2, mail: 1.2 },
  ha: { infra: [19, 49], svc: 3.1 },                                          // standby server for "no downtime"
  rent: [.035, .05],                                                          // rent a month, share of hardware cost
  support: { self: 620, help: 1480, sla: 3090 },                              // a month, plain currency
  svcSpread: 1.3,                                                             // upper bound of services = lower x 1.3
  seatPrice: 30,                                                              // a month per person for a cloud AI subscription
  hrsDefault: 2,                                                              // hours a week AI saves an active employee (assumption)
  rateDefault: 25                                                             // cost of an employee hour (assumption)
};
function scaleCFG(fx) {
  const k = x => Math.round(x * fx * 10) / 10, a = x => Math.round(x * fx / 10) * 10;
  const pair = o => { for (const i in o) o[i] = o[i].map(k); };
  const one = o => { for (const i in o) o[i] = k(o[i]); };
  pair(CFG.eq); pair(CFG.speech); one(CFG.asm); one(CFG.asmSp); one(CFG.svc); one(CFG.integr);
  CFG.install = k(CFG.install); CFG.ha = { infra: CFG.ha.infra.map(k), svc: k(CFG.ha.svc) };
  for (const i in CFG.support) CFG.support[i] = a(CFG.support[i]);
  CFG.seatPrice = a(CFG.seatPrice); CFG.rateDefault = a(CFG.rateDefault);
}
if (CURR === 'AED') scaleCFG(USD_AED);

/* ---------- texts ---------- */
const T = {
  en: {
    names: { A: 'Workstation for a small team', B: 'Entry-level business server', C: 'General-purpose business server', D: 'Corporate AI server', E: 'Corporate multi-GPU server', F: 'High-load AI cluster' },
    tasks: {
      chat: ['AI chat for staff', 'Emails, texts, ideas, answers to work questions'], kb: ['Knowledge base', 'Answers from company policies and documents'],
      docs: ['Documents and proposals', 'Drafting and checking from templates'], sales: ['Sales and CRM assistant', 'Helps managers, fills in the CRM'],
      bot: ['Customer bot', 'Website and messengers, 24/7'], calls: ['Call analysis', 'Transcripts, summaries, script control'],
      voice: ['Voice robot', 'Makes and answers calls itself'], media: ['Images and video', 'Ad creatives, photo editing, clips'],
      code: ['Developer help', 'Code, tests, documentation'], data: ['Data analytics', 'Questions to CRM, ERP and spreadsheets in plain language']
    },
    opt: {
      mode: [['work', 'Working hours', 'Staff in the office'], ['247', '24×7', 'A maintenance window is fine'], ['nodown', 'No downtime', 'Standby server, no outages']],
      quality: [['std', 'Standard', 'Emails, answers, simple documents'], ['high', 'High', 'Complex documents, analysis, code'], ['max', 'Maximum', 'The most capable models']],
      growth: [['0', 'No growth'], ['.5', '+50% in a year'], ['1', '×2']],
      calls: [['50', 'up to 50k minutes'], ['250', '50-250k'], ['750', '250-750k'], ['1500', 'over 750k']],
      bot: [['100', 'up to 100k messages'], ['500', 'up to 500k'], ['1000', 'up to 1M'], ['5000', 'over 1M']],
      voice: [['10', 'up to 10 lines'], ['40', 'up to 40'], ['100', 'up to 100'], ['300', 'over 100']],
      media: [['low', 'A little, up to 5k a month'], ['mid', 'A lot, up to 50k'], ['high', 'Very much or video']],
      integr: [['crm', 'CRM (Bitrix24, Zoho, HubSpot)'], ['erp', 'ERP and accounting'], ['tel', 'Telephony'], ['mail', 'Email']],
      supply: [['turnkey', 'Turnkey', 'We pick and deliver the hardware'], ['own', 'Own server', 'You already have one, we install'], ['rent', 'Rent', 'No purchase, monthly']],
      support: [['self', 'Self', 'Monitoring on request'], ['help', 'Help', 'Updates and assistance'], ['sla', '24×7 SLA', 'On-call team and SLA']]
    },
    packs: [
      ['Start', 'Team up to 30 people, pilot', ['AI chat and knowledge base', 'Workstation', 'Turnkey installation']],
      ['Business', 'Company of 30-100 people', ['Chat, knowledge base, documents', 'CRM assistant', '24×7'], 'Most popular'],
      ['Corporate', '100-300 people, customer service', ['Everything in Business', 'Customer bot', 'ERP integration']],
      ['Enterprise', '300+ people, no downtime', ['Everything in Corporate', 'Data analytics', 'Standby server, 24×7']]
    ],
    why: {
      emp: (e, l) => e + ' employees → level ' + l, sales: 'Sales or customer bot → +1 level', bot1m: 'Bot up to 1M messages → at least level 4',
      high: 'High quality → +1 level', max: 'Maximum quality → +2 levels', growth: 'Growth ×2 → +1 level',
      calls50: 'Calls up to 50k minutes fit on the main server', mediaLow: 'A small volume of images runs on the main server in a queue'
    },
    indiv: { bot: 'over 1M bot messages', max: 'maximum models', calls: 'over 750k call minutes', voice: 'over 100 voice lines', video: 'video generation' },
    node: { main: 'Main server', calls: 'Server for calls', voice: 'Voice server', media: 'Server for images and video' },
    cluster: n => 'AI cluster of ' + n + ' servers', speechOnly: 'Speech server'
  },
  ru: {
    names: { A: 'Рабочая станция для небольшой команды', B: 'Бизнес-сервер начального уровня', C: 'Универсальный бизнес-сервер', D: 'Корпоративный AI-сервер', E: 'Корпоративный multi-GPU сервер', F: 'Высоконагруженный AI-контур' },
    tasks: {
      chat: ['AI-чат для сотрудников', 'Письма, тексты, идеи, ответы на рабочие вопросы'], kb: ['База знаний', 'Ответы по регламентам и документам компании'],
      docs: ['Документы, договоры, КП', 'Подготовка и проверка по шаблонам'], sales: ['Продажи и CRM', 'Ассистент менеджеров, заполнение CRM'],
      bot: ['Бот для клиентов', 'Сайт и мессенджеры, круглосуточно'], calls: ['Анализ звонков', 'Расшифровка, резюме, контроль скрипта'],
      voice: ['Голосовой робот', 'Сам звонит и отвечает клиентам'], media: ['Картинки и видео', 'Креативы, редактирование фото, ролики'],
      code: ['Помощь разработчикам', 'Код, тесты, документация'], data: ['Аналитика данных', 'Вопросы к CRM, ERP и таблицам обычным языком']
    },
    opt: {
      mode: [['work', 'Рабочее время', 'Для сотрудников в офисе'], ['247', 'Круглосуточно', 'Перерыв на обслуживание допустим'], ['nodown', 'Без остановок', 'Запасной сервер, простой недопустим']],
      quality: [['std', 'Стандартное', 'Письма, ответы, простые документы'], ['high', 'Высокое', 'Сложные документы, анализ, код'], ['max', 'Максимальное', 'Самые мощные модели']],
      growth: [['0', 'Без роста'], ['.5', '+50% за год'], ['1', 'В 2 раза']],
      calls: [['50', 'до 50 тыс. минут'], ['250', '50-250 тыс.'], ['750', '250-750 тыс.'], ['1500', 'больше 750 тыс.']],
      bot: [['100', 'до 100 тыс. сообщений'], ['500', 'до 500 тыс.'], ['1000', 'до 1 млн'], ['5000', 'больше 1 млн']],
      voice: [['10', 'до 10 линий'], ['40', 'до 40'], ['100', 'до 100'], ['300', 'больше 100']],
      media: [['low', 'Немного, до 5 тыс. в месяц'], ['mid', 'Много, до 50 тыс.'], ['high', 'Очень много или видео']],
      integr: [['crm', 'CRM (Битрикс24, Zoho, HubSpot)'], ['erp', 'ERP и учёт'], ['tel', 'Телефония'], ['mail', 'Почта']],
      supply: [['turnkey', 'Под ключ', 'Подберём и поставим'], ['own', 'Свой сервер', 'Уже есть, проверим и установим'], ['rent', 'Аренда', 'Без покупки, помесячно']],
      support: [['self', 'Справимся сами', 'Мониторинг по желанию'], ['help', 'Нужна помощь', 'Обновления и поддержка'], ['sla', '24×7 SLA', 'Дежурство и SLA']]
    },
    packs: [
      ['Старт', 'Команда до 30 человек, пилот', ['AI-чат и база знаний', 'Рабочая станция', 'Установка под ключ']],
      ['Бизнес', 'Компания 30-100 человек', ['Чат, база знаний, документы', 'Ассистент в CRM', 'Круглосуточно'], 'Чаще выбирают'],
      ['Корпорация', '100-300 человек, клиентский сервис', ['Всё из «Бизнес»', 'Бот для клиентов', 'Интеграция с ERP']],
      ['Enterprise', '300+ человек, без простоя', ['Всё из «Корпорации»', 'Аналитика данных', 'Запасной сервер 24×7']]
    ],
    why: {
      emp: (e, l) => e + ' сотрудников → уровень ' + l, sales: 'Продажи или клиентский бот → +1 уровень', bot1m: 'Бот до 1 млн сообщений → минимум уровень 4',
      high: 'Высокое качество → +1 уровень', max: 'Максимальное качество → +2 уровня', growth: 'Рост в 2 раза → +1 уровень',
      calls50: 'Звонки до 50 тыс. минут помещаются на основной сервер', mediaLow: 'Небольшой объём картинок идёт на основной сервер в очереди'
    },
    indiv: { bot: 'больше 1 млн сообщений бота', max: 'максимальные модели', calls: 'больше 750 тыс. минут звонков', voice: 'больше 100 голосовых линий', video: 'генерация видео' },
    node: { main: 'Основной сервер', calls: 'Сервер для звонков', voice: 'Голосовой сервер', media: 'Сервер для картинок и видео' },
    cluster: n => 'AI-контур из ' + n + ' серверов', speechOnly: 'Речевой сервер'
  }
}[LG];
CFG.names = T.names;

const IC0 = { chat: 'chat', kb: 'book', docs: 'doc', sales: 'deal', bot: 'bot', calls: 'phone', voice: 'voice', media: 'image', code: 'code', data: 'chart' };
const TASKS = {};
for (const k in T.tasks) TASKS[k] = { t: T.tasks[k][0], d: T.tasks[k][1], svc: CFG.svc[k], ic: IC0[k] };
const EMP = [5, 10, 20, 30, 50, 75, 100, 150, 200, 300, 500, 750, 1000, 2000, 5000];
const OPT = T.opt;
const PACKS = [
  { id: 'start', s: { emp: 3, tasks: ['chat', 'kb'], mode: 'work' } },
  { id: 'biz', s: { emp: 6, tasks: ['chat', 'kb', 'docs', 'sales'], mode: '247', integr: ['crm'] } },
  { id: 'corp', s: { emp: 9, tasks: ['chat', 'kb', 'docs', 'sales', 'bot'], mode: '247', integr: ['crm', 'erp'] } },
  { id: 'ent', s: { emp: 12, tasks: ['chat', 'kb', 'docs', 'sales', 'bot', 'data'], mode: 'nodown', quality: 'high', integr: ['crm', 'erp'] } }
].map((p, i) => ({ ...p, n: T.packs[i][0], w: T.packs[i][1], inc: T.packs[i][2], tag: T.packs[i][3] }));
const ADDONS = ['calls', 'voice', 'media', 'code', 'data', 'bot'];
const DEF = { emp: 6, tasks: ['chat'], mode: 'work', quality: 'std', growth: '.5', calls: '50', bot: '100', voice: '10', media: 'low', integr: [], supply: 'turnkey', support: 'help', seats: '', price: '', api: '', hrs: '', rate: '' };

/* ===================== ENGINE (formulas as in localai) ===================== */
const LV = ['B', 'C', 'D', 'E', 'F'];
function calc(s) {
  const t = k => s.tasks.includes(k);
  const emp = EMP[s.emp]; const why = []; let indiv = [];
  let i = emp <= 30 ? 0 : emp <= 100 ? 1 : emp <= 300 ? 2 : emp <= 1000 ? 3 : 4; why.push(T.why.emp(emp, i + 1));
  if ((t('bot') || t('sales')) && i < 3) { i++; why.push(T.why.sales); }
  if (t('code') && emp > 100) i = Math.max(i, 3);
  if (t('bot')) { const m = +s.bot; if (m >= 1000) { i = Math.max(i, 3); why.push(T.why.bot1m); } if (m > 1000) { i = Math.max(i, 4); indiv.push(T.indiv.bot); } }
  if (s.quality === 'high') { i = Math.min(4, i + 1); why.push(T.why.high); }
  if (s.quality === 'max') { i = Math.min(4, Math.max(i + 2, 3)); indiv.push(T.indiv.max); why.push(T.why.max); }
  if (s.growth === '1' && i < 4) { i++; why.push(T.why.growth); }
  let main = LV[i];
  if (i === 0 && s.mode === 'work' && !t('bot') && !t('voice')) main = 'A';
  const txt = ['chat', 'kb', 'docs', 'sales', 'bot', 'code', 'data'].some(t); const nodes = txt ? [{ k: main, q: s.mode === 'nodown' ? 2 : 1, l: T.node.main }] : [];
  if (t('calls')) { const m = +s.calls; const sp = m <= 50 ? null : m <= 250 ? 'S1' : m <= 750 ? 'S2' : 'S4'; if (sp) nodes.push({ k: sp, q: 1, l: T.node.calls, sp: 1 }); else why.push(T.why.calls50); if (+s.calls >= 1500) indiv.push(T.indiv.calls); }
  if (t('voice')) { const n = +s.voice * 1.5; const sp = n <= 10 ? 'S1' : n <= 40 ? 'S2' : 'S4'; nodes.push({ k: sp, q: s.mode === 'nodown' ? 2 : 1, l: T.node.voice, sp: 1 }); if (+s.voice > 100) indiv.push(T.indiv.voice); }
  if (t('media')) { let k = s.media === 'low' ? (emp <= 100 && txt ? null : 'B') : s.media === 'mid' ? 'D' : 'E'; if (k) nodes.push({ k, q: !txt && s.mode === 'nodown' ? 2 : 1, l: T.node.media }); else why.push(T.why.mediaLow); if (s.media === 'high') indiv.push(T.indiv.video); }
  if (!nodes.length) nodes.push({ k: main, q: s.mode === 'nodown' ? 2 : 1, l: T.node.main });
  nodes.forEach(n => { if (n.k === 'A' && (nodes.length > 1 || s.mode !== 'work')) n.k = 'B'; });
  // money, in CFG units (thousands)
  let eqLo = 0, eqHi = 0, asm = 0;
  nodes.forEach(n => { const e = n.sp ? CFG.speech[n.k] : CFG.eq[n.k]; eqLo += e[0] * n.q; eqHi += e[1] * n.q; asm += (n.sp ? CFG.asmSp[n.k] : CFG.asm[n.k]) * n.q; });
  const inc = s.supply === 'turnkey';
  let svc = CFG.install + s.tasks.reduce((a, k) => a + TASKS[k].svc, 0) + s.integr.reduce((a, k) => a + CFG.integr[k], 0);
  if (s.mode === 'nodown') svc += CFG.ha.svc;
  const svcR = [svc, svc * CFG.svcSpread];
  const haR = s.mode === 'nodown' ? CFG.ha.infra : [0, 0];
  const lo = (inc ? eqLo + asm : 0) + svcR[0] + haR[0], hi = (inc ? eqHi + asm : 0) + svcR[1] + haR[1];
  const nq = nodes.reduce((a, n) => a + n.q, 0);
  const title = nq > 1 ? T.cluster(nq) : (nodes[0].sp ? T.speechOnly : CFG.names[nodes[0].k] || CFG.names[main]);
  return {
    lo, hi, eq: [eqLo + asm, eqHi + asm], inc, svc: svcR, ha: haR, nodes, title, indiv: [...new Set(indiv)], why, main,
    rent: s.supply === 'rent' ? [eqLo * CFG.unit * CFG.rent[0], eqHi * CFG.unit * CFG.rent[1]] : null, support: CFG.support[s.support]
  };
}

/* ---------- payback (as in localai) ---------- */
function seatsAuto(s) { return Math.max(1, Math.round(EMP[s.emp] * 0.5)); }
function payback(r, s) {
  const seats = +s.seats > 0 ? +s.seats : seatsAuto(s), price = +s.price > 0 ? +s.price : CFG.seatPrice, api = +s.api > 0 ? +s.api : 0;
  const hrs = (s.hrs === '' || s.hrs == null || isNaN(+s.hrs)) ? CFG.hrsDefault : +s.hrs, rate = +s.rate > 0 ? +s.rate : CFG.rateDefault;
  const now = seats * price + api, time = Math.round(seats * hrs * 4.33 * rate);
  const own = r.support + (r.rent ? (r.rent[0] + r.rent[1]) / 2 : 0);
  const res = { seats, price, api, hrs, rate, now, time, own, yearNow: now * 12, yearTime: time * 12 };
  const mm_ = (save) => { if (save <= 0) return null; const a = Math.max(1, Math.round(r.lo * CFG.unit / save)), b = Math.max(1, Math.round(r.hi * CFG.unit / save)); return a > 120 ? null : [a, Math.min(b, 999)]; };
  res.saveSubs = now - own; res.mSubs = mm_(res.saveSubs);
  res.saveAll = now + time - own; res.m = mm_(res.saveAll);
  res.y3 = res.saveAll * 36 - r.hi * CFG.unit; res.y3best = res.saveAll * 36 - r.lo * CFG.unit;
  return res;
}

/* ---------- money format: USD on EN, AED on RU ---------- */
const NB = ' ';
const fN = n => Number(n).toLocaleString(LG === 'ru' ? 'ru-RU' : 'en-US').replace(/\s/g, NB);
const d1 = x => { const v = (Math.round(x * 10) / 10).toString(); return LG === 'ru' ? v.replace('.', ',') : v; };
const r10 = a => a < 1000 ? Math.round(a) : Math.round(a / 10) * 10;
// absolute amount → [number, suffix]
function parts(a) {
  if (LG === 'ru') {
    if (a >= 1e6) return [d1(a / 1e6), 'млн'];
    if (a >= 1e4) return [fN(Math.round(a / 1e3)), 'тыс.'];
    return [fN(r10(a)), ''];
  }
  if (a >= 1e6) return [d1(a / 1e6), 'M'];
  if (a >= 1e4) return [fN(Math.round(a / 1e3)), 'k'];
  return [fN(r10(a)), ''];
}
function money(a) { const [n, s] = parts(a); return LG === 'ru' ? n + (s ? NB + s : '') + NB + 'AED' : '$' + n + s; }
const mm = x => money(x * CFG.unit);                       // CFG units → text
function rngS(lo, hi) {                                    // short range of CFG units: "$45-67k", "165-246 тыс. AED"
  const [a, s1] = parts(lo * CFG.unit), [b, s2] = parts(hi * CFG.unit);
  if (LG === 'ru') return a + (s1 !== s2 && s1 ? NB + s1 : '') + '-' + b + (s2 ? NB + s2 : '') + NB + 'AED';
  return '$' + a + (s1 !== s2 ? s1 : '') + '-' + b + s2;
}
function rng(lo, hi) {                                     // "from $45k to $67k", "от 165 до 246 тыс. AED"
  if (LG !== 'ru') return 'from ' + mm(lo) + ' to ' + mm(hi);
  const [a, s1] = parts(lo * CFG.unit), [b, s2] = parts(hi * CFG.unit);
  return 'от ' + a + (s1 !== s2 && s1 ? NB + s1 : '') + ' до ' + b + (s2 ? NB + s2 : '') + NB + 'AED';
}
const from = lo => (LG === 'ru' ? 'от ' : 'from ') + mm(lo);
function rub(a) {                                          // monthly amounts: exact below 100k ("$1,480", "5 440 AED")
  if (a >= 1e5) return money(a);
  const n = fN(r10(a)); return LG === 'ru' ? n + NB + 'AED' : '$' + n;
}
function rngM(a, b) {                                      // monthly range: "$2,350-4,950", "8 610-18 180 AED"
  if (b >= 1e5) return rub(a) + ' - ' + rub(b);
  const x = fN(r10(a)), y = fN(r10(b)); return LG === 'ru' ? x + '-' + y + NB + 'AED' : '$' + x + '-' + y;
}
