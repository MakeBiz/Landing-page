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
/* =====================================================================
   MakeBiz · Local LLM calculator, page UI (port of MakeBiz/localai src/calc.js)
   Needs engine.js before it. Goals: calc_start, calc_result, provider_click, go_<slug>; lead comes from site.js
   ===================================================================== */
(function () {
  const L = document.getElementById('c2Left'), R = document.getElementById('c2Right'), MB = document.getElementById('c2Bar'), MODE = document.getElementById('llmMode');
  if (!L || !R) return;
  const YM = 112503709;
  const U = {
    en: {
      emp: 'How many employees will use AI', empU: 'people', empA: 'Employees', tasks: 'What AI should do', tasksH: 'pick several',
      bot: 'Customer messages a month', calls: 'Call minutes a month', voice: 'Concurrent conversations of the robot', media: 'How many images and video',
      req: 'Requirements', mode: 'When the system must work', quality: 'Answer quality', qualityH: 'harder tasks need a stronger server', growth: 'Load growth in a year',
      integr: 'Connect with', integrH: 'optional', hw: 'Hardware and support', supply: 'Server', support: 'Support',
      payH: 'Payback: what you spend now', payN: 'No subscriptions yet? Leave the fields empty and we count what subscriptions for this team would cost. Hours and hour cost are assumptions, change them to yours',
      seats: 'Paid AI subscriptions', price: 'Subscription, $ a month', api: 'API and bots, $ a month', hrs: 'Time saved, hours a week', rate: 'Employee hour cost, $',
      addTo: 'Add to the package', tune: 'Tune this package →', pack: n => 'Package “' + n + '”', est: 'Estimate, turnkey',
      indiv: 'Needs an individual quote: ', eq: 'Hardware, assembly, test', yours: 'yours', rented: 'rented', svc: 'Installation and task setup', ha: 'Standby server, network and power',
      rentM: 'Server rent a month', perM: ', a month', pb: 'Payback', pbNow: 'Subscriptions and API now', pbTime: 'Staff time AI frees up', pbOwn: 'Support', pbOwnR: 'Support and rent',
      mo: ' a mo', pays: 'Pays back in ', noPay: 'Does not pay back with these assumptions', y3: 'Effect over 3 years: ', y3f: 'from ', y3t: ' to ', y3u: 'up to ',
      subsOnly: 'From subscriptions alone: ', subsNo: 'Subscriptions alone do not pay for the server, the main effect is staff time and data security',
      inst: 'Installation ', quote: 'Get exact quote', fine: d => 'Preliminary range as of ' + d + '. Payback is a scenario and depends on the hours and hour cost assumptions. Delivery and site preparation are quoted separately',
      buy: 'Buy and install', buyS: 'turnkey from MakeBiz', rentT: 'Rent a GPU server', rentS: 'at a partner, we install AI on it',
      barPay: m => 'Pays back in ' + m + ' mo', bar: 'Result ↓',
      months: n => n === 1 ? 'month' : 'months',
      lead: { mode: 'Mode', packs: p => 'package ' + p, custom: 'custom', emp: 'Employees', tasks: 'Tasks', run: 'Works', q: 'quality', g: 'growth', bot: 'Bot', calls: 'Calls', voice: 'Voice', media: 'Media', integr: 'Integrations', none: 'none', srv: 'Server', sup: 'support', range: 'Range', indiv: 'INDIVIDUAL', now: 'AI services now', pb: 'payback', mo: 'mo', comp: 'Configuration', ver: 'Version', intent: { buy: 'Wants: buy and install', rent: 'Wants: RENT a server and install' }, company: 'Company', team: 'Team size', calc: 'Calculation' }
    },
    ru: {
      emp: 'Сколько сотрудников будут пользоваться ИИ', empU: 'человек', empA: 'Сотрудники', tasks: 'Что должен делать ИИ', tasksH: 'можно несколько',
      bot: 'Сколько сообщений от клиентов в месяц', calls: 'Сколько минут звонков в месяц', voice: 'Сколько разговоров робот ведёт одновременно', media: 'Сколько картинок и видео',
      req: 'Требования', mode: 'Когда должна работать система', quality: 'Качество ответов', qualityH: 'чем сложнее задачи, тем мощнее сервер', growth: 'Рост нагрузки за год',
      integr: 'С чем связать', integrH: 'по желанию', hw: 'Оборудование и поддержка', supply: 'Сервер', support: 'Сопровождение',
      payH: 'Окупаемость: сколько тратите сейчас', payN: 'Если подписок пока нет, оставьте поля пустыми: посчитаем, сколько стоили бы подписки на эту команду. Часы и стоимость часа это допущения, поменяйте под себя',
      seats: 'Платных подписок', price: 'Подписка, AED в месяц', api: 'API и боты, AED в месяц', hrs: 'Экономия времени, часов в неделю', rate: 'Стоимость часа сотрудника, AED',
      addTo: 'Добавить к пакету', tune: 'Настроить этот пакет под себя →', pack: n => 'Пакет «' + n + '»', est: 'Ориентировочно под ключ',
      indiv: 'Нужен индивидуальный расчёт: ', eq: 'Оборудование, сборка, тест', yours: 'ваше', rented: 'в аренде', svc: 'Установка и подключение задач', ha: 'Запасной сервер, сеть и питание',
      rentM: 'Аренда сервера в месяц', perM: ', в месяц', pb: 'Окупаемость', pbNow: 'Подписки и API сейчас', pbTime: 'Время сотрудников, которое освободит ИИ', pbOwn: 'Сопровождение', pbOwnR: 'Сопровождение и аренда',
      mo: ' в мес', pays: 'Окупится за ', noPay: 'С такими допущениями не окупается', y3: 'Эффект за 3 года: ', y3f: 'от ', y3t: ' до ', y3u: 'до ',
      subsOnly: 'Только за счёт подписок: ', subsNo: 'Только за счёт подписок сервер не окупится, основной эффект дают время сотрудников и безопасность данных',
      inst: 'Установка ', quote: 'Получить точный расчёт', fine: d => 'Предварительная вилка на ' + d + '. Окупаемость сценарная и зависит от допущений по часам и стоимости часа. Доставка и подготовка площадки считаются отдельно',
      buy: 'Купить и установить', buyS: 'под ключ от MakeBiz', rentT: 'Арендовать GPU-сервер', rentS: 'у партнёра, ИИ установим мы',
      barPay: m => 'Окупится за ' + m + ' мес', bar: 'Итог ↓',
      months: n => { n = Math.abs(n) % 100; const m = n % 10; if (n > 10 && n < 20) return 'месяцев'; if (m > 1 && m < 5) return 'месяца'; if (m === 1) return 'месяц'; return 'месяцев'; },
      lead: { mode: 'Режим', packs: p => 'пакет «' + p + '»', custom: 'индивидуально', emp: 'Сотрудников', tasks: 'Задачи', run: 'Работа', q: 'качество', g: 'рост', bot: 'Бот', calls: 'Звонки', voice: 'Голос', media: 'Медиа', integr: 'Интеграции', none: 'нет', srv: 'Сервер', sup: 'сопровождение', range: 'Вилка', indiv: 'ИНДИВИДУАЛЬНО', now: 'Сейчас на ИИ-сервисы', pb: 'окупаемость', mo: 'мес', comp: 'Состав', ver: 'Версия', intent: { buy: 'Хочет: купить и установить', rent: 'Хочет: АРЕНДА сервера и установка' }, company: 'Компания', team: 'Размер команды', calc: 'Расчёт' }
    }
  }[LG];
  const P = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">';
  const IC = {
    chat: P + '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.4A8 8 0 1 1 21 12z"/></svg>',
    book: P + '<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M4 19V5M9 7h6"/></svg>',
    doc: P + '<path d="M6 2h8l4 4v16H6z"/><path d="M14 2v4h4M9 13h6M9 17h6"/></svg>',
    deal: P + '<path d="M3 7h18v12H3z"/><path d="M8 7V5h8v2M3 12h18"/></svg>',
    bot: P + '<rect x="4" y="7" width="16" height="12" rx="3"/><path d="M12 3v4M9 13h.01M15 13h.01"/></svg>',
    phone: P + '<path d="M5 3h4l2 5-3 2a11 11 0 0 0 6 6l2-3 5 2v4a2 2 0 0 1-2 2A17 17 0 0 1 3 5a2 2 0 0 1 2-2z"/></svg>',
    voice: P + '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/></svg>',
    image: P + '<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="10" r="2"/><path d="M21 16l-5-5-8 9"/></svg>',
    code: P + '<path d="M8 8l-4 4 4 4M16 8l4 4-4 4M13 5l-2 14"/></svg>',
    chart: P + '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M7 15l3-3 2 2 5-5"/></svg>'
  };
  const EXPERT = /expert=1/.test(location.search + location.hash);
  let S = { view: 'custom', ...JSON.parse(JSON.stringify(DEF)) }, PK = { i: 1, add: [] };
  const esc = x => String(x).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  /* ---------- goals ---------- */
  function goal(n, p) {
    try { if (window.ym) window.ym(YM, 'reachGoal', n, p); } catch (e) {}
    try { if (window.gtag) window.gtag('event', n, p || {}); } catch (e) {}
    try { if (window.__px && window.__px.event) window.__px.event(n, p); } catch (e) {}
  }
  let started = false, resulted = false;
  function touched() { if (!started) { started = true; goal('calc_start'); } }
  function result() { if (started && !resulted) { resulted = true; goal('calc_result'); } }

  /* ---------- form controls ---------- */
  function chips(key, opts, multi) {
    const cur = S[key];
    return '<div class="llm-chips">' + opts.map(o => { const on = multi ? cur.includes(o[0]) : cur === o[0]; return '<button type="button" class="llm-chip' + (on ? ' on' : '') + '" aria-pressed="' + on + '" data-k="' + key + '" data-v="' + o[0] + '"' + (multi ? ' data-multi="1"' : '') + '>' + o[1] + (o[2] ? '<small>' + o[2] + '</small>' : '') + '</button>'; }).join('') + '</div>';
  }
  const row = (label, body, hint) => '<div class="llm-row"><div class="llm-lab">' + label + (hint ? '<span>' + hint + '</span>' : '') + '</div>' + body + '</div>';
  const empTxt = i => i === EMP.length - 1 ? fN(5000) + '+' : fN(EMP[i]);
  function payInputs() {
    const st = cur();
    const inp = (k, lab, ph, step) => '<label>' + lab + '<input type="number" inputmode="decimal" min="0"' + (step ? ' step="' + step + '"' : '') + ' data-pay="' + k + '" value="' + esc(S[k] || '') + '" placeholder="' + ph + '"></label>';
    return '<div class="llm-sep">' + U.payH + '</div><p class="llm-note">' + U.payN + '</p><div class="llm-pay">' +
      inp('seats', U.seats, seatsAuto(st)) + inp('price', U.price, CFG.seatPrice) + inp('api', U.api, 0) + inp('hrs', U.hrs, CFG.hrsDefault, '0.5') + inp('rate', U.rate, CFG.rateDefault) + '</div>';
  }
  function renderCustom() {
    let h = row(U.emp, '<div class="llm-emp"><b>' + empTxt(S.emp) + '</b> ' + U.empU + '</div><input type="range" min="0" max="' + (EMP.length - 1) + '" value="' + S.emp + '" id="c2Emp" aria-label="' + U.empA + '"><div class="llm-rl"><span>5</span><span>100</span><span>' + fN(1000) + '</span><span>' + fN(5000) + '+</span></div>');
    h += row(U.tasks, '<div class="llm-tasks">' + Object.entries(TASKS).map(([k, x]) => '<button type="button" class="llm-task' + (S.tasks.includes(k) ? ' on' : '') + '" aria-pressed="' + S.tasks.includes(k) + '" data-task="' + k + '"><span class="llm-ti">' + IC[x.ic] + '</span><span><b>' + x.t + '</b><small>' + x.d + '</small></span></button>').join('') + '</div>', U.tasksH);
    const sub = [];
    if (S.tasks.includes('bot')) sub.push(row(U.bot, chips('bot', OPT.bot)));
    if (S.tasks.includes('calls')) sub.push(row(U.calls, chips('calls', OPT.calls)));
    if (S.tasks.includes('voice')) sub.push(row(U.voice, chips('voice', OPT.voice)));
    if (S.tasks.includes('media')) sub.push(row(U.media, chips('media', OPT.media)));
    if (sub.length) h += '<div class="llm-sub">' + sub.join('') + '</div>';
    h += '<div class="llm-sep">' + U.req + '</div>';
    h += row(U.mode, chips('mode', OPT.mode));
    h += row(U.quality, chips('quality', OPT.quality), U.qualityH);
    h += row(U.growth, chips('growth', OPT.growth));
    h += row(U.integr, chips('integr', OPT.integr, true), U.integrH);
    h += '<div class="llm-sep">' + U.hw + '</div>';
    h += row(U.supply, chips('supply', OPT.supply));
    h += row(U.support, chips('support', OPT.support));
    h += payInputs();
    L.innerHTML = h;
    L.querySelector('#c2Emp').oninput = ev => { touched(); S.emp = +ev.target.value; L.querySelector('.llm-emp b').textContent = empTxt(S.emp); const ph = L.querySelector('[data-pay="seats"]'); if (ph) ph.placeholder = seatsAuto(S); renderRight(); save(); };
  }
  function packState() { const p = PACKS[PK.i]; return { ...JSON.parse(JSON.stringify(DEF)), ...JSON.parse(JSON.stringify(p.s)), integr: [...(p.s.integr || [])], tasks: [...new Set([...p.s.tasks, ...PK.add])], seats: S.seats, price: S.price, api: S.api, hrs: S.hrs, rate: S.rate }; }
  function cur() { return S.view === 'packs' ? packState() : S; }
  function renderPacks() {
    const P0 = PACKS[PK.i], st = packState();
    let h = '<div class="llm-packs">' + PACKS.map((p, i) => { const r = calc({ ...DEF, ...p.s, integr: p.s.integr || [] }); return '<button type="button" class="llm-pk' + (i === PK.i ? ' on' : '') + '" aria-pressed="' + (i === PK.i) + '" data-pk="' + i + '">' + (p.tag ? '<span class="llm-tag">' + p.tag + '</span>' : '') + '<b>' + p.n + '</b><small>' + p.w + '</small><span class="llm-pr">' + from(r.lo) + '</span><ul>' + p.inc.map(x => '<li>' + x + '</li>').join('') + '</ul></button>'; }).join('') + '</div>';
    const adds = ADDONS.filter(k => !P0.s.tasks.includes(k));
    if (adds.length) h += '<div class="llm-lab" style="margin-top:22px">' + U.addTo + '</div><div class="llm-adds">' + adds.map(k => { const on = PK.add.includes(k); const w = on ? st.tasks : [...st.tasks, k], wo = st.tasks.filter(x => x !== k); const d = calc({ ...st, tasks: w }).lo - calc({ ...st, tasks: wo }).lo; return '<button type="button" class="llm-add' + (on ? ' on' : '') + '" aria-pressed="' + on + '" data-add="' + k + '"><span>' + (on ? '✓ ' : '+ ') + TASKS[k].t + '</span><i>+' + mm(Math.max(d, CFG.install / 6)) + '</i></button>'; }).join('') + '</div>';
    h += payInputs();
    h += '<button type="button" class="btn btn-ghost llm-tune" data-tune="1">' + U.tune + '</button>';
    L.innerHTML = h;
  }
  function mTxt(m) { return (m[0] === m[1] ? m[0] : m[0] + '-' + m[1]) + ' ' + U.months(m[1]); }
  function renderRight() {
    const s = cur(), r = calc(s), pb = payback(r, s);
    const sup = OPT.support.find(o => o[0] === s.support)[1];
    let h = '<div class="llm-res-l">' + (S.view === 'packs' ? U.pack(PACKS[PK.i].n) : U.est) + '</div>';
    h += '<div class="llm-res-p">' + (r.indiv.length ? from(r.lo) : rng(r.lo, r.hi)) + '</div><div class="llm-res-c">' + r.title + '</div>';
    if (r.indiv.length) h += '<div class="llm-indiv">' + U.indiv + r.indiv.join(', ') + '</div>';
    h += '<table class="llm-t">';
    h += '<tr><td>' + U.eq + '</td><td>' + (r.inc ? rngS(r.eq[0], r.eq[1]) : s.supply === 'own' ? U.yours : U.rented) + '</td></tr>';
    h += '<tr><td>' + U.svc + '</td><td>' + rngS(r.svc[0], r.svc[1]) + '</td></tr>';
    if (r.ha[1]) h += '<tr><td>' + U.ha + '</td><td>' + rngS(r.ha[0], r.ha[1]) + '</td></tr>';
    if (r.rent) h += '<tr><td>' + U.rentM + '</td><td>' + rngM(r.rent[0], r.rent[1]) + '</td></tr>';
    h += '<tr class="mo"><td>' + sup + U.perM + '</td><td>' + rub(r.support) + '</td></tr></table>';
    h += '<div class="llm-pb"><div class="llm-pb-h">' + U.pb + '</div>';
    h += '<div class="llm-pb-r"><span>' + U.pbNow + '</span><b>' + rub(pb.now) + U.mo + '</b></div>';
    h += '<div class="llm-pb-r"><span>' + U.pbTime + '</span><b>' + rub(pb.time) + U.mo + '</b></div>';
    h += '<div class="llm-pb-r"><span>' + (r.rent ? U.pbOwnR : U.pbOwn) + '</span><b>−' + rub(pb.own) + U.mo + '</b></div>';
    if (pb.m) { h += '<div class="llm-pb-big">' + U.pays + mTxt(pb.m) + '</div>'; if (pb.y3best > 0) h += '<div class="llm-pb-s">' + U.y3 + (pb.y3 > 0 ? U.y3f + rub(pb.y3) + U.y3t : U.y3u) + rub(pb.y3best) + '</div>'; }
    else h += '<div class="llm-pb-big sm">' + U.noPay + '</div>';
    h += '<div class="llm-pb-s">' + (pb.mSubs ? U.subsOnly + mTxt(pb.mSubs) : U.subsNo) + '</div></div>';
    h += '<div class="llm-nodes">' + r.nodes.map(n => '<span>' + (n.q > 1 ? n.q + '× ' : '') + n.l + (EXPERT ? ' · ' + CFG.vram[n.k] : '') + '</span>').join('') + '<span>' + U.inst + mm(CFG.install) + '</span></div>';
    h += '<button type="button" class="btn btn-wide" data-lead="buy">' + U.quote + '</button>';
    h += '<div class="llm-br"><a href="#form" data-lead="buy"><b>' + U.buy + '</b><span>' + U.buyS + '</span></a><a href="#rent" data-rent="1"><b>' + U.rentT + '</b><span>' + U.rentS + '</span></a></div>';
    h += '<p class="llm-fine">' + U.fine(CFG.priceDate) + '</p>';
    if (EXPERT) h += '<pre class="llm-xp">' + r.why.join('\n') + '\n' + r.nodes.map(n => n.q + '× ' + n.k + ' ' + CFG.vram[n.k]).join('\n') + '</pre>';
    R.innerHTML = h;
    if (MB) MB.innerHTML = '<div><small>' + (pb.m ? U.barPay(pb.m[0] === pb.m[1] ? pb.m[0] : pb.m[0] + '-' + pb.m[1]) : U.est) + '</small><b>' + (r.indiv.length ? from(r.lo) : rngS(r.lo, r.hi)) + '</b></div><button type="button" class="btn btn-sm" data-goto="1">' + U.bar + '</button>';
  }
  function save() { try { localStorage.setItem('mb_llm_ae', JSON.stringify({ S, PK })); } catch (e) {} }
  function render() {
    MODE.querySelectorAll('button').forEach(b => { const on = b.dataset.mode === S.view; b.classList.toggle('on', on); b.setAttribute('aria-selected', on); });
    S.view === 'packs' ? renderPacks() : renderCustom(); renderRight(); save();
  }
  MODE.addEventListener('click', e => { const b = e.target.closest('[data-mode]'); if (!b) return; touched(); S.view = b.dataset.mode; render(); });
  L.addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b) return; touched();
    if (b.dataset.task) { const k = b.dataset.task; S.tasks = S.tasks.includes(k) ? (S.tasks.length > 1 ? S.tasks.filter(x => x !== k) : S.tasks) : [...S.tasks, k]; return render(); }
    if (b.dataset.k) { const k = b.dataset.k, v = b.dataset.v; if (b.dataset.multi) S[k] = S[k].includes(v) ? S[k].filter(x => x !== v) : [...S[k], v]; else S[k] = v; return render(); }
    if (b.dataset.pk) { PK = { i: +b.dataset.pk, add: [] }; return render(); }
    if (b.dataset.add) { const k = b.dataset.add; PK.add = PK.add.includes(k) ? PK.add.filter(x => x !== k) : [...PK.add, k]; return render(); }
    if (b.dataset.tune) { S = { ...packState(), view: 'custom' }; return render(); }
  });
  L.addEventListener('input', e => { const el = e.target; if (el.dataset.pay) { touched(); S[el.dataset.pay] = el.value; renderRight(); save(); } });

  /* ---------- lead: calculation into the form ---------- */
  const T2 = U.lead;
  function summary() {
    const s = cur(), r = calc(s), pb = payback(r, s);
    const opt = (k, v) => ((OPT[k] || []).find(o => o[0] === v) || [, v])[1];
    return [
      T2.mode + ': ' + (S.view === 'packs' ? T2.packs(PACKS[PK.i].n) : T2.custom),
      T2.emp + ': ' + EMP[s.emp], T2.tasks + ': ' + s.tasks.map(k => TASKS[k].t).join('; '),
      T2.run + ': ' + opt('mode', s.mode) + ', ' + T2.q + ': ' + opt('quality', s.quality) + ', ' + T2.g + ': ' + opt('growth', s.growth),
      s.tasks.includes('bot') ? T2.bot + ': ' + opt('bot', s.bot) : '', s.tasks.includes('calls') ? T2.calls + ': ' + opt('calls', s.calls) : '',
      s.tasks.includes('voice') ? T2.voice + ': ' + opt('voice', s.voice) : '', s.tasks.includes('media') ? T2.media + ': ' + opt('media', s.media) : '',
      T2.integr + ': ' + (s.integr.map(k => opt('integr', k)).join(', ') || T2.none), T2.srv + ': ' + opt('supply', s.supply) + ', ' + T2.sup + ': ' + opt('support', s.support),
      T2.range + ': ' + rng(r.lo, r.hi) + (r.indiv.length ? ' (' + T2.indiv + ': ' + r.indiv.join(', ') + ')' : ''),
      T2.now + ': ' + rub(pb.now) + '/' + T2.mo + (pb.m ? ', ' + T2.pb + ' ' + pb.m[0] + '-' + pb.m[1] + ' ' + T2.mo : ''),
      T2.comp + ': ' + r.nodes.map(n => n.q + '× ' + n.k + ' ' + CFG.vram[n.k]).join(', '), T2.ver + ': ' + CFG.version
    ].filter(Boolean).join('\n').replace(/ /g, ' ');
  }
  const F = document.querySelector('form.lead-form[data-page$="local-llm"]');
  function goLead(intent) {
    if (!F) return;
    F.elements.intent.value = intent; F.elements.calc.value = summary();
    const box = F.querySelector('.llm-calc-note'); if (box) { box.hidden = false; box.querySelector('b').textContent = T2.intent[intent]; }
    F.scrollIntoView({ behavior: 'smooth', block: 'center' });
    setTimeout(() => { const n = F.elements.name; n && n.focus({ preventScroll: true }); }, 500);
  }
  document.addEventListener('click', e => {
    const a = e.target.closest('[data-lead]'); if (a) { e.preventDefault(); result(); goLead(a.dataset.lead); return; }
    if (e.target.closest('[data-rent]')) { result(); }
    if (e.target.closest('[data-goto]')) R.scrollIntoView({ behavior: 'smooth', block: 'start' });
    const p = e.target.closest('a[data-provider]');
    if (p) { const sl = p.dataset.provider; goal('provider_click', { provider: sl, campaign: 'local-llm', partner: 1, page: location.pathname }); goal('go_' + sl); }
  });
  // before site.js sends the form: company, team size, intent and calculation go into the comment
  document.addEventListener('submit', e => {
    if (e.target !== F) return;
    const el = F.elements, mark = '\n\n---\n';
    if (!el.calc.value) el.calc.value = summary();
    const cv = el.comment.value, own = (cv.indexOf(mark) >= 0 ? cv.split(mark)[0] : cv.indexOf(T2.calc + ':') >= 0 ? '' : cv).trim();
    const extra = [el.company.value.trim() ? T2.company + ': ' + el.company.value.trim() : '', el.team.value.trim() ? T2.team + ': ' + el.team.value.trim() : '',
      T2.intent[el.intent.value] || '', T2.calc + ':\n' + el.calc.value].filter(Boolean).join('\n');
    el.comment.value = own ? own + mark + extra : extra;
  }, true);

  /* ---------- result visible after interaction = calc_result ---------- */
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(en => { en.forEach(x => { if (x.isIntersecting && started) setTimeout(result, 1200); }); }, { threshold: .4 }).observe(R);
  }
  /* ---------- sticky mobile bar ---------- */
  if (MB && 'IntersectionObserver' in window) {
    const v = { c: false, r: false, f: false }, upd = () => MB.classList.toggle('show', v.c && !v.r && !v.f && innerWidth <= 900);
    new IntersectionObserver(en => { en.forEach(x => { v.c = x.isIntersecting; }); upd(); }, { threshold: [0, .05] }).observe(document.getElementById('calc'));
    const io2 = new IntersectionObserver(en => { en.forEach(x => { v[x.target === R ? 'r' : 'f'] = x.isIntersecting; }); upd(); }, { rootMargin: '0px 0px -35% 0px' }); io2.observe(R); if (F) io2.observe(F);
  }

  /* ---------- start: restore, link parameters (?packs, ?pack=, ?emp=, ?tasks=) ---------- */
  try { const sv = JSON.parse(localStorage.getItem('mb_llm_ae') || 'null'); if (sv && sv.S && Array.isArray(sv.S.tasks) && sv.S.tasks.every(k => TASKS[k]) && sv.S.integr.every(k => CFG.integr[k] != null)) { S = { ...S, ...sv.S }; PK = sv.PK || PK; } } catch (e) {}
  (function () {
    const q = new URLSearchParams(location.search);
    if (q.has('packs')) S.view = 'packs';
    if (q.get('pack')) { const i = PACKS.findIndex(p => p.id === q.get('pack')); if (i >= 0) { S.view = 'packs'; PK = { i, add: [] }; } }
    if (q.get('emp')) { S.emp = Math.max(0, Math.min(EMP.length - 1, +q.get('emp'))); S.view = 'custom'; }
    if (q.get('tasks')) { const t = q.get('tasks').split(',').filter(k => TASKS[k]); if (t.length) { S.tasks = t; S.view = 'custom'; } }
  })();
  document.getElementById('calc').classList.add('llm-js');
  render();
})();
