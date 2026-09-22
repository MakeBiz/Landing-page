
/* MakeBiz, мобильная раскладка (makebiztechnologies.com).
   Перенесено с makebiz.life (модуль __mbMobile) и дополнено тем, что нашлось на этом сайте.
   1) Поля форм 16px: Safari на iOS увеличивает страницу при фокусе в поле мельче 16px
   2) Нижняя граница кегля 12px и цель для пальца 40px
   3) Сетки в 3-5 колонок и пары «текст | картинка» из страниц-экспортов разбираются
      по вычисленному значению: бандлер нормализует инлайновый style, селектор по атрибуту
      ненадёжен. Плитки с короткими подписями идут в две колонки, секции с текстом в одну
   4) Точечные правки: блок кейсов без боковых отступов, растянутые карточки болей на
      /vector, боковое меню в макете кабинета, подвал под плавающими кнопками
   Класс и стиль переустанавливаются в цикле: бандлер при гидратации подменяет документ */
(function(){
  if(window.__mbMobile) return; window.__mbMobile=1;
  /* калькулятор в iframe: отдельное приложение со своей мобильной раскладкой */
  if(/calculator-agents-app/.test(location.pathname)) return;

  var CSS = '@media(max-width:760px){'
    + '.mb-1col{grid-template-columns:minmax(0,1fr)!important}'
    + '.mb-2col{grid-template-columns:repeat(2,minmax(0,1fr))!important}'
    + '.mb-1col>*,.mb-2col>*{min-width:0}'
    + 'h1,h2,h3,p,li{overflow-wrap:break-word}'
    + 'input:not([type=checkbox]):not([type=radio]):not([type=range]):not([type=hidden]),select,textarea{font-size:16px!important}'
    + '#mbcf-contact .mbcf-inp{padding:14px 15px!important}'
    + '#mbcf-contact .mbcf-submit{min-height:52px!important;font-size:16px!important}'
    + '#mbcf-contact .mbcf-seg button{min-height:42px!important;font-size:14px!important}'
    + '#mbcf-contact .mbcf-bubble{max-width:90%!important}'
    /* ссылки подвала шли строками по 20-24px, палец попадает в соседнюю */
    + '#mbf-footer .mbf-col a{display:block!important;padding:9px 0!important;font-size:14.5px!important}'
    /* кнопки «наверх» и cookie висят в нижних углах и закрывали строку копирайта */
    + '#mbf-footer{padding-bottom:84px!important}'
    /* блок кейсов вставляется во всю ширину, на телефоне карточки прилипали к краям экрана */
    + '#mb-cases-host{padding-left:18px!important;padding-right:18px!important}'
    /* /vector: карточки болей тянулись до высоты соседней колонки и стояли пустыми по 210px */
    + '[data-probgrid]>*{height:auto!important;min-height:0!important}'
    + '[data-probgrid] .mb-card{flex:none!important;min-height:0!important;height:auto!important}'
    /* макет кабинета: боковое меню занимало половину ширины, цифры шли по слогу в строке */
    + '[data-cab]>aside{display:none!important}'
    + '}';

  function style(){
    var st=document.getElementById('mb-mobile-css');
    if(st && st.parentNode) return;
    st=document.createElement('style'); st.id='mb-mobile-css'; st.textContent=CSS;
    (document.head||document.documentElement).appendChild(st);
  }

  function tlen(el){ return (el.textContent||'').replace(/\s+/g,' ').trim().length; }

  /* макеты интерфейса (кабинет, канбан, телефон) рисуют экран продукта: их сетки не трогаем */
  function inMockup(el){ return !!(el.closest && el.closest('[data-cab],[data-tilt],svg')); }

  function classOf(el){
    var cs=getComputedStyle(el);
    if(cs.display!=='grid') return '';
    var tracks=cs.gridTemplateColumns.trim().split(/\s+/).filter(Boolean);
    if(tracks.length<2 || tracks[0]==='none') return '';
    var kids=[], i;
    for(i=0;i<el.children.length;i++){
      if(getComputedStyle(el.children[i]).display!=='none') kids.push(el.children[i]);
    }
    if(kids.length<2) return '';
    var maxT=0, minW=1e9;
    for(i=0;i<kids.length;i++){
      var t=tlen(kids[i]); if(t>maxT) maxT=t;
      var w=kids[i].getBoundingClientRect().width; if(w<minW) minW=w;
    }
    var W=el.getBoundingClientRect().width, over=el.scrollWidth>W+2;
    if(tracks.length>=3){
      if(minW>=150 && !over) return '';
      return maxT<=60 ? 'mb-2col' : 'mb-1col';
    }
    /* две колонки трогаем, когда это раскладка секции или колонки вылезают за край */
    if(over) return 'mb-1col';
    if(W>=280 && maxT>80 && minW<220) return 'mb-1col';
    return '';
  }

  function fontFloor(){
    var els=document.querySelectorAll('p,li,span,div,td,a,summary,label,h4,h5,h6,b,strong'), i, c;
    for(i=0;i<els.length;i++){
      var el=els[i];
      if(el.getAttribute('data-mbfs')) continue;
      if(inMockup(el)){ el.setAttribute('data-mbfs','-'); continue; }
      var own='', cn=el.childNodes;
      for(c=0;c<cn.length;c++) if(cn[c].nodeType===3) own+=cn[c].textContent;
      if(own.replace(/\s+/g,' ').trim().length<6){ el.setAttribute('data-mbfs','-'); continue; }
      var fs=parseFloat(getComputedStyle(el).fontSize)||16;
      if(fs>0 && fs<12){ el.style.setProperty('font-size','12px','important'); el.setAttribute('data-mbfs','1'); }
      else el.setAttribute('data-mbfs','-');
    }
  }

  function textSibling(el){
    function t(x){ return !!x && x.nodeType===3 && x.textContent.replace(/\s+/g,'').length>0; }
    return t(el.previousSibling) || t(el.nextSibling);
  }

  function tapFloor(){
    var els=document.querySelectorAll('a,button,summary'), i;
    for(i=0;i<els.length;i++){
      var el=els[i];
      /* «x» разобрались, трогать не нужно; «1» уже поправили. Решения по размеру не запоминаем:
         на первых тиках бандл ещё собирается и коробка элемента бывает нулевой */
      var mark=el.getAttribute('data-mbtap');
      if(mark==='x') continue;
      if(mark==='1'){
        if(el.style.minHeight!=='40px'){
          el.style.setProperty('min-height','40px','important');
          el.style.setProperty('align-items','center','important');
        }
        continue;
      }
      if(inMockup(el) || (el.closest && el.closest('#mbf-footer,#mbm-header,header'))){ el.setAttribute('data-mbtap','x'); continue; }
      var txt=(el.textContent||'').replace(/\s+/g,' ').trim();
      if(!txt || txt.length>40){ el.setAttribute('data-mbtap','x'); continue; }
      if(textSibling(el)){ el.setAttribute('data-mbtap','x'); continue; }
      var host=el.closest ? el.closest('p,li,figcaption,small,blockquote') : null;
      if(host && host!==el){
        var ht=(host.textContent||'').replace(/\s+/g,' ').trim();
        if(ht.length>txt.length+3){ el.setAttribute('data-mbtap','x'); continue; }
      }
      var cs=getComputedStyle(el);
      if(cs.position==='absolute' || cs.position==='fixed'){ el.setAttribute('data-mbtap','x'); continue; }
      var r=el.getBoundingClientRect();
      if(r.width<56 || r.height===0 || r.height>=40) continue;
      el.style.setProperty('min-height','40px','important');
      if(cs.display==='inline') el.style.setProperty('display','inline-flex','important');
      el.style.setProperty('align-items','center','important');
      el.setAttribute('data-mbtap','1');
    }
  }

  function grids(){
    var els=document.querySelectorAll('[style*="grid"],[class*="grid"],[class*="g2"],[class*="g3"],[class*="g4"],[data-dc-tpl]'), i;
    for(i=0;i<els.length;i++){
      var el=els[i];
      var m=el.getAttribute('data-mbcol');
      if(m && m!=='-'){ if(!el.classList.contains(m)) el.classList.add(m); continue; }
      if(m) continue;
      if(inMockup(el)){ el.setAttribute('data-mbcol','-'); continue; }
      if(el.getBoundingClientRect().width===0) continue;
      var c=classOf(el);
      if(c){ el.classList.add(c); el.setAttribute('data-mbcol',c); }
      else if(getComputedStyle(el).display==='grid') el.setAttribute('data-mbcol','-');
    }
  }

  function apply(){
    style();
    if(window.innerWidth>760) return;
    grids();
    fontFloor();
    tapFloor();
  }

  apply();
  var n=0, iv=setInterval(function(){ apply(); if(++n>80) clearInterval(iv); },150);
  if(window.MutationObserver){
    var busy=0, mo=new MutationObserver(function(){ if(busy) return; busy=1; setTimeout(function(){ busy=0; apply(); },120); });
    try{ mo.observe(document.documentElement,{childList:true,subtree:true}); }catch(e){}
    setTimeout(function(){ try{mo.disconnect();}catch(e){} },15000);
  }
  document.addEventListener('DOMContentLoaded', apply);
  var rt=0;
  window.addEventListener('resize', function(){
    clearTimeout(rt); rt=setTimeout(function(){
      var els=document.querySelectorAll('[data-mbcol],[data-mbfs],[data-mbtap]'), i;
      for(i=0;i<els.length;i++){
        var m=els[i].getAttribute('data-mbcol'); if(m && m!=='-') els[i].classList.remove(m);
        els[i].removeAttribute('data-mbcol'); els[i].removeAttribute('data-mbfs'); els[i].removeAttribute('data-mbtap');
      }
      apply();
    },200);
  });
})();
