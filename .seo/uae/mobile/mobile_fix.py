#!/usr/bin/env python3
"""Мобильная версия makebiztechnologies.com: правки исходников. Идемпотентно, повторный запуск безопасен.

1. mb-attr.js: модуль __mbMobile (из mb-mobile.js рядом)
2. /bitrix RU+EN: поле «Что нужно» было неразвёрнутым <sc-raw-select> из экспорта, варианты
   висели текстом без поля; иконки без viewBox; форма на странице не отправляла заявку вообще,
   только показывала «Спасибо»
3. /intdoc RU+EN: .hgrid обнулял боковые отступы .wrap, первый экран прилипал к краю
4. /news RU+EN: блок фильтров липкий, на телефоне занимал 310px экрана при прокрутке
5. /calculator-agents RU+EN: на телефоне iframe во весь рост приложения (20 000px), нижняя
   панель с итогом и окно расчёта уезжали в самый низ. Теперь iframe высотой в экран со своей
   прокруткой, панель итога всегда перед глазами
"""
import os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
os.chdir(ROOT)
done, skipped = [], []

def rd(p): return open(p, encoding='utf-8').read()
def wr(p, s): open(p, 'w', encoding='utf-8').write(s)

def pairs(path, prs, label):
    h = rd(path); n = 0
    for old, new in prs:
        assert old not in new, 'новая строка содержит старую: ' + old[:60]
        if old not in h:
            continue
        h = h.replace(old, new); n += 1
    wr(path, h)
    (done if n else skipped).append('%s %s (%d)' % (path, label, n))
    return h

