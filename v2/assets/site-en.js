(function () {
  var hdr = document.querySelector('.hdr');
  function onScroll() { if (hdr) hdr.classList.toggle('is-scrolled', window.scrollY > 8); }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  // бургер
  var burger = document.querySelector('.burger'), mnav = document.querySelector('.mnav');
  if (burger && mnav) burger.addEventListener('click', function () {
    var open = mnav.hidden; mnav.hidden = !open; burger.setAttribute('aria-expanded', String(open));
  });
  if (mnav) mnav.addEventListener('click', function (e) { if (e.target.closest('a')) { mnav.hidden = true; burger.setAttribute('aria-expanded', 'false'); } });

  // выпадающие меню по клику (тач)
  document.querySelectorAll('.nav-dd > .nav-link').forEach(function (b) {
    b.addEventListener('click', function (e) {
      var dd = b.parentNode, was = dd.classList.contains('open');
      document.querySelectorAll('.nav-dd.open').forEach(function (x) { x.classList.remove('open'); });
      if (!was) dd.classList.add('open');
      b.setAttribute('aria-expanded', String(!was)); e.stopPropagation();
    });
  });
  document.addEventListener('click', function () { document.querySelectorAll('.nav-dd.open').forEach(function (x) { x.classList.remove('open'); }); });

  // атрибуция: как mb-attr.js старого сайта (тот же ключ mb_attr, 90 дней, первое и последнее касание, ClientID Метрики)
  var KEY = 'mb_attr', TTL = 90 * 864e5,
      MARKS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'gclid', 'gbraid', 'wbraid', 'yclid', 'ymclid', 'fbclid', 'ttclid', 'msclkid'];
  function cut(v, n) { return String(v == null ? '' : v).slice(0, n || 200); }
  function box() { try { localStorage.setItem('__mb_t', '1'); localStorage.removeItem('__mb_t'); return localStorage; } catch (e) { try { return sessionStorage; } catch (e2) { return null; } } }
  function load() { var b = box(); if (!b) return null; try { var d = JSON.parse(b.getItem(KEY) || 'null'); if (!d || !d.first || !d.first.ts) return null; if (Date.now() - d.first.ts > TTL) { b.removeItem(KEY); return null; } return d; } catch (e) { return null; } }
  function save(d) { var b = box(); if (b) try { b.setItem(KEY, JSON.stringify(d)); } catch (e) {} }
  function touch() {
    var t = { ts: Date.now(), path: cut(location.pathname + location.search, 300) };
    try { var r = document.referrer; if (r && new URL(r).hostname !== location.hostname) t.ref = cut(r, 300); } catch (e) {}
    try { var q = new URLSearchParams(location.search); MARKS.forEach(function (k) { var v = q.get(k); if (v) t[k] = cut(v); }); } catch (e) {}
    return t;
  }
  (function record() {
    var d = load(), t = touch(), hasMark = MARKS.some(function (k) { return !!t[k]; });
    if (!d) return save({ first: t, last: t });
    if (hasMark || t.ref) { d.last = t; save(d); }
  })();
  if (!window.__mbAttr) window.__mbAttr = function () {
    var d = load() || {}, s = { url: cut(location.href, 500) };
    if (d.first) s.first = d.first;
    if (d.last && d.first && d.last.ts !== d.first.ts) s.last = d.last;
    try { var m = document.cookie.match(/(?:^|;\s*)_ym_uid=(\d+)/); if (m) s.cid = m[1]; } catch (e) {}
    return s;
  };

  function goal(name) { try { if (window.ym) window.ym(112503709, 'reachGoal', name); } catch (e) {} try { if (window.gtag) window.gtag('event', name); } catch (e) {} }
  // клики по телефону и мессенджерам: цель в Метрике + источник менеджерам в Telegram (/api/click, не чаще раза в 30 минут)
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a'); if (!a) return;
    var h = a.getAttribute('href') || '', g = '';
    if (/^tel:/i.test(h)) g = 'call';
    else if (/t\.me\/makebizchannel/i.test(h)) g = 'tg_channel';
    else if (/t\.me\//i.test(h)) g = 'telegram';
    else if (/max\.ru\//i.test(h)) g = 'max';
    else if (/wa\.me\//i.test(h)) g = 'whatsapp';
    else if (/#form$/.test(h)) g = 'cta_form';
    if (!g) return;
    goal(g);
    return;
    try {
      var kk = 'mb_clk_' + g, last = 0;
      try { last = +sessionStorage.getItem(kk) || 0; } catch (x) {}
      if (Date.now() - last < 1800000) return;
      try { sessionStorage.setItem(kk, String(Date.now())); } catch (x) {}
      var body = JSON.stringify({ type: g, attr: window.__mbAttr() });
      if (navigator.sendBeacon) navigator.sendBeacon('/api/click', new Blob([body], { type: 'application/json' }));
      else fetch('/api/click', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: body, keepalive: true });
    } catch (x) {}
  });

  // формы
  document.querySelectorAll('.lead-form').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var name = f.elements.name, phone = f.elements.phone, ok = true;
      [name, phone].forEach(function (i) { var bad = !i.value.trim(); i.classList.toggle('invalid', bad); if (bad) ok = false; });
      if (!ok) return;
      var btn = f.querySelector('button'); btn.disabled = true; btn.textContent = 'Sending...';
      var v = phone.value.trim(), isTg = /^@|^t\.me|[a-z_]{4,}/i.test(v) && !/^\+?\d[\d\s()-]{6,}$/.test(v);
      var data = {
        name: name.value.trim(), comment: f.elements.comment.value.trim(), _gotcha: f.elements._gotcha.value,
        form: 'site-ae-' + f.dataset.page, page: f.dataset.page, from: 'makebiztechnologies.com EN', attr: window.__mbAttr(),
        method: isTg ? 'Telegram' : 'Phone'
      };
      if (isTg) data.telegram = v; else data.phone = v;
      fetch('/api/lead', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) })
        .then(function (r) { return r.json(); })
        .then(function (r) {
          if (!r || r.ok === false) throw 0;
          f.querySelectorAll('label,button,.form-note').forEach(function (x) { x.hidden = true; });
          f.querySelector('.form-ok').hidden = false; goal('lead');
        })
        .catch(function () { f.querySelector('.form-err').hidden = false; btn.disabled = false; btn.textContent = 'Send request'; });
    });
  });
})();

