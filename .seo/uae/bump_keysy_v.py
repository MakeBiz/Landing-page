#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Пересчитывает ?v= у файлов раздела кейсов после правки cases-data.js.

Версия это первые 10 знаков sha1 содержимого файла: пока адрес не поменялся,
браузер держит старую копию в кэше и правка до людей не доходит.

    python3 .seo/uae/bump_keysy_v.py .
"""
import hashlib, io, os, re, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
os.chdir(ROOT)

ASSETS = ['keysy/cases-data.js', 'keysy/cases-engine.js', 'keysy/keysy.css',
          'en/keysy/cases-data.js', 'en/keysy/cases-engine.js', 'en/keysy/keysy.css']


def sha(p):
    return hashlib.sha1(io.open(p, 'rb').read()).hexdigest()[:10]


def html_files():
    out = []
    for root, dirs, fs in os.walk('.'):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('node_modules', 'b')]
        for f in fs:
            if f.endswith('.html'):
                out.append(os.path.relpath(os.path.join(root, f), '.'))
    return sorted(out)


def main():
    want = {}
    for a in ASSETS:
        if os.path.exists(a):
            want[a] = sha(a)
    changed = 0
    for f in html_files():
        h = io.open(f, encoding='utf-8').read()
        o = h
        for a, v in want.items():
            name = a.rsplit('/', 1)[1]
            pre = '/en/keysy/' if a.startswith('en/') else '/keysy/'
            h = re.sub(re.escape(pre + name) + r'\?v=[0-9a-f]+', pre + name + '?v=' + v, h)
        if h != o:
            io.open(f, 'w', encoding='utf-8').write(h)
            changed += 1
    for a, v in sorted(want.items()):
        print('%-28s ?v=%s' % (a, v))
    print('страниц обновлено: %d' % changed)


if __name__ == '__main__':
    main()
