window.__mbYM=function(){
  var ID=112503709, SRC='https://mc.yandex.ru/metrika/tag.js?id='+ID, i='ym', m=window;
  m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
  m[i].l=1*new Date();
  m[i](ID,'init',{ssr:true, webvisor:true, clickmap:true, ecommerce:"dataLayer", referrer: document.referrer, url: location.href, accurateTrackBounce:true, trackLinks:true});
  function ensure(){
    try{
      var ss=document.getElementsByTagName('script');
      for(var j=0;j<ss.length;j++){ if(ss[j].src===SRC) return; }
      var k=document.createElement('script'); k.async=1; k.src=SRC;
      (document.head||document.documentElement).appendChild(k);
    }catch(e){}
  }
  ensure();
  var n=0, iv=setInterval(function(){ ensure(); if(++n>20) clearInterval(iv); }, 400);
};