// ===== 3D и живые панели
(function () {
  // наклон панели героя за мышью
  document.querySelectorAll('.vis-wrap').forEach(function (w) {
    var v = w.querySelector('.vis'); if (!v) return;
    w.addEventListener('pointermove', function (e) { if (innerWidth < 960) return; var r = w.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5; v.style.transform = 'rotateY(' + (-12 + x * 12) + 'deg) rotateX(' + (5 - y * 10) + 'deg)'; });
    w.addEventListener('pointerleave', function () { v.style.transform = ''; });
  });
  // наклон карточек
  document.querySelectorAll('.tilt').forEach(function (b) {
    b.addEventListener('pointermove', function (e) { if (innerWidth < 960) return; var r = b.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5; b.style.transform = 'perspective(900px) rotateY(' + x * 7 + 'deg) rotateX(' + (-y * 7) + 'deg) translateY(-4px)'; });
    b.addEventListener('pointerleave', function () { b.style.transform = ''; });
  });
  // появление шагов
  var obs = 'IntersectionObserver' in window ? new IntersectionObserver(function (es) { es.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add('on'); obs.unobserve(x.target); } }); }, { threshold: .25 }) : null;
  document.querySelectorAll('.steps,.track').forEach(function (el) { obs ? obs.observe(el) : el.classList.add('on'); });

  function rnd(a) { return a[Math.floor(Math.random() * a.length)]; }
  function money() { return 'AED ' + Math.round(Math.random() * 45 + 5) + 'K'; }
  var A = {
    board: function (v) {
      var N = ['Al Noor', 'Gulf Logistics', 'Marina Realty', 'Emirates Build', 'Desert Foods', 'Smart Clinic', 'AutoHouse', 'Palm Supply', 'Creek Decor', 'Falcon Tech'], S = ['WhatsApp', 'Website', 'Call', 'Instagram', 'Bayut'];
      var cols = v.querySelectorAll('.col'), cnt = v.querySelector('[data-cnt]'), c = 24, k = 0;
      function card() { var d = document.createElement('div'); d.className = 'dl' + (Math.random() < .25 ? ' hot' : ''); d.innerHTML = '<b>' + N[k % N.length] + '</b><small>' + S[k % S.length] + ' · ' + money() + '</small>'; k++; return d; }
      for (var s = 0; s < 4; s++) for (var j = 0; j < 3 - Math.floor(s / 2); j++) cols[s].appendChild(card());
      setInterval(function () {
        for (var s = 3; s >= 0; s--) { var cs = cols[s].querySelectorAll('.dl'); if (s === 3) { if (cs.length > 2) cs[cs.length - 1].remove(); continue; } if (cs.length && Math.random() < .55) { var d = cs[cs.length - 1]; d.remove(); d.style.animation = 'none'; void d.offsetWidth; d.style.animation = ''; cols[s + 1].insertBefore(d, cols[s + 1].children[1]); var nx = cols[s + 1].querySelectorAll('.dl'); for (var q = nx.length - 1; q >= 3; q--) nx[q].remove(); } }
        if (cols[0].querySelectorAll('.dl').length < 3) cols[0].insertBefore(card(), cols[0].children[1]); if (Math.random() < .5) c++; if (cnt) cnt.textContent = c;
      }, 1600);
    },
    tickets: function (v) {
      var box = v.querySelector('.rows'), T = ['Form does not create deals', 'Set up Zoho Books exchange', 'Train a new department', 'Adjust the pipeline', 'Warehouse access rights', 'Automation does not set a task', 'Connect telephony', 'New fields in the card'], k = 0, cnt = v.querySelector('[data-cnt]'), done = 128;
      function row(st) { var d = document.createElement('div'); d.className = 'rw'; d.innerHTML = '<span class="ico">B24</span><span class="tx"><b>' + T[k++ % T.length] + '</b><small>request No. ' + (2400 + k) + '</small></span><span class="st ' + (st === 'New' ? 'new' : st === 'Solved' ? 'ok' : '') + '">' + st + '</span>'; return d; }
      ['New', 'In progress', 'In progress', 'Solved', 'Solved'].forEach(function (s) { box.appendChild(row(s)); });
      setInterval(function () { var rs = box.querySelectorAll('.rw'); var w = [].filter.call(rs, function (r) { return r.querySelector('.st').textContent === 'In progress'; }); if (w.length) { var st = w[w.length - 1].querySelector('.st'); st.textContent = 'Solved'; st.className = 'st ok'; done++; if (cnt) cnt.textContent = done; }
        var n = [].filter.call(rs, function (r) { return r.querySelector('.st').textContent === 'New'; }); n.forEach(function (r) { var st = r.querySelector('.st'); st.textContent = 'In progress'; st.className = 'st'; });
        box.insertBefore(row('New'), box.firstChild); var all = box.querySelectorAll('.rw'); if (all.length > 5) all[all.length - 1].remove(); }, 2000);
    },
    chat: function (v) {
      var box = v.querySelector('.msgs'), seq = [['in', 'ch-wa', 'WhatsApp', 'Hello, how much is a CRM setup?'], ['out', '', 'Manager, from Bitrix24', 'Good afternoon! CRM setup starts from AED 10,000, could you tell us about the company?'], ['in', 'ch-tg', 'Telegram', 'Please send a quote'], ['ai', '', 'AI agent', 'Quote sent, deal moved to the Quote stage'], ['in', 'ch-av', 'Instagram', 'Is the Marina apartment still available?'], ['in', 'ch-wa', 'WhatsApp', 'Can we call tomorrow?']], i = 0;
      function add() { var m = seq[i++ % seq.length], d = document.createElement('div'); d.className = 'msg ' + m[0]; d.innerHTML = '<small class="' + m[1] + '">' + m[2] + '</small>' + m[3]; box.appendChild(d); var all = box.querySelectorAll('.msg'); if (all.length > 4) all[0].remove(); }
      add(); add(); setInterval(add, 2200);
    },
    sync: function (v) {
      var its = v.querySelectorAll('.it'), cnt = v.querySelector('[data-cnt]'), n = 1240, i = 0;
      setInterval(function () { var a = its[i % its.length]; a.classList.add('flash'); setTimeout(function () { a.classList.remove('flash'); }, 900); i++; n += 1; if (cnt) cnt.textContent = n.toLocaleString('en-US'); }, 700);
    },
    license: function (v) {
      var ts = v.querySelectorAll('.tier'), i = 0;
      setInterval(function () { ts.forEach(function (t) { t.classList.remove('on'); }); ts[i++ % ts.length].classList.add('on'); }, 2200);
      ts[0].classList.add('on');
    },
    bi: function (v) {
      v.querySelectorAll('[data-to]').forEach(function (el) { var to = +el.dataset.to, suf = el.dataset.suf || '', t0 = null; function step(t) { if (!t0) t0 = t; var p = Math.min(1, (t - t0) / 1800); el.textContent = Math.round(to * (1 - Math.pow(1 - p, 3))).toLocaleString('en-US') + suf; if (p < 1) requestAnimationFrame(step); } requestAnimationFrame(step); });
    },
    agents: function (v) {
      var box = v.querySelector('.rows'), E = [['L', 'Liaison', 'Replied to a client in WhatsApp in 12 sec'], ['F', 'Finance', 'Account balances updated'], ['A', 'Analyst', 'Reviewed 48 calls, 3 need attention'], ['P', 'Procurement', 'Collected 6 price lists, best is 8% cheaper'], ['Q', 'Qualifier', 'Hot lead passed to a manager'], ['H', 'Recruiter', 'Candidate passed the test, invitation sent']], i = 0;
      function add() { var e = E[i++ % E.length], d = document.createElement('div'); d.className = 'rw'; d.innerHTML = '<span class="ico">' + e[0] + '</span><span class="tx"><b>' + e[1] + '</b><small>' + e[2] + '</small></span><span class="st ok">done</span>'; box.insertBefore(d, box.firstChild); var all = box.querySelectorAll('.rw'); if (all.length > 5) all[all.length - 1].remove(); }
      for (var k = 0; k < 4; k++) add(); setInterval(add, 2000);
    }
  };
  document.querySelectorAll('[data-vis]').forEach(function (v) { var f = A[v.dataset.vis]; if (f) f(v); });
})();
;document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('.sh-t');if(!b)return;var f=b.closest('.shot'),im=f.querySelector('img');f.querySelectorAll('.sh-t').forEach(function(x){x.classList.toggle('on',x===b)});im.style.opacity=.2;var n=new Image();n.onload=function(){im.src=b.dataset.src;im.alt=b.dataset.alt;im.style.opacity=1};n.src=b.dataset.src;var s=f.querySelector('.shot-bar span');if(s)s.textContent=b.textContent});
;(function(){var f=document.querySelector('.kfilter');if(!f)return;var st={ind:'',prod:''},box=document.querySelector(f.dataset.target),em=document.querySelector('.kf-empty');
function ap(){var n=0;box.querySelectorAll('.case').forEach(function(c){var ok=(!st.ind||(' '+c.dataset.ind+' ').indexOf(' '+st.ind+' ')>-1)&&(!st.prod||(' '+c.dataset.prod+' ').indexOf(' '+st.prod+' ')>-1);c.hidden=!ok;if(ok)n++});if(em)em.hidden=n>0;
f.querySelectorAll('.fchip').forEach(function(b){b.classList.toggle('on',st[b.dataset.f]===b.dataset.v)})}
f.addEventListener('click',function(e){var b=e.target.closest('.fchip');if(!b)return;st[b.dataset.f]=b.dataset.v;ap();try{history.replaceState(null,'',st.ind?'#'+st.ind:location.pathname)}catch(x){}});
var h=(location.hash||'').slice(1);if(h&&f.querySelector('[data-f=ind][data-v="'+h+'"]')){st.ind=h;ap()}})();
;(function(){var c=document.querySelector('.pcalc');if(!c)return;function fm(x){return 'AED '+Math.round(x).toLocaleString('en-US')}
function up(){var n=+c.querySelector('[data-i=n]').value,k=+c.querySelector('[data-i=c]').value,first=n*k*.2,rep=n*k*.5*3*.1;
c.querySelector('[data-o=n]').textContent=n;c.querySelector('[data-o=c]').textContent=fm(k);c.querySelector('[data-o=first]').textContent=fm(first);c.querySelector('[data-o=rep]').textContent=fm(rep);c.querySelector('[data-o=tot]').textContent=fm(first+rep)}
c.addEventListener('input',up);up()})();
;document.addEventListener('click',function(e){var y=e.target.closest&&e.target.closest('.yt');if(!y||y.querySelector('iframe'))return;var f=document.createElement('iframe');f.src='https://www.youtube-nocookie.com/embed/'+y.dataset.id+'?autoplay=1';f.allow='autoplay; encrypted-media; picture-in-picture';f.allowFullscreen=true;f.title='MakeBiz video';y.appendChild(f);try{if(window.ym)ym(112503709,'reachGoal','video_play')}catch(x){}});

