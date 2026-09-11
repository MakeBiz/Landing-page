# Часть C2: SSR-блоки (бандл-страницы, калькулятор) и навигация для краулеров на x-dc страницах
import sys, os, re, json, subprocess, html as H
sys.path.insert(0, os.path.dirname(__file__))
from seo_lib import *
from ssr_content import SSR
import ssr as SS
ROOT = sys.argv[1]; os.chdir(ROOT)
STYLE = 'max-width:920px;margin:0 auto;padding:40px 22px;color:#e8eef7;background:#07090d;font-family:system-ui,-apple-system,sans-serif;line-height:1.55'

def cases(lang):
    out = subprocess.check_output(['node', '-e', "const vm=require('vm');const c={window:{}};vm.createContext(c);vm.runInContext(require('fs').readFileSync(process.argv[1],'utf8'),c);console.log(JSON.stringify(c.window.MB_CASES))",
                                   ('en/' if lang == 'en' else '') + 'keysy/cases-data.js']).decode()
    return json.loads(out)
plain = lambda x: re.sub(r'\s+', ' ', H.unescape(re.sub(r'<[^>]+>', '', x or ''))).strip()

def case_list(lang, product=None):
    pre = '/en' if lang == 'en' else ''
    items = [c for c in cases(lang) if not product or product in c.get('products', [])]
    return '<ul>' + ''.join('<li><a href="%s/keysy/%s">%s</a>: %s</li>' % (pre, c['slug'], H.escape(plain(c['title'])), H.escape(plain(c['lead'])[:220])) for c in items) + '</ul>'

def block(f, removable=False):
    lang = 'en' if f.startswith('en/') else 'ru'
    body = SSR[f]
    if '{CASES}' in body: body = body.replace('{CASES}', case_list(lang, 'ai-agents' if 'ai-agents' in f else None))
    nav = '<nav>' + ' '.join('<a href="%s">%s</a>' % (u, H.escape(n)) for u, n in SS.NAV[lang]) + '</nav>'
    inner = body + '\n' + nav + '\n<p>' + SS.FOOT[lang] + '</p>'
    div = '<!--mb-ssr--><div id="mb-ssr" style="%s">\n%s\n</div>' % (STYLE, inner)
    if removable: div += '<script>(function(){var e=document.getElementById("mb-ssr");if(e&&e.parentNode)e.parentNode.removeChild(e);})();</script>'
    return div + '<!--/mb-ssr-->', SS.words(inner)

def strip_old(s):
    s = re.sub(r'<!--mb-ssr-->.*?<!--/mb-ssr-->', '', s, flags=re.S)
    m = re.search(r'<div id="mb-ssr"[^>]*>', s)
    if m:
        e = s.find('</div>', m.end()); assert '<div' not in s[m.end():e], 'nested div in old ssr'
        s = s[:m.start()] + s[e + 6:]
    return s

log = []
for f in ['index.html', 'en/index.html', 'ai-agents.html', 'en/ai-agents.html', 'contacts.html', 'en/contacts.html']:
    s = strip_old(rd(f))
    blk, w = block(f)
    m = re.search(r'<body[^>]*>', s); s = s[:m.end()] + '\n' + blk + s[m.end():]
    wr(f, s); log.append(f'{f}: SSR {w} слов')

# калькулятор: статичная страница, блок в конце body и сразу удаляется скриптом (посетитель видит калькулятор в iframe)
f = 'calculator-agents.html'
s = strip_old(rd(f)); blk, w = block(f, removable=True)
i = s.rfind('</body>'); s = s[:i] + blk + '\n' + s[i:]; wr(f, s); log.append(f'{f}: SSR {w} слов')

# x-dc страницы: ссылки для краулеров (шапку и подвал рисует скрипт), тоже удаляются сразу
for f in ['vector.html', 'en/vector.html', 'vps.html', 'en/vps.html']:
    lang = 'en' if f.startswith('en/') else 'ru'
    s = rd(f)
    s = re.sub(r'<!--mb-ssr-nav-->.*?<!--/mb-ssr-nav-->', '', s, flags=re.S)
    nav = '<nav>' + ' '.join('<a href="%s">%s</a>' % (u, H.escape(n)) for u, n in SS.NAV[lang]) + '</nav>'
    blk = ('<!--mb-ssr-nav--><div id="mb-ssr-nav" style="%s">%s<p>%s</p></div>'
           '<script>(function(){var e=document.getElementById("mb-ssr-nav");if(e&&e.parentNode)e.parentNode.removeChild(e);})();</script><!--/mb-ssr-nav-->') % (STYLE, nav, SS.FOOT[lang])
    i = s.rfind('</body>'); s = s[:i] + blk + '\n' + s[i:]; wr(f, s); log.append(f'{f}: crawler nav')

# /vps: второй H1 превращаем в H2 (на странице должен быть один H1)
for f in ['vps.html']:
    s = rd(f)
    h1s = [m for m in re.finditer(r'<h1\b([^>]*)>(.*?)</h1>', s, re.S)]
    if len(h1s) > 1:
        m = h1s[1]; s = s[:m.start()] + '<h2' + m.group(1) + '>' + m.group(2) + '</h2>' + s[m.end():]
        wr(f, s); log.append(f'{f}: second H1 -> H2 ({re.sub("<[^>]+>","",m.group(2))[:50]})')
print('\n'.join(log))
