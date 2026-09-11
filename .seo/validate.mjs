import { createRequire } from 'node:module'; const require = createRequire(import.meta.url); const { chromium } = require('playwright');
import fs from 'node:fs';
const BASE='http://127.0.0.1:8766';
const sm = fs.readFileSync(process.argv[2],'utf8'); const urls = [...sm.matchAll(/<loc>https:\/\/makebiztechnologies\.com([^<]*)<\/loc>/g)].map(m=>m[1]||'/');
const b = await chromium.launch(); const out=[];
async function run(u, vw, mobile){
  const ctx = await b.newContext({ viewport: vw, isMobile: mobile });
  await ctx.addInitScript(() => { try { localStorage.setItem('mb_consent_v2','declined'); } catch(e){} });
  await ctx.route('**/*', r => { const x=r.request().url(); if(x.startsWith(BASE)||x.startsWith('data:')||x.startsWith('blob:')) return r.continue();
    if(x.startsWith('https://www.googletagmanager.com/')||x.startsWith('https://mc.yandex.ru/')) return r.fulfill({status:200,contentType:'text/javascript',body:''}); return r.abort(); });
  const page = await ctx.newPage(); const errs=[]; page.on('pageerror', e=>errs.push(String(e.message).slice(0,120)));
  const resp = await page.goto(BASE+u,{waitUntil:'load'}); await page.waitForTimeout(3200);
  const r = await page.evaluate(() => {
    const vis = el => el && el.getClientRects().length && getComputedStyle(el).display!=='none' && getComputedStyle(el).visibility!=='hidden';
    const h1 = [...document.querySelectorAll('h1')].filter(vis).map(h=>h.textContent.replace(/\s+/g,' ').trim().slice(0,70));
    return { title: document.title, h1, ssrVisible: !!(vis(document.getElementById('mb-ssr')) || vis(document.getElementById('mb-ssr-nav'))),
      overflow: document.documentElement.scrollWidth - window.innerWidth, textLen: (document.body.innerText||'').length };
  });
  await ctx.close(); return { status: resp.status(), ...r, errs };
}
for (const u of urls) {
  const d = await run(u, {width:1366,height:900}, false);
  const m = await run(u, {width:390,height:800}, true);
  out.push({ u, status:d.status, title:d.title, h1:d.h1, ssrVisible:d.ssrVisible||m.ssrVisible, overflowMobile:m.overflow, text:d.textLen, errs:[...d.errs,...m.errs] });
}
await b.close(); fs.writeFileSync('validate.json', JSON.stringify(out,null,1));
let bad=0; for (const o of out) { const p = o.status!==200 || !o.h1.length || o.ssrVisible || o.overflowMobile>2 || o.errs.length || o.text<400; if(p){bad++; console.log('PROBLEM', JSON.stringify(o).slice(0,400));} }
console.log('checked', out.length, 'problems', bad);
