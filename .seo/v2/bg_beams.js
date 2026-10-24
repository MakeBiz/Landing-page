
// ===== фон «Лучи» в цветах флага ОАЭ (как на прошлом makebiztechnologies.com): тёмная подложка и мягкие лучи за курсором
;(function(){
  if (window.__mbBeams) return; window.__mbBeams = 1;
  var BG = '#04050A', BEAMS = [[.12,'#16C15A',.15,120,0],[.30,'#EAF1FF',.08,90,1.6],[.48,'#0C7A33',.17,150,3.1],[.68,'#C8102E',.13,110,4.4],[.86,'#16C15A',.12,130,2.2]];
  var c = document.createElement('canvas'); c.id = 'mb-bg'; c.setAttribute('aria-hidden', 'true');
  document.body.insertBefore(c, document.body.firstChild);
  var ctx = c.getContext('2d'), b = {W:1,H:1,mx:.5,my:.4,tx:.5,ty:.4,active:false,af:0,t:0};
  var reduced = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches; if (reduced) b.t = 4.2;
  function rgba(h, a){ var n = parseInt(h.slice(1), 16); return 'rgba(' + ((n>>16)&255) + ',' + ((n>>8)&255) + ',' + (n&255) + ',' + a + ')'; }
  function resize(){ b.W = innerWidth; b.H = innerHeight; var d = 1; c.width = Math.round(b.W*d); c.height = Math.round(b.H*d); ctx.setTransform(d,0,0,d,0,0); }
  var still = (window.matchMedia && matchMedia('(pointer: coarse)').matches) || innerWidth < 960;
  resize(); addEventListener('resize', function(){ resize(); if (still) draw(); });
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
  if (still || reduced) { draw(); return; }
  function frame(now){ if (last != null && now - last < 32) { requestAnimationFrame(frame); return; } if (last == null) last = now; var dt = Math.min((now-last)/1000,.05); last = now; if (!reduced) b.t += dt*.72; b.mx += (b.tx-b.mx)*.14; b.my += (b.ty-b.my)*.14; b.af += ((b.active?1:0)-b.af)*.12; draw(); requestAnimationFrame(frame); }
  requestAnimationFrame(frame);
})();
