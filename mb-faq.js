/* MakeBiz — блок «Частые вопросы». Рисуется из разметки FAQPage на самой странице,
   поэтому текст на экране и текст для поисковиков всегда совпадают. Классы mbq-* изолированы. */
(function () {
  if (window.__mbFaqDone) return; window.__mbFaqDone = 1;

  function findFaq() {
    var s = document.querySelectorAll('script[type="application/ld+json"]');
    for (var i = 0; i < s.length; i++) {
      try {
        var d = JSON.parse(s[i].textContent);
        var g = d['@graph'] || [d];
        for (var j = 0; j < g.length; j++) if (g[j]['@type'] === 'FAQPage') return g[j];
      } catch (e) {}
    }
    return null;
  }

  var faq = findFaq();
  if (!faq || !faq.mainEntity || !faq.mainEntity.length) return;
  var EN = /^\/en(\/|$)/.test(location.pathname);

  var CSS = [
    '#mb-faq{max-width:1240px;margin:0 auto;padding:clamp(34px,4vw,58px) clamp(18px,4vw,40px) 0;'
      + 'font-family:Oxygen,system-ui,-apple-system,Segoe UI,Roboto,sans-serif;position:relative;z-index:1}',
    '#mb-faq *{box-sizing:border-box}',
    '#mb-faq .mbq-head{font:700 12px Oxygen;letter-spacing:.13em;text-transform:uppercase;color:#8FE7AE;'
      + 'background:rgba(22,193,90,.1);border:1px solid rgba(22,193,90,.28);padding:8px 15px;border-radius:100px;display:inline-block}',
    '#mb-faq h2{font:700 clamp(1.5rem,2.7vw,2.15rem)/1.14 Oxygen;letter-spacing:-.02em;color:#fff;margin:22px 0 26px}',
    '#mb-faq .mbq{background:linear-gradient(180deg,#0E1420,#0A0E15);border:1px solid rgba(255,255,255,.1);'
      + 'border-radius:18px;margin:0 0 12px;overflow:hidden}',
    '#mb-faq .mbq[open]{border-color:rgba(22,193,90,.4)}',
    '#mb-faq summary{list-style:none;cursor:pointer;padding:19px 56px 19px 22px;position:relative;'
      + 'font:700 16px/1.4 Oxygen;color:#EAF1FF}',
    '#mb-faq summary::-webkit-details-marker{display:none}',
    '#mb-faq summary:after{content:"";position:absolute;right:24px;top:26px;width:9px;height:9px;'
      + 'border-right:2px solid #16C15A;border-bottom:2px solid #16C15A;transform:rotate(45deg);transition:transform .18s}',
    '#mb-faq .mbq[open] summary:after{transform:rotate(-135deg);top:29px}',
    '#mb-faq .mbq-a{padding:0 22px 20px;font:300 15px/1.65 Oxygen;color:#93A4B8;max-width:88ch}',
    '@media(max-width:560px){#mb-faq summary{font-size:15px;padding:17px 48px 17px 18px}#mb-faq .mbq-a{padding:0 18px 18px;font-size:14px}}'
  ].join('\n');

  function esc(t) {
    return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  function build() {
    if (document.getElementById('mb-faq')) return true;
    var anchor = document.getElementById('mbcf-contact') || document.querySelector('footer');
    if (!anchor || !anchor.parentNode) return false;
    if (!document.getElementById('mb-faq-style')) {
      var st = document.createElement('style'); st.id = 'mb-faq-style'; st.textContent = CSS;
      document.head.appendChild(st);
    }
    var items = '';
    for (var i = 0; i < faq.mainEntity.length; i++) {
      var q = faq.mainEntity[i];
      var a = (q.acceptedAnswer && q.acceptedAnswer.text) || '';
      items += '<details class="mbq"' + (i === 0 ? ' open' : '') + '><summary>' + esc(q.name)
            + '</summary><div class="mbq-a">' + esc(a) + '</div></details>';
    }
    var sec = document.createElement('section');
    sec.id = 'mb-faq';
    sec.innerHTML = '<span class="mbq-head">' + (EN ? 'FAQ' : 'Частые вопросы') + '</span><h2>'
      + (EN ? 'Questions we are asked most often' : 'Что спрашивают чаще всего') + '</h2>' + items;
    anchor.parentNode.insertBefore(sec, anchor);
    return true;
  }

  var tries = 0;
  function attempt() {
    if (build()) return;
    if (tries++ > 60) return;
    setTimeout(attempt, 150);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', attempt);
  else attempt();
  // бандл может перерисовать документ: возвращаем блок на место
  setInterval(function () { if (!document.getElementById('mb-faq')) build(); }, 900);
})();
