/* =====================================================================
   MakeBiz. Движок раздела кейсов. Этот файл править не нужно.
   Он рисует из списка MB_CASES три вещи:
     1) вкладку Кейсы (элемент с атрибутом data-mb-hub),
     2) блок под продуктом (элемент data-mb-block с data-product),
     3) страницу кейса (элемент data-mb-case, берёт кейс из адреса).

   Дополнено под многоязычный сайт MakeBiz (корень RU, /ru, /en):
     - ссылки строятся с языковым префиксом текущего адреса (/, /ru, /en);
     - интерфейс на русском или английском по языку страницы;
     - устойчивый запуск (интервал + наблюдатель), чтобы блок, вставленный
       на страницу продукта позже (на бандле), тоже отрисовался;
     - slug кейса берётся и из адреса /keysy/имя, и из ?c=имя.
   Меняются редко только справочники ниже: сферы и направления (RU и EN).
   ===================================================================== */
(function(){
  'use strict';

  /* ---- язык и префикс пути ---- */
  function prefix(){ var p=location.pathname; if(/^\/en(\/|$)/.test(p))return '/en'; if(/^\/ru(\/|$)/.test(p))return '/ru'; return ''; }
  var PRE = prefix();
  var LANG = (PRE==='/en') ? 'en' : 'ru';
  function u(path){ return PRE + path; }

  /* ---- справочники ---- */
  var SPHERES = {
    ru: [
      ['all','Все'],['prodazhi','Продажи и B2B'],['logistika','Логистика'],
      ['ecom','Интернет-магазины'],['uslugi','Услуги и сервис'],['nedvizhimost','Недвижимость'],
      ['obrazovanie','Образование'],['medicina','Медицина'],['proizvodstvo','Производство и опт']
    ],
    en: [
      ['all','All'],['prodazhi','Sales & B2B'],['logistika','Logistics'],
      ['ecom','E-commerce'],['uslugi','Services'],['nedvizhimost','Real estate'],
      ['obrazovanie','Education'],['medicina','Healthcare'],['proizvodstvo','Manufacturing & wholesale']
    ]
  };
  var PRODUCTS = {
    ru: { 'ai-agents':'AI-агенты', 'crm':'CRM', 'analytics':'Аналитика' },
    en: { 'ai-agents':'AI Agents', 'crm':'CRM', 'analytics':'Analytics' }
  };
  var PRODUCT_ORDER = ['ai-agents','crm','analytics'];

  var SPHERE_LABEL = {}; SPHERES[LANG].forEach(function(s){ SPHERE_LABEL[s[0]] = s[1]; });

  /* ---- строки интерфейса ---- */
  var T = ({
    ru: {
      hubTitle:'Кейсы <b>наших клиентов</b>',
      hubSub:'Реальные проекты по сферам: с какой задачей пришёл клиент, что мы сделали и что изменилось. Отфильтруйте по своей нише и по тому, что внедряли.',
      fSphere:'Сфера деятельности', fProduct:'Что внедряли', allChip:'Все',
      total:'Всего кейсов: ', found:'Найдено: ',
      empty:'По такому фильтру кейсов пока нет. Попробуйте сбросить одну из меток.',
      was:'Было:', now:'Стало:', open:'Открыть кейс →',
      blockTitle:'Кейсы: ', blockTitleAll:'Наши кейсы', fresh:'свежие проекты', allLink:'Все кейсы →',
      back:'← Все кейсы', notFound:'Кейс не найден',
      nfText:'Возможно, ссылка устарела. ', nfLink:'Посмотреть все кейсы',
      lbTask:'Задача', hTask:'С чем пришёл клиент', lbSol:'Что мы сделали', hSol:'Решение',
      lbRes:'Что изменилось', hRes:'Результат', baWas:'Было', baNow:'Стало',
      factsHead:'Кратко о проекте', fClient:'Клиент', fRegion:'Регион',
      fDir:'Что внедряли', fBuilt:'Что построили', fTerm:'Срок',
      keyRes:'Главный результат', discuss:'Обсудить проект', more:'Похожие кейсы',
      qO:'«', qC:'»', titleSuffix:' | Кейсы MakeBiz', ogSuffix:' | MakeBiz',
      crumbHome:'Главная', crumbCases:'Кейсы'
    },
    en: {
      hubTitle:'Client <b>case studies</b>',
      hubSub:'Real projects by industry: the problem the client came with, what we did and what changed. Filter by your niche and by what we implemented.',
      fSphere:'Industry', fProduct:'What we implemented', allChip:'All',
      total:'Total cases: ', found:'Found: ',
      empty:'No cases match this filter yet. Try clearing one of the tags.',
      was:'Before:', now:'After:', open:'Open case →',
      blockTitle:'Cases: ', blockTitleAll:'Our cases', fresh:'recent projects', allLink:'All cases →',
      back:'← All cases', notFound:'Case not found',
      nfText:'This link may be outdated. ', nfLink:'See all cases',
      lbTask:'Task', hTask:'What the client came with', lbSol:'What we did', hSol:'Solution',
      lbRes:'What changed', hRes:'Result', baWas:'Before', baNow:'After',
      factsHead:'Project at a glance', fClient:'Client', fRegion:'Region',
      fDir:'What we implemented', fBuilt:'What we built', fTerm:'Timeline',
      keyRes:'Key result', discuss:'Discuss a project', more:'Similar cases',
      qO:'“', qC:'”', titleSuffix:' | MakeBiz Cases', ogSuffix:' | MakeBiz',
      crumbHome:'Home', crumbCases:'Case studies'
    }
  })[LANG];

  /* ---- утилиты ---- */
  function cases(){ return (window.MB_CASES || []).slice(); }
  function byDateDesc(a,b){ return (b.date||'').localeCompare(a.date||''); }
  function esc(s){ return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
  function plain(s){ return String(s==null?'':s).replace(/<[^>]+>/g,''); }
  function prodLabel(k){ return (PRODUCTS[LANG][k]) || k; }
  function indLabel(k){ return SPHERE_LABEL[k] || k; }
  function prods(c){ return Array.isArray(c.products) ? c.products : (c.product ? [c.product] : []); }
  function prodTags(c){ return prods(c).map(function(k){ return '<span class="mb-prodtag">'+esc(prodLabel(k))+'</span>'; }).join(''); }
  function inds(c){ return Array.isArray(c.ind) ? c.ind : (c.ind ? [c.ind] : []); }
  function indTags(c, cls){ return inds(c).map(function(k){ return '<span class="mb-chip '+cls+'">'+esc(indLabel(k))+'</span>'; }).join(''); }

  /* ---- карточка кейса ---- */
  function card(c){
    var metric = c.metric ? '<div class="metric">'+esc(c.metric)+'</div>' : '<span></span>';
    return '<a class="mb-card" href="'+u('/keysy/'+encodeURIComponent(c.slug))+'">'+
      '<div class="mb-ctop"><span class="mb-tags" style="justify-content:flex-start">'+indTags(c,'n')+'</span>'+
        '<span class="mb-tags">'+prodTags(c)+'</span></div>'+
      '<h4>'+esc(plain(c.title))+'</h4>'+
      '<div class="mb-ba"><div class="li"><i class="r"></i><span><b>'+T.was+'</b> '+esc(c.was)+'</span></div>'+
        '<div class="li"><i class="g"></i><span><b>'+T.now+'</b> '+esc(c.now)+'</span></div></div>'+
      '<div class="mb-cfoot">'+metric+'<span class="go">'+T.open+'</span></div>'+
    '</a>';
  }

  /* ---- вкладка Кейсы: два фильтра плюс сетка ---- */
  function initHub(host){
    var all = cases().sort(byDateDesc);
    var usedInd = {}, usedProd = {};
    all.forEach(function(c){ inds(c).forEach(function(k){ usedInd[k]=true; }); prods(c).forEach(function(p){ usedProd[p]=true; }); });

    var sphereChips = SPHERES[LANG].filter(function(s){ return s[0]==='all' || usedInd[s[0]]; })
      .map(function(s){ return '<span class="mb-fchip'+(s[0]==='all'?' on':'')+'" data-f="'+s[0]+'">'+esc(s[1])+'</span>'; }).join('');
    var prodChips = '<span class="mb-fchip on" data-f="all">'+T.allChip+'</span>' +
      PRODUCT_ORDER.filter(function(k){ return usedProd[k]; })
      .map(function(k){ return '<span class="mb-fchip" data-f="'+k+'">'+esc(prodLabel(k))+'</span>'; }).join('');

    host.innerHTML =
      '<div class="mb-pagehero"><h1>'+T.hubTitle+'</h1>'+
      '<p class="sub">'+T.hubSub+'</p></div>'+
      '<div class="mb-filterlabel">'+T.fSphere+'</div>'+
      '<div class="mb-filterbar" data-dim="ind">'+sphereChips+'</div>'+
      '<div class="mb-filterlabel">'+T.fProduct+'</div>'+
      '<div class="mb-filterbar" data-dim="product">'+prodChips+'</div>'+
      '<div class="mb-fcount"></div>'+
      '<div class="mb-grid"></div>';
    var grid = host.querySelector('.mb-grid');
    var count = host.querySelector('.mb-fcount');
    var state = { ind:'all', product:'all' };

    function draw(){
      var list = all.filter(function(c){
        var okI = state.ind==='all' || inds(c).indexOf(state.ind)>=0;
        var okP = state.product==='all' || prods(c).indexOf(state.product)>=0;
        return okI && okP;
      });
      grid.innerHTML = list.length ? list.map(card).join('') :
        '<div class="mb-empty">'+T.empty+'</div>';
      var both = state.ind==='all' && state.product==='all';
      count.textContent = both ? (T.total+list.length) : (T.found+list.length);
    }
    host.querySelectorAll('.mb-filterbar').forEach(function(bar){
      var dim = bar.getAttribute('data-dim');
      bar.addEventListener('click', function(e){
        var chip = e.target.closest('.mb-fchip'); if(!chip) return;
        bar.querySelectorAll('.mb-fchip').forEach(function(x){ x.classList.toggle('on', x===chip); });
        state[dim] = chip.getAttribute('data-f');
        draw();
      });
    });
    // предустановка фильтра из адреса: /keysy?ind=logistika или /keysy?product=crm
    var q = new URLSearchParams(location.search);
    ['ind','product'].forEach(function(dim){
      var v = q.get(dim); if(!v) return;
      var bar = host.querySelector('.mb-filterbar[data-dim="'+dim+'"]');
      var pre = bar && bar.querySelector('.mb-fchip[data-f="'+v+'"]');
      if(pre){ bar.querySelectorAll('.mb-fchip').forEach(function(x){ x.classList.toggle('on', x===pre); }); state[dim]=v; }
    });
    draw();
  }

  /* ---- блок под продуктом: свежие кейсы по направлению ---- */
  function initBlock(host){
    var slugsAttr = host.getAttribute('data-slugs'), list, head, link;
    if(slugsAttr){
      var bySlug={}; cases().forEach(function(c){ bySlug[c.slug]=c; });
      list = slugsAttr.split(',').map(function(s){ return bySlug[s.trim()]; }).filter(Boolean).slice(0,4);
      head = T.blockTitleAll;
      link = u('/keysy');
    } else {
      var prod = host.getAttribute('data-product');
      list = cases().filter(function(c){ return prods(c).indexOf(prod)>=0; }).sort(byDateDesc).slice(0,4);
      head = T.blockTitle+esc(prodLabel(prod))+' <span>'+T.fresh+'</span>';
      link = u('/keysy?product='+encodeURIComponent(prod));
    }
    if(!list.length){ host.innerHTML=''; return; }
    host.innerHTML =
      '<div class="mb-block-top"><h3>'+head+'</h3>'+
      '<a class="mb-alllink" href="'+link+'">'+T.allLink+'</a></div>'+
      '<div class="mb-mini4">'+list.map(card).join('')+'</div>';
  }

  /* ---- страница кейса ---- */
  function caseSlug(){
    var q = new URLSearchParams(location.search).get('c');
    if(q) return q;
    var m = location.pathname.match(/\/keysy\/([^\/?#]+)\/?$/);
    if(m){ var s=decodeURIComponent(m[1]); if(s && s!=='case.html' && s!=='case') return s; }
    return null;
  }
  function initCase(host){
    var slug = caseSlug();
    var c = cases().filter(function(x){ return x.slug===slug; })[0];
    if(!c){
      host.innerHTML = '<div class="mb-case"><a class="mb-back" href="'+u('/keysy')+'">'+T.back+'</a>'+
        '<h1>'+T.notFound+'</h1><p style="color:var(--mb-mu2);margin-top:12px">'+T.nfText+
        '<a href="'+u('/keysy')+'" style="color:var(--mb-g3)">'+T.nfLink+'</a>.</p></div>';
      return;
    }
    document.title = plain(c.title)+T.titleSuffix;
    setMeta('description', plain(c.lead));
    setMeta('og:title', plain(c.title)+T.ogSuffix, true);
    setMeta('og:description', plain(c.lead), true);
    // Один кейс открывается по двум адресам: /keysy/имя и /keysy/case?c=имя.
    // Канонический адрес всегда чистый, иначе поисковик видит две одинаковые страницы.
    var canon = location.origin + u('/keysy/' + encodeURIComponent(c.slug));
    setMeta('og:url', canon, true);
    setLink('canonical', canon);
    caseLd(c, canon);

    var quote = c.quote ? '<div class="mb-quote"><p>'+T.qO+esc(c.quote.text)+T.qC+'</p>'+
      '<div class="who"><span class="av"></span><span><b>'+esc(c.quote.who)+'</b><span>'+esc(c.quote.org)+'</span></span></div></div>' : '';
    var mine = prods(c);
    var more = cases().filter(function(x){
      return x.slug!==c.slug && prods(x).some(function(p){ return mine.indexOf(p)>=0; });
    }).sort(byDateDesc).slice(0,3);
    var moreBlk = more.length ? '<div class="mb-more"><div class="mt">'+T.more+'</div>'+
      '<div class="mb-grid">'+more.map(card).join('')+'</div></div>' : '';
    var prodNames = mine.map(prodLabel).join(', ');

    host.innerHTML =
      '<div class="mb-case">'+
      '<a class="mb-back" href="'+u('/keysy')+'">'+T.back+'</a>'+
      '<div class="mb-chips">'+indTags(c,'g')+prodTags(c)+'</div>'+
      '<h1>'+c.title+'</h1>'+
      '<div class="mb-two"><div>'+
        '<div class="mb-blk"><div class="mb-lb rr">'+T.lbTask+'</div><h3>'+T.hTask+'</h3><div class="mb-prose"><p>'+esc(c.problem)+'</p></div></div>'+
        '<div class="mb-blk"><div class="mb-lb gg">'+T.lbSol+'</div><h3>'+T.hSol+'</h3><div class="mb-prose"><p>'+esc(c.solution)+'</p></div></div>'+
        '<div class="mb-blk"><div class="mb-lb g3">'+T.lbRes+'</div><h3>'+T.hRes+'</h3><div class="mb-prose"><p>'+c.result+'</p></div>'+
          '<div class="mb-ba2"><div class="c b"><p class="h">'+T.baWas+'</p><p>'+esc(c.was)+'</p></div>'+
          '<div class="c a"><p class="h">'+T.baNow+'</p><p>'+esc(c.now)+'</p></div></div></div>'+
        quote+
      '</div><div>'+
        '<div class="mb-facts"><div class="fh">'+T.factsHead+'</div>'+
          fact(T.fClient, c.client)+fact(T.fRegion, c.region)+fact(T.fDir, prodNames)+
          fact(T.fBuilt, c.built)+fact(T.fTerm, c.term)+
          '<div class="res"><div class="rl">'+T.keyRes+'</div><p>'+esc(c.now)+'.</p></div>'+
          (c.soft ? '<div class="soft">'+c.soft+'</div>' : '')+
          '<a class="mb-btn red" href="'+u('/contacts')+'" style="width:100%;margin-top:16px">'+T.discuss+'</a>'+
        '</div>'+
      '</div></div>'+
      moreBlk+
      '</div>';
  }

  function fact(k,v){ return v ? '<div class="f"><span class="k">'+esc(k)+'</span><span class="v">'+esc(v)+'</span></div>' : ''; }
  /* ---- микроразметка страницы кейса ----
     Страница кейса собирается в браузере, поэтому и разметку для поисковика
     собираем здесь же: описание статьи и цепочку разделов.
     Копия /ru пока не размечается, чтобы не плодить дубли в поиске. */
  function setLd(id, obj){
    var el = document.getElementById(id);
    if(!el){
      el = document.createElement('script');
      el.type = 'application/ld+json';
      el.id = id;
      document.head.appendChild(el);
    }
    el.textContent = JSON.stringify(obj);
  }

  function caseLd(c, canon){
    if(PRE === '/ru') return;
    var site = location.origin;
    var org = site + '/#organization';
    var home = site + (PRE || '/');
    var hub = site + u('/keysy');
    var day = /^\d{4}-\d{2}$/.test(c.date || '') ? c.date + '-01' : (c.date || '');
    var tags = inds(c).map(indLabel).concat(prods(c).map(prodLabel));

    setLd('mb-ld-case', {
      '@context': 'https://schema.org',
      '@type': 'Article',
      '@id': canon + '#article',
      'headline': plain(c.title).slice(0, 110),
      'name': plain(c.title),
      'description': plain(c.lead),
      'url': canon,
      'mainEntityOfPage': { '@type': 'WebPage', '@id': canon },
      'inLanguage': LANG,
      'datePublished': day || undefined,
      'dateModified': day || undefined,
      'image': site + '/favicon.png',
      'keywords': tags.join(', '),
      'author': { '@id': org },
      'publisher': {
        '@type': 'Organization',
        '@id': org,
        'name': 'MakeBiz Group',
        'url': site + '/',
        'logo': { '@type': 'ImageObject', 'url': site + '/favicon.png', 'width': 310, 'height': 310 }
      }
    });

    setLd('mb-ld-crumb', {
      '@context': 'https://schema.org',
      '@type': 'BreadcrumbList',
      '@id': canon + '#breadcrumb',
      'itemListElement': [
        { '@type': 'ListItem', 'position': 1, 'name': T.crumbHome, 'item': home },
        { '@type': 'ListItem', 'position': 2, 'name': T.crumbCases, 'item': hub },
        { '@type': 'ListItem', 'position': 3, 'name': plain(c.title), 'item': canon }
      ]
    });
  }

  function setLink(rel, href){ var el=document.head.querySelector('link[rel="'+rel+'"]'); if(!el){ el=document.createElement('link'); el.setAttribute('rel',rel); document.head.appendChild(el); } el.setAttribute('href', href); }
  function setMeta(name, content, isProp){
    var attr = isProp ? 'property' : 'name';
    var el = document.head.querySelector('meta['+attr+'="'+name+'"]');
    if(!el){ el = document.createElement('meta'); el.setAttribute(attr, name); document.head.appendChild(el); }
    el.setAttribute('content', content);
  }

  /* ---- запуск: идемпотентный, переживает поздний рендер (бандлы) ---- */
  function boot(){
    if(!window.MB_CASES) return;                 // данные ещё не подгрузились
    document.querySelectorAll('[data-mb-hub]:not([data-mb-done])').forEach(function(h){ h.setAttribute('data-mb-done','1'); initHub(h); });
    document.querySelectorAll('[data-mb-block]:not([data-mb-done])').forEach(function(h){ h.setAttribute('data-mb-done','1'); initBlock(h); });
    document.querySelectorAll('[data-mb-case]:not([data-mb-done])').forEach(function(h){ h.setAttribute('data-mb-done','1'); initCase(h); });
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', boot); else boot();
  var n=0, iv=setInterval(function(){ boot(); if(++n>40) clearInterval(iv); }, 300);
  if(window.MutationObserver){ try{ new MutationObserver(boot).observe(document.documentElement,{childList:true,subtree:true}); }catch(e){} }
})();
