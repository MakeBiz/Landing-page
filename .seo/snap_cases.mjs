import { createRequire } from 'node:module'; const require = createRequire(import.meta.url); const { chromium } = require('playwright');
import fs from 'node:fs';
const BASE='http://127.0.0.1:8766';
const urls = process.argv.slice(3); const OUT = process.argv[2];
const b = await chromium.launch(); const res = {};
for (const u of urls) {
  const ctx = await b.newContext({ viewport:{width:1366,height:900} });
  await ctx.addInitScript(() => { try { localStorage.setItem('mb_consent_v2','declined'); } catch(e){} });
  await ctx.route('**/*', r => { const x=r.request().url(); if(x.startsWith(BASE)||x.startsWith('data:')||x.startsWith('blob:')) return r.continue(); return r.abort(); });
  const page = await ctx.newPage(); const errs=[]; page.on('pageerror', e=>errs.push(String(e.message)));
  await page.goto(BASE+u, {waitUntil:'load'}); await page.waitForTimeout(2500);
  res[u] = await page.evaluate(() => {
    const host = document.querySelector('[data-mb-case],[data-mb-hub]');
    const g = (sel, a) => { const e=document.head.querySelector(sel); return e ? e.getAttribute(a) : null; };
    return {
      kind: host ? (host.hasAttribute('data-mb-case') ? 'case' : 'hub') : null,
      title: document.title, desc: g('meta[name="description"]','content'), ogt: g('meta[property="og:title"]','content'), ogd: g('meta[property="og:description"]','content'),
      canon: g('link[rel="canonical"]','href'),
      ldCase: (document.getElementById('mb-ld-case')||{}).textContent || null, ldCrumb: (document.getElementById('mb-ld-crumb')||{}).textContent || null,
      html: host ? host.innerHTML : null
    };
  });
  res[u].errors = errs; await ctx.close();
}
await b.close(); fs.writeFileSync(OUT, JSON.stringify(res, null, 1)); console.log('ok', Object.keys(res).length);
