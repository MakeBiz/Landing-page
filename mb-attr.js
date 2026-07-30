/* =====================================================================
   MakeBiz. Источник заявки: utm-метки, gclid, yclid и переход извне.

   Что делает:
     1) при заходе с рекламной меткой запоминает её в браузере на 90 дней;
     2) хранит два касания: первое (откуда человек узнал о нас) и последнее
        (по какой рекламе он пришёл перед заявкой);
     3) незаметно подмешивает эти данные в любую отправку на /api/lead,
        поэтому формы на страницах менять не нужно.

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

  /* ---- подмешиваем источник в заявку ---- */
  var orig = window.fetch;
  if (typeof orig === 'function') {
    window.fetch = function (input, init) {
      try {
        var url = typeof input === 'string' ? input
          : (input && typeof input.url === 'string' ? input.url : '');
        if (/\/api\/lead(\?|$)/.test(url) && init && typeof init.body === 'string') {
          var b = JSON.parse(init.body);
          if (b && typeof b === 'object' && !Array.isArray(b) && !b.attr) {
            b.attr = snapshot();
            var next = {};
            for (var k in init) if (Object.prototype.hasOwnProperty.call(init, k)) next[k] = init[k];
            next.body = JSON.stringify(b);
            return orig.call(this, input, next);
          }
        }
      } catch (e) {}
      return orig.apply(this, arguments);
    };
  }

  record();
})();
