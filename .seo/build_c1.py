# Часть C1: статические страницы кейсов (+ предзаполненный список кейсов) из снимка движка
import sys, os, re, json
sys.path.insert(0, os.path.dirname(__file__))
from seo_lib import *
ROOT, SNAP = sys.argv[1], sys.argv[2]; os.chdir(ROOT)
S = json.load(open(SNAP))
LOCAL = 'http://127.0.0.1:8766'
fix = lambda x: x.replace(LOCAL, BASE) if isinstance(x, str) else x
made = []
for url, r in S.items():
    en = url.startswith('/en/')
    if r['kind'] == 'case':
        slug = url.rsplit('/', 1)[1]
        tpl = rd('en/keysy/case.html' if en else 'keysy/case.html')
        canon = BASE + url
        h = set_title(tpl, r['title'])
        h = set_meta(h, 'description', r['desc'])
        h = set_meta(h, 'og:title', r['ogt'], 'property'); h = set_meta(h, 'og:description', r['ogd'], 'property')
        h = set_meta(h, 'og:url', canon, 'property'); h = set_meta(h, 'og:type', 'article', 'property')
        h = re.sub(r'\s*<meta name="robots" content="[^"]*">', '', h)
        h = set_canonical(h, canon)
        h = set_hreflang(h, [('ru', BASE + '/keysy/' + slug), ('en', BASE + '/en/keysy/' + slug), ('x-default', BASE + '/keysy/' + slug)])
        ld = ld_script(json.loads(fix(r['ldCase'])), 'mb-ld-case') + ld_script(json.loads(fix(r['ldCrumb'])), 'mb-ld-crumb')
        a, b = head_bounds(h); head = LD_RE.sub('', h[a:b]).rstrip() + '\n' + ld + '\n'; h = h[:a] + head + h[b:]
        assert h.count('<div data-mb-case></div>') == 1
        h = h.replace('<div data-mb-case></div>', '<div data-mb-case>' + fix(r['html']) + '</div>')
        out = ('en/' if en else '') + 'keysy/' + slug + '.html'
        wr(out, h); made.append(out)
    elif r['kind'] == 'hub':
        f = 'en/keysy.html' if en else 'keysy.html'
        h = rd(f)
        h = re.sub(r'<div data-mb-hub>.*?</div><!--/mb-hub-->', '<div data-mb-hub></div>', h, flags=re.S)   # идемпотентно
        assert h.count('<div data-mb-hub></div>') == 1
        h = h.replace('<div data-mb-hub></div>', '<div data-mb-hub>' + fix(r['html']) + '</div><!--/mb-hub-->')
        wr(f, h); made.append(f)
# шаблон-запасной вариант для ещё не отрендеренных кейсов: noindex
for f in ['keysy/case.html', 'en/keysy/case.html']:
    h = rd(f)
    if get_meta(h, 'robots') is None: h = set_meta(h, 'robots', 'noindex, follow'); wr(f, h); made.append(f + ' (noindex)')
print('\n'.join(made))