# ---------- 1. mb-attr.js ----------
MOD = rd(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mb-mobile.js'))
a = rd('mb-attr.js')
START = '\n/* MakeBiz, мобильная раскладка (makebiztechnologies.com).'
if START in a:
    a = a[:a.index(START)]
a = a.rstrip('\n') + '\n' + MOD.rstrip('\n') + '\n'
wr('mb-attr.js', a); done.append('mb-attr.js модуль __mbMobile')

# ---------- 2. /bitrix ----------
BITRIX_SUBMIT = {
 'ru': ('Не удалось отправить автоматически. <a href="%s" target="_blank" rel="noopener" style="color:#4FE07F;text-decoration:underline">Отправьте заявку в WhatsApp</a>, текст уже готов',
        'Заявка с сайта (Битрикс24)', 'Имя', 'Компания', 'Сотрудников', 'Телефон', 'Что нужно', 'Задача'),
 'en': ('Could not send automatically. <a href="%s" target="_blank" rel="noopener" style="color:#4FE07F;text-decoration:underline">Send the request via WhatsApp</a>, the text is ready',
        'Website request (Bitrix24)', 'Name', 'Company', 'Employees', 'Phone', 'Need', 'Task'),
}
OLD_SUBMIT = "if(fbtn)fbtn.addEventListener('click',()=>{const f=root.querySelector('[data-form]'),ok=root.querySelector('[data-success]');if(f&&ok){f.style.display='none';ok.style.display='block';}});"

def new_submit(lang):
    fail, head, n1, n2, n3, n4, n5, n6 = BITRIX_SUBMIT[lang]
    fail_js = fail.replace('"', '\\"') % '"+wa+"'
    return ("if(fbtn)fbtn.addEventListener('click',()=>{const f=root.querySelector('[data-form]'),ok=root.querySelector('[data-success]');if(!f||!ok)return;"
      "const ins=f.querySelectorAll('input'),v=i=>ins[i]?ins[i].value.trim():'',sel=f.querySelector('select'),ta=f.querySelector('textarea');"
      "let bad=0;[0,3].forEach(i=>{if(ins[i]&&!v(i)){ins[i].style.borderColor='#E4384D';bad=1;}});if(bad)return;"
      "const need=sel?sel.value:'',task=ta?ta.value.trim():'';"
      "const p={form:'client',page:'bitrix',from:(new URLSearchParams(location.search).get('from')||''),name:v(0),company:v(1),phone:v(3),telegram:'',method:'"+("Телефон" if lang=='ru' else 'Phone')+"',"
      "automate:["+("'Что нужно: '" if lang=='ru' else "'Need: '")+"+need,v(2)?"+("'Сотрудников: '" if lang=='ru' else "'Employees: '")+"+v(2):'',task].filter(Boolean).join('. '),_gotcha:''};"
      "f.style.display='none';ok.style.display='block';"
      "const fail=()=>{const NL=String.fromCharCode(10);const t=['"+head+"','"+n1+": '+p.name,'"+n4+": '+p.phone,p.company?'"+n2+": '+p.company:'',v(2)?'"+n3+": '+v(2):'',need?'"+n5+": '+need:'',task?'"+("Задача" if lang=='ru' else 'Task')+": '+task:''].filter(Boolean).join(NL);"
      "const wa='https://wa.me/971502620927?text='+encodeURIComponent(t);const q=ok.querySelector('p');if(q)q.innerHTML=\""+fail_js+"\";};"
      "try{fetch('/api/lead',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(p)}).then(r=>{if(!r||!r.ok)throw 0;return r.json();}).then(r=>{if(r&&r.ok===false)throw 0;}).catch(fail);}catch(e){fail();}"
      "});")

for path, lang in (('bitrix.html', 'ru'), ('en/bitrix.html', 'en')):
    h = rd(path)
    n = 0
    if '<sc-raw-select' in h:
        h = re.sub(r'<sc-raw-select style="([^"]*)"( style-focus="[^"]*")?>',
                   lambda m: '<select style="' + m.group(1).rstrip(';') + ';color-scheme:dark;cursor:pointer"' + (m.group(2) or '') + '>', h)
        h = h.replace('</sc-raw-select>', '</select>'); n += 1
    if 'sc-camel-view-box=' in h:
        h = h.replace('sc-camel-view-box=', 'viewBox='); n += 1
    if OLD_SUBMIT in h:
        h = h.replace(OLD_SUBMIT, new_submit(lang)); n += 1
    wr(path, h)
    (done if n else skipped).append('%s select/viewBox/отправка (%d)' % (path, n))

# ---------- 3. /intdoc ----------
for path in ('intdoc.html', 'en/intdoc.html'):
    pairs(path, [('align-items:center;padding:clamp(30px,5vw,58px) 0}',
                  'align-items:center;padding-top:clamp(30px,5vw,58px);padding-bottom:clamp(30px,5vw,58px)}')], 'hero отступы')

# ---------- 4. /news ----------
OLDF = '.filters{position:sticky;top:60px;z-index:60;background:rgba(7,9,13,.92);backdrop-filter:blur(14px);border-bottom:1px solid var(--line);padding:14px 0}'
for path in ('news.html', 'en/news.html'):
    h = rd(path)
    if OLDF in h and '@media(max-width:760px){.filters{position:static' not in h:
        h = h.replace(OLDF, OLDF + '\n@media(max-width:760px){.filters{position:static}}', 1); wr(path, h); done.append(path + ' фильтры не липнут')
    else:
        skipped.append(path + ' фильтры')

# ---------- 5. /calculator-agents ----------
CALC_OLD_JS = """  var wrap=document.getElementById('mbcalcwrap'), fr=document.getElementById('mbcalcframe'), BAR=63;
  window.addEventListener('message',function(e){
    var d=e&&e.data; if(d&&typeof d.mbCalcHeight==='number'){
      var h=Math.max(600,d.mbCalcHeight); fr.style.height=h+'px'; wrap.style.height=(h-BAR)+'px';
    }
  });"""
def calc_new_js(src):
    return """  var wrap=document.getElementById('mbcalcwrap'), fr=document.getElementById('mbcalcframe'), BAR=63;
  /* На телефоне iframe высотой в экран со своей прокруткой: иначе он растягивался на всю длину
     каталога, и панель итога с окном расчёта (position:fixed внутри приложения) уезжали вниз */
  var MOB=window.matchMedia&&matchMedia('(max-width:760px)').matches;
  if(MOB) fr.setAttribute('scrolling','yes');
  if(!fr.getAttribute('src')) fr.setAttribute('src','""" + src + """');
  function fitMob(){ var hd=document.querySelector('header'), top=hd?hd.getBoundingClientRect().height:0;
    var h=Math.max(460,window.innerHeight-top); wrap.style.height=h+'px'; fr.style.height=(h+BAR)+'px'; }
  if(MOB){ fitMob(); window.addEventListener('resize',fitMob); }
  window.addEventListener('message',function(e){
    var d=e&&e.data; if(d&&typeof d.mbCalcHeight==='number'){
      if(MOB){ fitMob(); return; }
      var h=Math.max(600,d.mbCalcHeight); fr.style.height=h+'px'; wrap.style.height=(h-BAR)+'px';
    }
  });"""
CALC_CSS_ANCHOR = '.calcwrap iframe{display:block;width:100%;border:0;margin-top:-63px;height:1400px;background:#07090D}'
CALC_CSS_ADD = '\n@media(max-width:760px){.calcwrap{min-height:0}#mbTop,#mbCkT{bottom:96px!important}}'
for path, src in (('calculator-agents.html', '/calculator-agents-app'), ('en/calculator-agents.html', '/calculator-agents-app?lang=en')):
    h = rd(path); n = 0
    old_tag = ' src="%s" title=' % src
    if old_tag in h:
        h = h.replace('<iframe id="mbcalcframe"' + old_tag, '<iframe id="mbcalcframe" title=', 1); n += 1
    if CALC_OLD_JS in h:
        h = h.replace(CALC_OLD_JS, calc_new_js(src), 1); n += 1
    if CALC_CSS_ANCHOR in h and CALC_CSS_ADD not in h:
        h = h.replace(CALC_CSS_ANCHOR, CALC_CSS_ANCHOR + CALC_CSS_ADD, 1); n += 1
    wr(path, h)
    (done if n else skipped).append('%s калькулятор (%d)' % (path, n))

print('СДЕЛАНО:'); [print('  ' + x) for x in done]
print('БЕЗ ИЗМЕНЕНИЙ:'); [print('  ' + x) for x in skipped]
