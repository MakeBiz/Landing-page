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
