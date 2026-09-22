#!/usr/bin/env python3
"""Версия ?v=<sha1[:10]> для /mb-attr.js во всех HTML, включая строки шаблонов бандла.
Без версии посетитель держит старую копию до часа. Запускать после каждой правки mb-attr.js"""
import hashlib, os, re
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
os.chdir(ROOT)
v = hashlib.sha1(open('mb-attr.js', 'rb').read()).hexdigest()[:10]
pat = re.compile(r'(/|\\u002F)mb-attr\.js(\?v=[0-9a-f]+)?(?=\\?")')
n = 0
for dp, dn, fn in os.walk('.'):
    if '_to_delete' in dp or '/.' in dp or dp.startswith('./_'): continue
    for f in fn:
        if not f.endswith('.html'): continue
        p = os.path.join(dp, f); h = open(p, encoding='utf-8').read()
        h2 = pat.sub(lambda m: m.group(1) + 'mb-attr.js?v=' + v, h)
        if h2 != h: open(p, 'w', encoding='utf-8').write(h2); n += 1
print('mb-attr.js v=%s, файлов обновлено: %d' % (v, n))
