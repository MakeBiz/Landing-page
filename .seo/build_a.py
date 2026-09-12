# Часть A: title/description/og, заголовки EN, описания новостей, viewport, дубли twitter:card
import os
import sys, os, re, json, subprocess
sys.path.insert(0, os.path.dirname(__file__))
from seo_lib import *
from meta_config import META, EN_FIX
ROOT = sys.argv[1]; os.chdir(ROOT)

def tpl_apply_head(s, fn):
    m = tpl_get(s)
    raw = m.group(2); T, pos = json_str_map(raw)
    ha = T.find('>', T.find('<head')) + 1; he = T.find('</head>')
    T2 = fn(T)
    he2 = T2.find('</head>')
    assert T2[:ha] == T[:ha] and T2[he2:] == T[he:], 'fn changed outside head'
    new_raw = raw[:pos[ha]] + jenc(T2[ha:he2]) + raw[pos[he]:]
    assert json.loads(new_raw) == T2
    return s[:m.start(2)] + new_raw + s[m.end(2):]

def set_runtime_title(s, title):
    pat = re.compile(r'(var T=)("(?:[^"\\]|\\.)*")(;function s\(\)\{if\(document\.title!==T\))')
    n = len(pat.findall(s))
    return pat.sub(lambda m: m.group(1) + json.dumps(title) + m.group(3), s), n

def trim_desc(d, limit=160):
    if len(d) <= limit: return d
    parts = re.split(r'(?<=[.!?])\s+', d)
    out = ''
    for p in parts:
        cand = (out + ' ' + p).strip()
        if len(cand) <= limit: out = cand
        else: break
    if len(out) >= 90: return out
    cut = d[:limit - 1].rsplit(' ', 1)[0].rstrip(',;:')
    return cut + '…'

log = []
def head_fn(title, desc):
    def fn(h):
        if title:
            h = set_title(h, title)
            if get_meta(h, 'og:title', 'property') is not None: h = set_meta(h, 'og:title', title, 'property')
        if desc:
            h = set_meta(h, 'description', desc)
            if get_meta(h, 'og:description', 'property') is not None: h = set_meta(h, 'og:description', desc, 'property')
        return h
    return fn

for f, (title, desc) in META.items():
    s = rd(f); o = s
    fn = head_fn(title, desc)
    s = fn(s)
    if tpl_get(s): s = tpl_apply_head(s, fn)
    if title:
        s, n = set_runtime_title(s, title)
        if n: log.append(f'{f}: runtime title x{n}')
    if s != o: wr(f, s); log.append(f'{f}: head updated')

# английские заголовки
for f, pairs in EN_FIX.items():
    s = rd(f); o = s
    tpl_pairs = []
    dec = tpl_decoded(s) or ''
    for old, new in pairs:
        if old.startswith('TPL:'):
            if old[4:] in dec: tpl_pairs.append((old[4:], new))      # уже исправлено: пропускаем
            continue
        if s.count(old) == 0 and new in s: continue
        assert s.count(old) == 1, (f, old[:50], s.count(old))
        s = s.replace(old, new)
    if tpl_pairs: s = tpl_patch(s, tpl_pairs)
    wr(f, s); log.append(f'{f}: EN headings x{len(pairs)}')

# новости: описания до 160 знаков, один twitter:card
news = ([('news/' + f) for f in sorted(os.listdir('news')) if f.endswith('.html')]
        + [('en/news/' + f) for f in sorted(os.listdir('en/news')) if f.endswith('.html')]
        + ['news.html', 'en/news.html'])  # было git ls-files: в папке STAGE нет репозитория
for f in news:
    s = rd(f); o = s
    d = get_meta(s, 'description')
    if d and len(d) > 160:
        nd = trim_desc(d); s = set_meta(s, 'description', nd); log.append(f'{f}: desc {len(d)} -> {len(nd)}')
    tc = get_meta(s, 'twitter:card')
    if tc: s = set_meta(s, 'twitter:card', tc)
    if s != o: wr(f, s)

# viewport во внешнем head ai-agents
s = rd('ai-agents.html')
if get_meta(s, 'viewport') is None:
    s = set_meta(s, 'viewport', 'width=device-width, initial-scale=1'); wr('ai-agents.html', s); log.append('ai-agents.html: viewport')
print('\n'.join(log))