// ===== фон «Лучи» в цветах флага ОАЭ (как на прошлом makebiztechnologies.com): тёмная подложка и мягкие лучи за курсором
;(function(){
  if (window.__mbBeams) return; window.__mbBeams = 1;
  var BG = '#04050A', BEAMS = [[.12,'#16C15A',.15,120,0],[.30,'#EAF1FF',.08,90,1.6],[.48,'#0C7A33',.17,150,3.1],[.68,'#C8102E',.13,110,4.4],[.86,'#16C15A',.12,130,2.2]];
  var c = document.createElement('canvas'); c.id = 'mb-bg'; c.setAttribute('aria-hidden', 'true');
  document.body.insertBefore(c, document.body.firstChild);
  var ctx = c.getContext('2d'), b = {W:1,H:1,mx:.5,my:.4,tx:.5,ty:.4,active:false,af:0,t:0};
  var reduced = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches; if (reduced) b.t = 4.2;
  function rgba(h, a){ var n = parseInt(h.slice(1), 16); return 'rgba(' + ((n>>16)&255) + ',' + ((n>>8)&255) + ',' + (n&255) + ',' + a + ')'; }
  function resize(){ b.W = innerWidth; b.H = innerHeight; var d = Math.min(devicePixelRatio || 1, 1.6); c.width = Math.round(b.W*d); c.height = Math.round(b.H*d); ctx.setTransform(d,0,0,d,0,0); }
  resize(); addEventListener('resize', resize);
  addEventListener('pointermove', function(e){ b.tx = e.clientX / b.W; b.ty = e.clientY / b.H; b.active = true; }, {passive:true});
  document.documentElement.addEventListener('pointerleave', function(){ b.active = false; });
  function draw(){
    var W = b.W, H = b.H, t = b.t, mx = b.mx * W;
    ctx.globalCompositeOperation = 'source-over'; ctx.fillStyle = BG; ctx.fillRect(0,0,W,H);
    ctx.globalCompositeOperation = 'lighter'; ctx.save(); ctx.translate(W/2,0); ctx.rotate(-.3); ctx.translate(-W/2,0);
    for (var i = 0; i < BEAMS.length; i++){ var o = BEAMS[i], bx = o[0]*W + Math.sin(t*.18 + o[4])*W*.04, near = Math.exp(-((bx-mx)*(bx-mx))/160000)*b.af, w = o[3]*(1+.35*near), g = ctx.createLinearGradient(bx-w,0,bx+w,0);
      g.addColorStop(0, rgba(o[1],0)); g.addColorStop(.5, rgba(o[1], o[2]*(1+1.1*near))); g.addColorStop(1, rgba(o[1],0)); ctx.fillStyle = g; ctx.fillRect(bx-w,-H*.3,w*2,H*1.8); }
    ctx.restore();
    var tg = ctx.createLinearGradient(0,0,0,H*.5); tg.addColorStop(0, rgba('#0C7A33',.12)); tg.addColorStop(1,'rgba(0,0,0,0)'); ctx.fillStyle = tg; ctx.fillRect(0,0,W,H*.5);
    if (b.af > .01){ var gr = ctx.createRadialGradient(b.mx*W,b.my*H,0,b.mx*W,b.my*H,300); gr.addColorStop(0, rgba('#EAF1FF',.04*b.af)); gr.addColorStop(1, rgba('#EAF1FF',0)); ctx.fillStyle = gr; ctx.beginPath(); ctx.arc(b.mx*W,b.my*H,300,0,6.2832); ctx.fill(); }
    ctx.globalCompositeOperation = 'source-over';
    var vg = ctx.createLinearGradient(0,H*.55,0,H); vg.addColorStop(0,'rgba(0,0,0,0)'); vg.addColorStop(1,'rgba(2,3,5,.55)'); ctx.fillStyle = vg; ctx.fillRect(0,H*.55,W,H*.45);
  }
  var last = null;
  function frame(now){ if (last == null) last = now; var dt = Math.min((now-last)/1000,.05); last = now; if (!reduced) b.t += dt*.72; b.mx += (b.tx-b.mx)*.07; b.my += (b.ty-b.my)*.07; b.af += ((b.active?1:0)-b.af)*.06; draw(); requestAnimationFrame(frame); }
  requestAnimationFrame(frame);
})();
