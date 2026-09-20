/* =====================================================================
   MakeBiz. Источник заявки: utm-метки, gclid, yclid и переход извне.

   Что делает:
     1) при заходе с рекламной меткой запоминает её в браузере на 90 дней;
     2) хранит два касания: первое (откуда человек узнал о нас) и последнее
        (по какой рекламе он пришёл перед заявкой);
     3) незаметно подмешивает эти данные в любую отправку на /api/lead,
        поэтому формы на страницах менять не нужно;
     4) отправляет цели в Метрику (счётчик 112503709) и события в GA4:
        lead после успешной заявки; call / telegram / whatsapp / max / email / tg_channel
        при клике по контакту; form_view и form_start по форме; demo по записи на
        демонстрацию; calc_agent / calc_select / calc_tariff / calc_cta в калькуляторе;
        scroll_75 по дочитыванию страницы. Метрика включается только после согласия
        на cookie, до согласия цели в неё не уходят.

   Файл подключается в <head> каждой страницы. Повторный запуск безопасен.
   ===================================================================== */
(function () {
  'use strict';
  if (window.__mbAttrDone) return;
  window.__mbAttrDone = 1;

  var KEY = 'mb_attr';
  var TTL = 90 * 24 * 60 * 60 * 1000;   // 90 дней
  var MARKS = [
    'utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term',
    'gclid', 'gbraid', 'wbraid', 'yclid', 'ymclid', 'fbclid', 'ttclid', 'msclkid'
  ];

  function box() {
    try {
      var s = window.localStorage;
      s.setItem('__mb_t', '1');
      s.removeItem('__mb_t');
      return s;
    } catch (e) {
      try { return window.sessionStorage; } catch (e2) { return null; }
    }
  }

  function load() {
    var s = box();
    if (!s) return null;
    try {
      var d = JSON.parse(s.getItem(KEY) || 'null');
      if (!d || !d.first || !d.first.ts) return null;
      if (Date.now() - d.first.ts > TTL) { s.removeItem(KEY); return null; }
      return d;
    } catch (e) { return null; }
  }

  function save(d) {
    var s = box();
    if (!s) return;
    try { s.setItem(KEY, JSON.stringify(d)); } catch (e) {}
  }

  function cut(v, n) { return String(v == null ? '' : v).slice(0, n || 200); }

  function marks() {
    var out = {};
    try {
      var q = new URLSearchParams(location.search);
      MARKS.forEach(function (k) { var v = q.get(k); if (v) out[k] = cut(v); });
    } catch (e) {}
    return out;
  }

  /* реферер считаем только внешний: переходы внутри сайта источником не являются */
  function referrer() {
    var r = document.referrer || '';
    if (!r) return '';
    try { if (new URL(r).hostname === location.hostname) return ''; } catch (e) { return ''; }
    return cut(r, 300);
  }

  function touch() {
    var t = { ts: Date.now(), path: cut(location.pathname + location.search, 300) };
    var r = referrer();
    if (r) t.ref = r;
    var m = marks();
    for (var k in m) if (Object.prototype.hasOwnProperty.call(m, k)) t[k] = m[k];
    return t;
  }

  function record() {
    var d = load();
    var t = touch();
    var hasMark = MARKS.some(function (k) { return !!t[k]; });
    if (!d) {
      save({ first: t, last: t });
      return;
    }
    // новое касание фиксируем, только если пришли по рекламе или из внешнего источника
    if (hasMark || t.ref) { d.last = t; save(d); }
  }

  function snapshot() {
    var d = load() || {};
    var s = { url: cut(location.href, 500) };
    if (d.first) s.first = d.first;
    if (d.last && d.first && d.last.ts !== d.first.ts) s.last = d.last;
    return s;
  }
  window.__mbAttr = snapshot;

  /* ---- цели Метрики и события GA4 ----
     Контакты: call, telegram, whatsapp, max, email, tg_channel
     Форма: form_view (форма попала в зону видимости), form_start (начал заполнять), lead (сервер принял заявку)
     Калькулятор в iframe: calc_agent (открыл карточку агента), calc_select (отметил агента),
       calc_tariff (выбрал тариф), calc_cta (кнопка заявки внутри калькулятора)
     Прочее: demo (запись на демонстрацию), scroll_75 (дочитал страницу до 75%)
     Метрика включается после согласия на cookie, до него цели в неё не уходят. */
  var YM_ID = 112503709;
  var CONTACTS = { call: 1, telegram: 1, whatsapp: 1, max: 1, email: 1, tg_channel: 1 };
  var fired = {};
  function goal(name, once) {
    if (once) { if (fired[name]) return; fired[name] = 1; }
    var w = window;
    try {
      /* страница внутри iframe нашего же сайта (калькулятор): цель отдаём родителю */
      if (typeof w.ym !== 'function' && typeof w.gtag !== 'function' &&
          w.parent && w.parent !== w && typeof w.parent.__mbGoal === 'function') {
        w.parent.__mbGoal(name);
        return;
      }
    } catch (e) {}
    try { if (typeof w.ym === 'function') w.ym(YM_ID, 'reachGoal', name); } catch (e) {}
    try {
      if (typeof w.gtag === 'function') {
        if (name === 'lead') w.gtag('event', 'generate_lead');
        else if (CONTACTS[name]) w.gtag('event', 'contact_click', { method: name });
        else w.gtag('event', name);
      }
    } catch (e) {}
  }
  window.__mbGoal = goal;

  function contactKind(href) {
    var h = String(href || '').toLowerCase();
    if (/^tel:/.test(h)) return 'call';
    if (/^mailto:/.test(h)) return 'email';
    if (/^https?:\/\/(www\.)?t\.me\/makebizchannel/.test(h)) return 'tg_channel';
    if (/^tg:/.test(h) || /^https?:\/\/(www\.)?(t\.me|telegram\.me)\//.test(h)) return 'telegram';
    if (/^whatsapp:/.test(h) || /^https?:\/\/(www\.)?(wa\.me|api\.whatsapp\.com|chat\.whatsapp\.com|whatsapp\.com)\//.test(h)) return 'whatsapp';
    if (/^https?:\/\/(www\.)?max\.ru\//.test(h)) return 'max';
    return '';
  }

  var ON_CALC = /^\/calculator-agents-app/.test(location.pathname);
  function txt(el) { return ((el && (el.innerText || el.textContent)) || '').replace(/\s+/g, ' ').trim(); }
  /* ищем у клика ближайший осмысленный подпись-элемент: сам элемент или до четырёх родителей */
  function nearText(el, re, maxLen) {
    var n = el, i = 0, t;
    while (n && n.nodeType === 1 && i < 5) {
      t = txt(n);
      if (t && t.length <= (maxLen || 80) && re.test(t)) return t;
      n = n.parentElement; i++;
    }
    return '';
  }
  document.addEventListener('click', function (e) {
    try {
      var t = e.target;
      if (!t || !t.closest) return;
      var a = t.closest('a[href]');
      if (a) { var g = contactKind(a.getAttribute('href')); if (g) goal(g); }
      if (nearText(t, /^(Записаться на демонстрац|Записаться на демо|Book a demo|Request a demo)/i, 60)) goal('demo');
      if (!ON_CALC) return;
      if (nearText(t, /^(Подробнее|Details)$/i, 20)) goal('calc_agent');
      else if (nearText(t, /^(Выбрать|Select)/i, 40)) goal('calc_select');
      else if (nearText(t, /(Старт|Бизнес|Холдинг|Start|Business|Holding)[\s\S]{0,30}AED/, 70)) goal('calc_tariff');
      else if (nearText(t, /(Обсудить проект|Оставить заявку|Получить расчёт|Discuss the project|Leave a request)/i, 60)) goal('calc_cta');
    } catch (err) {}
  }, true);

  /* форма заявки: показ и начало заполнения */
  function watchForm() {
    var f = document.getElementById('mbcf-contact') || document.getElementById('mbcf-lead') || document.querySelector('.mbcf-wrap');
    if (!f) return false;
    if (f.__mbFormWatched) return true;
    f.__mbFormWatched = 1;
    try {
      if (window.IntersectionObserver) {
        var io = new IntersectionObserver(function (es) {
          for (var i = 0; i < es.length; i++) if (es[i].isIntersecting) { goal('form_view', 1); io.disconnect(); }
        }, { threshold: 0.35 });
        io.observe(f);
      } else { goal('form_view', 1); }
    } catch (e) {}
    var start = function (ev) {
      var el = ev && ev.target;
      if (el && el.tagName && /^(INPUT|TEXTAREA|SELECT)$/.test(el.tagName) && el.id !== 'mbcf-gotcha') goal('form_start', 1);
    };
    f.addEventListener('focusin', start, true);
    f.addEventListener('input', start, true);
    return true;
  }
  var fTries = 0, fIv = setInterval(function () { if (watchForm() || ++fTries > 40) clearInterval(fIv); }, 400);
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', watchForm); else watchForm();

  /* дочитал страницу: 75% высоты */
  var sTimer = null;
  window.addEventListener('scroll', function () {
    if (fired.scroll_75 || sTimer) return;
    sTimer = setTimeout(function () {
      sTimer = null;
      try {
        var h = document.documentElement;
        var total = Math.max(h.scrollHeight, document.body ? document.body.scrollHeight : 0) - window.innerHeight;
        var y = window.pageYOffset || h.scrollTop || 0;
        if (total > 500 && y / total >= 0.75) goal('scroll_75', 1);
      } catch (e) {}
    }, 400);
  }, false);

  /* ---- подмешиваем источник в заявку и отмечаем успешную отправку ---- */
  var orig = window.fetch;
  if (typeof orig === 'function') {
    window.fetch = function (input, init) {
      var lead = false, res = null;
      try {
        var url = typeof input === 'string' ? input
          : (input && typeof input.url === 'string' ? input.url : '');
        lead = /\/api\/lead(\?|$)/.test(url);
        if (lead && init && typeof init.body === 'string') {
          var b = JSON.parse(init.body);
          if (b && typeof b === 'object' && !Array.isArray(b) && !b.attr) {
            b.attr = snapshot();
            var next = {};
            for (var k in init) if (Object.prototype.hasOwnProperty.call(init, k)) next[k] = init[k];
            next.body = JSON.stringify(b);
            res = orig.call(this, input, next);
          }
        }
      } catch (e) {}
      if (!res) res = orig.apply(this, arguments);
      if (lead && res && typeof res.then === 'function') {
        res.then(function (r) { if (r && r.ok) goal('lead'); }, function () {});
      }
      return res;
    };
  }

  /* ---- ссылка на политику конфиденциальности под формой ----
     По 152-ФЗ и по требованиям модерации Яндекс.Директа фраза согласия должна
     открывать политику по клику. Вёрстка этого текста на страницах разная,
     поэтому вместо правки каждой формы находим фразу в тексте и оборачиваем
     её в ссылку. Бандл перерисовывает документ, поэтому повторяем по таймеру. */
  (function () {
    var EN = /^\/en(\/|$)/.test(location.pathname);
    var HREF = EN ? '/en/privacy' : '/privacy';
    var RE = EN
      ? /(personal data processing policy|privacy policy)/i
      : /(политик(?:ой|и|у|а) конфиденциальности|политик(?:ой|и|у|а) обработки персональных данных)/i;
    var runs = 0;
    /* на самих правовых страницах фраза это заголовок, ссылку туда не ставим */
    var SKIP_PAGE = /^\/(en\/)?(privacy|terms)(\/|$)/.test(location.pathname);

    function pass() {
      if (SKIP_PAGE) return;
      var w, n, hits = [];
      try { w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null); } catch (e) { return; }
      while ((n = w.nextNode())) {
        var v = n.nodeValue;
        if (!v || v.length > 400 || !RE.test(v)) continue;
        var p = n.parentNode;
        if (!p || p.nodeType !== 1) continue;
        if (p.closest('a, h1, h2, h3, script, style, #mb-ssr, #mbf-cookie, #mbcf-msgs')) continue;
        hits.push(n);
        if (hits.length > 12) break;
      }
      for (var i = 0; i < hits.length; i++) {
        var node = hits[i], m = RE.exec(node.nodeValue);
        if (!m) continue;
        var before = node.nodeValue.slice(0, m.index);
        var after = node.nodeValue.slice(m.index + m[0].length);
        var a = document.createElement('a');
        a.href = HREF;
        a.textContent = m[0];
        a.setAttribute('data-mb-policy', '1');
        a.style.color = 'inherit';
        a.style.textDecoration = 'underline';
        a.style.textUnderlineOffset = '2px';
        var frag = document.createDocumentFragment();
        if (before) frag.appendChild(document.createTextNode(before));
        frag.appendChild(a);
        if (after) frag.appendChild(document.createTextNode(after));
        try { node.parentNode.replaceChild(frag, node); } catch (e) {}
      }
    }

    function tick() { runs++; try { pass(); } catch (e) {} if (runs > 70) clearInterval(t); }
    var t = setInterval(tick, 900);
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', tick);
    else tick();
  })();

  /* ---- телефон в шапке ----
     Шапку рисует общий скрипт mbm, места в ней впритык: на 1512 px строка заполнена
     ровно по границе. Поэтому не задаём брейкпойнты наугад, а меряем: сначала пробуем
     номер текстом, не влезло - оставляем только иконку, не влезло и это - убираем совсем.
     В бургер-меню ссылка «Позвонить» есть всегда. */
  (function () {
    var TEL = '+971502620927';
    var HUMAN = '+971 50 262 0927';
    var EN = /^\/en(\/|$)/.test(location.pathname);
    var CALL = EN ? 'Call' : 'Позвонить';
    var ICON = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
      + '<path d="M6.6 10.8a15 15 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.24 11.4 11.4 0 0 0 3.6.58 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.46.58 3.6a1 1 0 0 1-.25 1z"/></svg>';
    var CSS = '#mbm-header .mb-ph{display:inline-flex;align-items:center;gap:7px;font:700 14px Oxygen,system-ui,sans-serif;'
      + 'color:#EAF1FF;text-decoration:none;white-space:nowrap;transition:color .15s}'
      + '#mbm-header .mb-ph:hover{color:#16C15A}'
      + '#mbm-header .mb-ph.mb-ph-icon .mb-ph-t{display:none}'
      + '#mbm-drop .mb-ph-drop{color:#16C15A;font-weight:700}';

    function style() {
      if (document.getElementById('mb-ph-css')) return;
      var st = document.createElement('style');
      st.id = 'mb-ph-css';
      st.textContent = CSS;
      (document.head || document.documentElement).appendChild(st);
    }

    function fit() {
      var inn = document.querySelector('#mbm-header .mbm-in');
      var el = document.querySelector('#mbm-header .mb-ph');
      if (!inn || !el) return;
      el.style.display = '';
      el.classList.remove('mb-ph-icon');
      if (inn.scrollWidth > inn.clientWidth + 1) el.classList.add('mb-ph-icon');
      if (inn.scrollWidth > inn.clientWidth + 1) el.style.display = 'none';
    }

    function place() {
      style();
      var right = document.querySelector('#mbm-header .mbm-right');
      if (right && !right.querySelector('.mb-ph')) {
        var a = document.createElement('a');
        a.className = 'mb-ph';
        a.href = 'tel:' + TEL;
        a.title = HUMAN;
        a.setAttribute('aria-label', CALL + ' ' + HUMAN);
        a.innerHTML = ICON + '<span class="mb-ph-t">' + HUMAN + '</span>';
        right.insertBefore(a, right.firstChild);
      }
      var drop = document.querySelector('#mbm-drop nav');
      if (drop && !drop.querySelector('.mb-ph-drop')) {
        var d = document.createElement('a');
        d.className = 'mb-ph-drop';
        d.href = 'tel:' + TEL;
        d.textContent = CALL + ' ' + HUMAN;
        drop.appendChild(d);
      }
      fit();
    }

    var t = setInterval(place, 900);
    setTimeout(function () { clearInterval(t); setInterval(place, 2500); }, 60000);
    window.addEventListener('resize', function () { clearTimeout(window.__mbPhT); window.__mbPhT = setTimeout(fit, 200); });
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', place);
    else place();
  })();

  record();

  /* ---- пиксель панели сквозной аналитики ------------------------------
     На бандл-страницах документ перерисовывается из шаблона, и тег из
     исходного head может не пережить перерисовку. Модуль возвращает его
     на место, если после отрисовки тега нет. Идемпотентен. */
  (function mbPx(){
    /* Пиксель панели сквозной аналитики.
       На бандл-страницах документ перерисовывается и тег из исходного head
       пропадает из DOM, хотя скрипт уже успел загрузиться и отправить событие.
       Поэтому проверяем не DOM, а факт сетевого запроса: так мы не поставим
       второй счётчик и не удвоим просмотры. */
    var HOST = 'makebiz-makebiz-platform-3628.twc1.net';
    function loaded(){
      try {
        var e = performance.getEntriesByType('resource');
        for (var i = 0; i < e.length; i++) if (e[i].name.indexOf(HOST) >= 0) return true;
      } catch (err) {}
      return !!document.querySelector('script[src*="' + HOST + '"]');
    }
    var tries = 0;
    (function check(){
      tries++;
      if (loaded()) return;
      if (tries > 12) {
        var s = document.createElement('script');
        s.defer = true;
        s.src = 'https://' + HOST + '/px/t.js';
        s.setAttribute('data-site', 'makebiz-com');
        s.setAttribute('data-endpoint', 'https://' + HOST + '/px');
        (document.head || document.documentElement).appendChild(s);
        return;
      }
      setTimeout(check, 700);
    })();
  })();
})();
