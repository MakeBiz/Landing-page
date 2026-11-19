// Numbers for the static parts of /local-llm (HTML, JSON-LD, FAQ) from the same engine as the calculator.
// Usage: node figures.mjs en|ru  → JSON to stdout
import fs from 'fs'; import vm from 'vm';
const lang = process.argv[2] === 'ru' ? 'ru' : 'en';
const code = fs.readFileSync(new URL('./engine.js', import.meta.url), 'utf8');
const ctx = { location: { search: '', hash: '' }, console }; vm.createContext(ctx);
vm.runInContext('var LLM_LANG=' + JSON.stringify(lang) + ';' + code + '\n;globalThis.API={rngS,rng,from,mm,rub,calc,payback,DEF,PACKS,EMP,CFG,TASKS,USD_AED,CURR};', ctx);
const { rngS, rng, from, mm, rub, calc, payback, DEF, PACKS, EMP, CFG, TASKS, USD_AED, CURR } = ctx.API;
const fx = CURR === 'AED' ? USD_AED : 1;
const st = o => ({ ...JSON.parse(JSON.stringify(DEF)), ...o, integr: o.integr || [] });
const one = o => {
  const s = st(o), r = calc(s), p = payback(r, s);
  return {
    emp: EMP[s.emp], lo: r.lo, hi: r.hi, loAbs: Math.round(r.lo * CFG.unit), hiAbs: Math.round(r.hi * CFG.unit),
    range: rng(r.lo, r.hi), short: rngS(r.lo, r.hi), from: from(r.lo), title: r.title,
    nodes: r.nodes.map(n => (n.q > 1 ? n.q + '× ' : '') + n.l), tasks: s.tasks.map(k => TASKS[k].t),
    now: rub(p.now), time: rub(p.time), support: rub(r.support), m: p.m || null, mSubs: p.mSubs || null,
    y3: p.y3best > 0 ? rub(p.y3best) : null
  };
};
const out = {
  lang, cur: CURR,
  packs: PACKS.map(p => ({ id: p.id, n: p.n, w: p.w, inc: p.inc, tag: p.tag || '', ...one(p.s) })),
  cases: {
    distr: one({ emp: 4, tasks: ['chat', 'kb', 'docs', 'sales'], mode: '247', integr: ['crm', 'erp'], seats: '40' }),
    cc: one({ emp: 8, tasks: ['chat', 'kb', 'sales', 'calls'], calls: '750', mode: 'nodown', integr: ['crm', 'tel'], seats: '100', api: String(Math.round(1850 * fx / 10) * 10) }),
    prod: one({ emp: 9, tasks: ['chat', 'kb', 'docs', 'code', 'data'], quality: 'high', mode: '247', integr: ['erp'], seats: '150' })
  },
  cfg: {
    install: mm(CFG.install), seat: rub(CFG.seatPrice), rate: rub(CFG.rateDefault), hrs: CFG.hrsDefault,
    support: { self: rub(CFG.support.self), help: rub(CFG.support.help), sla: rub(CFG.support.sla) },
    rent: [Math.round(CFG.rent[0] * 1000) / 10, Math.round(CFG.rent[1] * 1000) / 10], classA: rngS(CFG.eq.A[0], CFG.eq.A[1]), classF: rngS(CFG.eq.F[0], CFG.eq.F[1]),
    priceDate: CFG.priceDate
  }
};
out.min = Math.min(...out.packs.map(p => p.loAbs));
process.stdout.write(JSON.stringify(out));
