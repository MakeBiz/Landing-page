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

  function goal(name) { try { if (window.ym) window.ym(112151442, 'reachGoal', name); } catch (e) {} try { if (window.gtag) window.gtag('event', name); } catch (e) {} }
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
    if (g === 'tg_channel' || g === 'cta_form' || /^\/en(\/|$)/.test(location.pathname)) return;
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
      var btn = f.querySelector('button'); btn.disabled = true; btn.textContent = 'Отправляем...';
      var v = phone.value.trim(), isTg = /^@|^t\.me|[a-z_]{4,}/i.test(v) && !/^\+?\d[\d\s()-]{6,}$/.test(v);
      var data = {
        name: name.value.trim(), comment: f.elements.comment.value.trim(), _gotcha: f.elements._gotcha.value,
        form: 'site-' + f.dataset.page, page: f.dataset.page, from: 'сайт makebiz.life', attr: window.__mbAttr(),
        method: isTg ? 'Telegram' : 'Телефон'
      };
      if (isTg) data.telegram = v; else data.phone = v;
      fetch('/api/lead', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) })
        .then(function (r) { return r.json(); })
        .then(function (r) {
          if (!r || r.ok === false) throw 0;
          f.querySelectorAll('label,button,.form-note').forEach(function (x) { x.hidden = true; });
          f.querySelector('.form-ok').hidden = false; goal('lead');
        })
        .catch(function () { f.querySelector('.form-err').hidden = false; btn.disabled = false; btn.textContent = 'Отправить заявку'; });
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
  function money() { return (Math.round(Math.random() * 90 + 10) * 1000).toLocaleString('ru-RU') + ' ₽'; }
  // анимации панелей работают только на экране и в активной вкладке
  function every(v, fn, ms) { setInterval(function () { if (document.hidden || v.__off) return; fn(); }, ms); }
  var vio = 'IntersectionObserver' in window ? new IntersectionObserver(function (es) { es.forEach(function (x) { x.target.__off = !x.isIntersecting; x.target.classList.toggle('is-off', !x.isIntersecting); }); }, { rootMargin: '120px' }) : null;
  var A = {
    board: function (v) {
      var N = ['ООО «Вектор»', 'ТД «Север»', 'Логистик Плюс', 'СтройМаркет', 'Альфа Опт', 'ИП Смирнов', 'МедЦентр', 'АвтоДом', 'ФудТрейд', 'ПромСнаб'], S = ['WhatsApp', 'Сайт', 'Звонок', 'Telegram', 'Авито'];
      var cols = v.querySelectorAll('.col'), cnt = v.querySelector('[data-cnt]'), c = 24, k = 0;
      function card() { var d = document.createElement('div'); d.className = 'dl' + (Math.random() < .25 ? ' hot' : ''); d.innerHTML = '<b>' + N[k % N.length] + '</b><small>' + S[k % S.length] + ' · ' + money() + '</small>'; k++; return d; }
      for (var s = 0; s < 4; s++) for (var j = 0; j < 3 - Math.floor(s / 2); j++) cols[s].appendChild(card());
      every(v, function () {
        for (var s = 3; s >= 0; s--) { var cs = cols[s].querySelectorAll('.dl'); if (s === 3) { if (cs.length > 2) cs[cs.length - 1].remove(); continue; } if (cs.length && Math.random() < .55) { var d = cs[cs.length - 1]; d.remove(); d.style.animation = 'none'; void d.offsetWidth; d.style.animation = ''; cols[s + 1].insertBefore(d, cols[s + 1].children[1]); var nx = cols[s + 1].querySelectorAll('.dl'); for (var q = nx.length - 1; q >= 3; q--) nx[q].remove(); } }
        if (cols[0].querySelectorAll('.dl').length < 3) cols[0].insertBefore(card(), cols[0].children[1]); if (Math.random() < .5) c++; if (cnt) cnt.textContent = c;
      }, 1600);
    },
    tickets: function (v) {
      var box = v.querySelector('.rows'), T = ['Не создаются сделки из формы', 'Настроить обмен с 1С', 'Обучить новый отдел', 'Доработать воронку', 'Права доступа для склада', 'Робот не ставит задачу', 'Подключить телефонию', 'Новые поля в карточке'], k = 0, cnt = v.querySelector('[data-cnt]'), done = 128;
      function row(st) { var d = document.createElement('div'); d.className = 'rw'; d.innerHTML = '<span class="ico">Б24</span><span class="tx"><b>' + T[k++ % T.length] + '</b><small>заявка №' + (2400 + k) + '</small></span><span class="st ' + (st === 'Новая' ? 'new' : st === 'Решено' ? 'ok' : '') + '">' + st + '</span>'; return d; }
      ['Новая', 'В работе', 'В работе', 'Решено', 'Решено'].forEach(function (s) { box.appendChild(row(s)); });
      every(v, function () { var rs = box.querySelectorAll('.rw'); var w = [].filter.call(rs, function (r) { return r.querySelector('.st').textContent === 'В работе'; }); if (w.length) { var st = w[w.length - 1].querySelector('.st'); st.textContent = 'Решено'; st.className = 'st ok'; done++; if (cnt) cnt.textContent = done; }
        var n = [].filter.call(rs, function (r) { return r.querySelector('.st').textContent === 'Новая'; }); n.forEach(function (r) { var st = r.querySelector('.st'); st.textContent = 'В работе'; st.className = 'st'; });
        box.insertBefore(row('Новая'), box.firstChild); var all = box.querySelectorAll('.rw'); if (all.length > 5) all[all.length - 1].remove(); }, 2000);
    },
    chat: function (v) {
      var box = v.querySelector('.msgs'), seq = [['in', 'ch-wa', 'WhatsApp', 'Здравствуйте, сколько стоит настройка CRM?'], ['out', '', 'Менеджер, из Битрикс24', 'Добрый день! Стандартная настройка 97 500 ₽, расскажете о компании?'], ['in', 'ch-tg', 'Telegram', 'Пришлите КП, пожалуйста'], ['ai', '', 'ИИ-агент', 'КП отправлено, сделка переведена на этап «КП»'], ['in', 'ch-av', 'Авито', 'Объявление ещё актуально?'], ['in', 'ch-max', 'MAX', 'Можно созвониться завтра?']], i = 0;
      function add() { var m = seq[i++ % seq.length], d = document.createElement('div'); d.className = 'msg ' + m[0]; d.innerHTML = '<small class="' + m[1] + '">' + m[2] + '</small>' + m[3]; box.appendChild(d); var all = box.querySelectorAll('.msg'); if (all.length > 4) all[0].remove(); }
      add(); add(); every(v, add, 2200);
    },
    sync: function (v) {
      var its = v.querySelectorAll('.it'), cnt = v.querySelector('[data-cnt]'), n = 1240, i = 0;
      every(v, function () { var a = its[i % its.length]; a.classList.add('flash'); setTimeout(function () { a.classList.remove('flash'); }, 900); i++; n += 1; if (cnt) cnt.textContent = n.toLocaleString('ru-RU'); }, 700);
    },
    license: function (v) {
      var ts = v.querySelectorAll('.tier'), i = 0;
      every(v, function () { ts.forEach(function (t) { t.classList.remove('on'); }); ts[i++ % ts.length].classList.add('on'); }, 2200);
      ts[0].classList.add('on');
    },
    bi: function (v) {
      v.querySelectorAll('[data-to]').forEach(function (el) { var to = +el.dataset.to, suf = el.dataset.suf || '', t0 = null; function step(t) { if (!t0) t0 = t; var p = Math.min(1, (t - t0) / 1800); el.textContent = Math.round(to * (1 - Math.pow(1 - p, 3))).toLocaleString('ru-RU') + suf; if (p < 1) requestAnimationFrame(step); } requestAnimationFrame(step); });
    },
    agents: function (v) {
      var box = v.querySelector('.rows'), E = [['С', 'Связной', 'Ответил клиенту в WhatsApp за 12 сек'], ['Ф', 'Финансист', 'Остатки по счетам обновлены'], ['А', 'Аналитик', 'Разобрал 48 звонков, 3 требуют внимания'], ['З', 'Закупщик', 'Собрал 6 прайсов, лучший на 8% дешевле'], ['К', 'Квалификатор', 'Горячий лид передан менеджеру'], ['Н', 'Наймщик', 'Кандидат прошёл тест, приглашение отправлено']], i = 0;
      function add() { var e = E[i++ % E.length], d = document.createElement('div'); d.className = 'rw'; d.innerHTML = '<span class="ico">' + e[0] + '</span><span class="tx"><b>' + e[1] + '</b><small>' + e[2] + '</small></span><span class="st ok">готово</span>'; box.insertBefore(d, box.firstChild); var all = box.querySelectorAll('.rw'); if (all.length > 5) all[all.length - 1].remove(); }
      for (var k = 0; k < 4; k++) add(); every(v, add, 2000);
    }
  };
  document.querySelectorAll('[data-vis]').forEach(function (v) { var f = A[v.dataset.vis]; if (f) f(v); if (vio) vio.observe(v); });
  if (vio) document.querySelectorAll('.mq,.aiblk').forEach(function (m) { vio.observe(m); });
})();
;document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('.sh-t');if(!b)return;var f=b.closest('.shot'),im=f.querySelector('img');f.querySelectorAll('.sh-t').forEach(function(x){x.classList.toggle('on',x===b)});im.style.opacity=.2;var n=new Image();n.onload=function(){im.src=b.dataset.src;im.alt=b.dataset.alt;im.style.opacity=1};n.src=b.dataset.src;var s=f.querySelector('.shot-bar span');if(s)s.textContent=b.textContent});
;(function(){var f=document.querySelector('.kfilter');if(!f)return;var st={ind:'',prod:''},box=document.querySelector(f.dataset.target),em=document.querySelector('.kf-empty');
function ap(){var n=0;box.querySelectorAll('.case').forEach(function(c){var ok=(!st.ind||(' '+c.dataset.ind+' ').indexOf(' '+st.ind+' ')>-1)&&(!st.prod||(' '+c.dataset.prod+' ').indexOf(' '+st.prod+' ')>-1);c.hidden=!ok;if(ok)n++});if(em)em.hidden=n>0;
f.querySelectorAll('.fchip').forEach(function(b){b.classList.toggle('on',st[b.dataset.f]===b.dataset.v)})}
f.addEventListener('click',function(e){var b=e.target.closest('.fchip');if(!b)return;st[b.dataset.f]=b.dataset.v;ap();try{history.replaceState(null,'',st.ind?'#'+st.ind:location.pathname)}catch(x){}});
var h=(location.hash||'').slice(1);if(h&&f.querySelector('[data-f=ind][data-v="'+h+'"]')){st.ind=h;ap()}})();
;(function(){var c=document.querySelector('.pcalc');if(!c)return;function fm(x){return Math.round(x).toLocaleString('ru-RU')+' ₽'}
function up(){var n=+c.querySelector('[data-i=n]').value,k=+c.querySelector('[data-i=c]').value,first=n*k*.2,rep=n*k*.5*3*.1;
c.querySelector('[data-o=n]').textContent=n;c.querySelector('[data-o=c]').textContent=fm(k);c.querySelector('[data-o=first]').textContent=fm(first);c.querySelector('[data-o=rep]').textContent=fm(rep);c.querySelector('[data-o=tot]').textContent=fm(first+rep)}
c.addEventListener('input',up);up()})();
;document.addEventListener('click',function(e){var y=e.target.closest&&e.target.closest('.yt');if(!y||y.querySelector('iframe'))return;var f=document.createElement('iframe');f.src='https://www.youtube-nocookie.com/embed/'+y.dataset.id+'?autoplay=1';f.allow='autoplay; encrypted-media; picture-in-picture';f.allowFullscreen=true;f.title='Видео MakeBiz';y.appendChild(f);try{if(window.ym)ym(112151442,'reachGoal','video_play')}catch(x){}});
;(function(){var c=navigator.connection;if(c&&(c.saveData||/2g/.test(c.effectiveType||'')))return;var done={},tm;function ok(a){if(!a||!a.href||a.target==='_blank'||a.hasAttribute('download'))return false;var u;try{u=new URL(a.href)}catch(e){return false}if(u.origin!==location.origin||u.search||/^\/api\/|\.(xml|txt|pdf|zip|png|jpe?g|webp|svg)$/i.test(u.pathname))return false;if(u.pathname===location.pathname)return false;return u.pathname}function go(p){if(done[p])return;done[p]=1;var l=document.createElement('link');l.rel='prefetch';l.href=p;document.head.appendChild(l)}document.addEventListener('mouseover',function(e){var a=e.target.closest&&e.target.closest('a');var p=ok(a);if(!p)return;clearTimeout(tm);tm=setTimeout(function(){go(p)},65)},{passive:true});document.addEventListener('mouseout',function(){clearTimeout(tm)},{passive:true});document.addEventListener('touchstart',function(e){var a=e.target.closest&&e.target.closest('a');var p=ok(a);if(p)go(p)},{passive:true});})();
;(function(){if(window.__mbLeadPatch||!window.fetch)return;window.__mbLeadPatch=1;var of=window.fetch;window.fetch=function(u,o){try{var url=typeof u==='string'?u:(u&&u.url)||'';if(/\/api\/lead(\?|$)/.test(url)&&o&&typeof o.body==='string'){var d=JSON.parse(o.body);if(d&&typeof d==='object'){var ch=0;if(!d.attr&&window.__mbAttr){d.attr=window.__mbAttr();ch=1}if(!d._title){d._title=String(document.title||'').slice(0,200);ch=1}if(!d._url){d._url=String(location.href).slice(0,500);ch=1}if(ch){o=Object.assign({},o,{body:JSON.stringify(d)})}}}}catch(e){}return of.call(this,u,o)}})();
