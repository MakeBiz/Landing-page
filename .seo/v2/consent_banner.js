(function(){
  if(window.__mbCookieInit) return; window.__mbCookieInit=1;
  var KEY='mb_consent_v2';
  window.dataLayer=window.dataLayer||[];
  function gtag(){window.dataLayer.push(arguments);}
  if(!window.gtag) window.gtag=gtag;
  gtag('consent','default',{ad_storage:'denied',analytics_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',personalization_storage:'denied',functionality_storage:'granted',security_storage:'granted',wait_for_update:500});
  var EN=/^\/en(\/|$)/.test(location.pathname);
  var PRE=EN?'/en':(/^\/ru(\/|$)/.test(location.pathname)?'/ru':'');
  var T=EN
    ?{t:'We use cookies and analytics (Yandex Metrica and Google services) to improve the site and measure advertising. Accept, or decline non-essential.',a:'Accept',d:'Decline',m:'Privacy Policy',u:PRE+'/privacy#cookie',s:'Cookie settings'}
    :{t:'Мы используем cookie и аналитику (Яндекс.Метрика и сервисы Google), чтобы улучшать сайт и оценивать рекламу. Примите или отклоните необязательные.',a:'Принять',d:'Отклонить',m:'Политика конфиденциальности',u:PRE+'/privacy#cookie',s:'Настройки cookie'};
  function GT(){try{return localStorage.getItem(KEY);}catch(e){return null;}}
  function ST(v){try{localStorage.setItem(KEY,v);}catch(e){}}
  function grant(){
    gtag('consent','update',{ad_storage:'granted',analytics_storage:'granted',ad_user_data:'granted',ad_personalization:'granted',personalization_storage:'granted'});
    window.__mbConsent='granted';
    if(typeof window.__mbYM==='function'){try{window.__mbYM();}catch(e){}}
  }
  function deny(){ gtag('consent','update',{ad_storage:'denied',analytics_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',personalization_storage:'denied'}); window.__mbConsent='denied'; }
  if(GT()==='accepted') grant();
  var ICON='<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 2a10 10 0 1 0 10 10 3 3 0 0 1-3-3 3 3 0 0 1-3-3 3 3 0 0 1-1-2Z"/><circle cx="9" cy="10.5" r="1" fill="currentColor" stroke="none"/><circle cx="13" cy="14" r="1" fill="currentColor" stroke="none"/><circle cx="15.5" cy="9.5" r="1" fill="currentColor" stroke="none"/></svg>';
  var CSS='#mbCk{position:fixed;left:14px;right:14px;bottom:14px;z-index:2147483000;background:#0e1620;color:#eaf1fb;border:1px solid rgba(255,255,255,.14);border-radius:16px;box-shadow:0 14px 44px rgba(0,0,0,.45);font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif}'
   +'#mbCk .i{max-width:1080px;margin:0 auto;padding:15px 20px;display:flex;gap:18px;align-items:center;justify-content:space-between;flex-wrap:wrap}'
   +'#mbCk .x{font-size:13px;line-height:1.5;flex:1;min-width:230px}#mbCk a{color:#7FB0FF;text-decoration:underline}'
   +'#mbCk .z{display:flex;gap:10px;flex:none}#mbCk button{font:600 14px system-ui,sans-serif;padding:10px 22px;border-radius:100px;cursor:pointer;border:1px solid rgba(255,255,255,.22)}'
   +'#mbCkD{background:transparent;color:#cbd6e8}#mbCkA{background:#16C15A;color:#04120a;border-color:#16C15A}'
   +'#mbCkT{position:fixed;left:14px;bottom:14px;z-index:2147482000;width:42px;height:42px;border-radius:50%;border:1px solid rgba(255,255,255,.18);background:#0e1620;color:#eaf1fb;display:flex;align-items:center;justify-content:center;cursor:pointer;box-shadow:0 6px 20px rgba(0,0,0,.35)}';
  function style(){ if(!document.getElementById('mbCkCSS')){var s=document.createElement('style');s.id='mbCkCSS';s.textContent=CSS;(document.head||document.documentElement).appendChild(s);} }
  function done(){var x=document.getElementById('mbCk');if(x&&x.parentNode)x.parentNode.removeChild(x);}
  function banner(){
    if(document.getElementById('mbCk')) return;
    var d=document.createElement('div');d.id='mbCk';
    d.innerHTML='<div class="i"><div class="x">'+T.t+' <a href="'+T.u+'" target="_blank" rel="noopener">'+T.m+'</a></div><div class="z"><button id="mbCkD" type="button">'+T.d+'</button><button id="mbCkA" type="button">'+T.a+'</button></div></div>';
    (document.body||document.documentElement).appendChild(d);
    d.querySelector('#mbCkA').onclick=function(){ST('accepted');grant();done();};
    d.querySelector('#mbCkD').onclick=function(){ST('declined');deny();done();};
  }
  function toggle(){
    if(document.getElementById('mbCkT'))return;
    var b=document.createElement('button');b.id='mbCkT';b.type='button';b.title=T.s;b.setAttribute('aria-label',T.s);b.innerHTML=ICON;
    b.onclick=function(){ if(!document.getElementById('mbCk')) banner(); };
    (document.body||document.documentElement).appendChild(b);
  }
  function ensure(){ style(); if(GT()){ done(); toggle(); } else { banner(); } }
  ensure(); setInterval(ensure,800);
})();
