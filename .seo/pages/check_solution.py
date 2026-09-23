#!/usr/bin/env python3
"""Проверки страницы-решения перед публикацией: JSON-островы парсятся, в видимом тексте нет длинного тире,
title не длиннее 70, description не длиннее 170, страница есть в sitemap, llms.txt и блоке решений на /bitrix.
Запуск из корня сайта: python3 .seo/pages/check_solution.py bitrix-distribution"""
import io, json, re, sys, html as H
slug = sys.argv[1]
bad = 0


def fail(msg):
    global bad
    bad += 1
    print('ОШИБКА', msg)


def islands(path):
    s = io.open(path, encoding='utf-8').read()
    n = 0
    for m in re.finditer(r'<script type="(application/ld\+json|__bundler/[a-z]+)">([\s\S]*?)</script>', s):
        n += 1
        try:
            json.loads(m.group(2))
        except Exception as e:
            fail('%s: %s не парсится: %s' % (path, m.group(1), e))
    return s, n


for path in (slug + '.html', 'en/' + slug + '.html', 'bitrix.html', 'en/bitrix.html'):
    s, n = islands(path)
    print('%-34s JSON-островов %d' % (path, n))
    if path.endswith(slug + '.html'):
        t = H.unescape(re.search(r'<title>(.*?)</title>', s, re.S).group(1))
        d = H.unescape(re.search(r'<meta name="description" content="([^"]*)"', s).group(1))
        if len(t) > 70: fail('%s: title %d > 70' % (path, len(t)))
        if len(d) > 170: fail('%s: description %d > 170' % (path, len(d)))
        main = re.search(r'<main id="mbabout">[\s\S]*?</main>', s).group(0)
        vis = H.unescape(re.sub(r'<[^>]+>', ' ', main))
        for ch in ('—', '–'):
            if ch in vis or ch in t or ch in d: fail('%s: длинное тире %r в видимом тексте' % (path, ch))
        ld = json.loads(re.search(r'<!--mb-ld--><script type="application/ld\+json">([\s\S]*?)</script>', s).group(1))
        types = [g.get('@type') for g in ld['@graph']]
        if 'FAQPage' not in types: fail('%s: нет FAQPage' % path)
        faq = [g for g in ld['@graph'] if g.get('@type') == 'FAQPage']
        for q in (faq[0]['mainEntity'] if faq else []):
            for ch in ('—', '–'):
                if ch in q['name'] or ch in q['acceptedAnswer']['text']: fail('%s: тире в FAQ' % path)
        if 'OpenClaw' in s: fail('%s: слово OpenClaw' % path)
        print('%-34s title %d, description %d, узлы %s' % ('', len(t), len(d), types))
    else:
        if '/%s"' % slug not in s: fail('%s: нет карточки /%s в блоке решений' % (path, slug))
sm = io.open('sitemap.xml', encoding='utf-8').read()
for loc in ('/' + slug, '/en/' + slug):
    if '<loc>https://makebiztechnologies.com%s</loc>' % loc not in sm: fail('sitemap: нет %s' % loc)
ll = io.open('llms.txt', encoding='utf-8').read()
for loc in ('/' + slug + ')', '/en/' + slug + ')'):
    if loc not in ll: fail('llms.txt: нет %s' % loc)
print('Итог:', 'OK' if not bad else 'ошибок %d' % bad)
sys.exit(1 if bad else 0)
