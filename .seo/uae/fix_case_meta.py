#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Подтягивает заголовки и описания страниц кейсов под новый текст.

build_c1 печёт эти поля из снимка браузера, а снимок снять нечем (на Маке нет
Playwright). После правки текста кейсов title и description остались старыми,
поэтому берём их прямо со страницы: H1 в заголовок, og:description в описание.

    python3 .seo/uae/fix_case_meta.py .
"""
import glob, html as H, io, os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from seo_lib import set_title, set_meta      # noqa: E402


def trim_desc(d, limit=160):
    # та же логика, что в build_a: импортировать оттуда нельзя, модуль при импорте сам себя запускает
    if len(d) <= limit:
        return d
    out = ''
    for part in re.split(r'(?<=[.!?])\s+', d):
        cand = (out + ' ' + part).strip()
        if len(cand) <= limit:
            out = cand
        else:
            break
    if len(out) >= 90:
        return out
    return d[:limit - 1].rsplit(' ', 1)[0].rstrip(',;:') + '…'

ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
os.chdir(ROOT)


def plain(x):
    return re.sub(r'\s+', ' ', H.unescape(re.sub(r'<[^>]+>', '', x))).strip()


def main():
    done = []
    for f in sorted(glob.glob('keysy/*.html')) + sorted(glob.glob('en/keysy/*.html')):
        if f.endswith('/case.html'):
            continue
        h = io.open(f, encoding='utf-8').read()
        m = re.search(r'<h1[^>]*>(.*?)</h1>', h, re.S)
        ogd = re.search(r'<meta property="og:description" content="([^"]*)"', h)
        if not m or not ogd:
            continue
        title = plain(m.group(1)) + ' | MakeBiz'
        desc = trim_desc(H.unescape(ogd.group(1)))
        o = h
        h = set_title(h, title)
        h = set_meta(h, 'og:title', title, 'property')
        h = set_meta(h, 'description', desc)
        if h != o:
            io.open(f, 'w', encoding='utf-8').write(h)
            done.append('%s -> %s' % (f, title[:60]))
    print('\n'.join(done) if done else 'менять нечего')


if __name__ == '__main__':
    main()
