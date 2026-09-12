#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Собирает английскую обёртку калькулятора en/calculator-agents.html из русской.

Сама страница это только рама вокруг iframe: шапка, подвал, общие модули и SSR-блок.
Английские версии общих модулей берём с готовых английских страниц, чтобы они не разъезжались.

    python3 .seo/calc/build_calc_en_page.py .
"""
import io, os, re, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
os.chdir(ROOT)

SRC = 'calculator-agents.html'
OUT = 'en/calculator-agents.html'
BASE = 'https://makebiztechnologies.com'

TITLE = 'AI agents cost calculator for business | MakeBiz'
DESC = ('Build your team of AI agents from the catalogue and see the implementation and '
        'support price in AED at once. Start, Business and Holding plans, from AED 6,000.')


def rd(p):
    return io.open(p, encoding='utf-8').read()


def wr(p, s):
    d = os.path.dirname(p)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    io.open(p, 'w', encoding='utf-8').write(s)


SCRIPT_RE = re.compile(r'<script\b[^>]*>.*?</script>', re.S)


def script_with(html, needle):
    for m in SCRIPT_RE.finditer(html):
        if needle in m.group(0):
            return m.group(0)
    raise SystemExit('НЕ НАЙДЕН скрипт с «%s»' % needle)


def swap_script(html, needle, new):
    old = script_with(html, needle)
    return html.replace(old, new, 1)


def block(html, tag):
    m = re.search(r'<%s>.*?</%s>' % (tag, tag), html, re.S)
    if not m:
        raise SystemExit('НЕ НАЙДЕН блок <%s>' % tag)
    return m.group(0)


def main():
    ru = rd(SRC)
    en_plain = rd('en/privacy.html')     # английские общие модули на статичной странице
    en_form = rd('en/bitrix.html')       # английский блок «Discuss a project»

    h = ru

    # 1. общие модули на английские версии
    h = swap_script(h, 'единый фон «Лучи»', script_with(en_plain, 'unified Rays background'))
    h = swap_script(h, 'чистка: убрать', script_with(en_plain, 'чистка (EN-enhanced)'))
    h = swap_script(h, 'универсальный блок «Обсудить проект»',
                    script_with(en_form, 'универсальный блок «Discuss a project»'))

    # 2. шапка и подвал
    h = h.replace(block(ru, 'header'), block(en_plain, 'header'), 1)
    h = h.replace(block(ru, 'footer'), block(en_plain, 'footer'), 1)

    # 3. язык документа
    h = h.replace('<html lang="ru">', '<html lang="en">', 1)

    # 4. head: заголовок, описание, og, canonical, hreflang
    reps = [
        ('<title>Калькулятор стоимости AI-агентов для бизнеса | MakeBiz</title>',
         '<title>%s</title>' % TITLE),
        ('<meta property="og:title" content="Калькулятор стоимости AI-агентов для бизнеса | MakeBiz">',
         '<meta property="og:title" content="%s">' % TITLE),
        ('<meta property="og:url" content="%s/calculator-agents">' % BASE,
         '<meta property="og:url" content="%s/en/calculator-agents">' % BASE),
        ('<meta property="og:locale" content="ru_RU">',
         '<meta property="og:locale" content="en_US">'),
        ('<link rel="canonical" href="%s/calculator-agents">' % BASE,
         '<link rel="canonical" href="%s/en/calculator-agents">' % BASE),
        ('<iframe id="mbcalcframe" src="/calculator-agents-app" title="Калькулятор стоимости AI-агентов"',
         '<iframe id="mbcalcframe" src="/calculator-agents-app?lang=en" title="AI agents cost calculator"'),
        ('<div class="calcback"><a href="/ai-agents">← Вернуться к AI-агентам</a></div>',
         '<div class="calcback"><a href="/en/ai-agents">← Back to AI agents</a></div>'),
    ]
    for a, b in reps:
        if a not in h:
            raise SystemExit('НЕ НАЙДЕНО в исходнике: %s' % a[:80])
        h = h.replace(a, b, 1)

    # описание страницы в двух местах (meta description и og:description)
    h = re.sub(r'(<meta (?:name="description"|property="og:description") content=")[^"]*(">)',
               lambda m: m.group(1) + DESC + m.group(2), h)

    # hreflang: русская и английская версии ссылаются друг на друга, x-default на русскую
    alt = ('  <link rel="alternate" hreflang="ru" href="%s/calculator-agents">\n'
           '  <link rel="alternate" hreflang="en" href="%s/en/calculator-agents">\n'
           '  <link rel="alternate" hreflang="x-default" href="%s/calculator-agents">' % (BASE, BASE, BASE))
    h = re.sub(r'[ \t]*<link rel="alternate"[^>]*>\n?', '', h)
    h = h.replace('<link rel="canonical" href="%s/en/calculator-agents">' % BASE,
                  '<link rel="canonical" href="%s/en/calculator-agents">\n%s' % (BASE, alt), 1)

    # 5. SSR-блок русской страницы убираем: английский положит build_c2
    h = re.sub(r'<!--mb-ssr-->.*?<!--/mb-ssr-->', '', h, flags=re.S)

    wr(OUT, h)

    # то же зеркало прописываем на русской странице
    ru2 = re.sub(r'[ \t]*<link rel="alternate"[^>]*>\n?', '', ru)
    ru2 = ru2.replace('<link rel="canonical" href="%s/calculator-agents">' % BASE,
                      '<link rel="canonical" href="%s/calculator-agents">\n%s' % (BASE, alt), 1)
    if ru2 != ru:
        wr(SRC, ru2)

    # проверка: не осталось ли русских слов вне скриптов и SSR
    body = SCRIPT_RE.sub('', h)
    body = re.sub(r'<style\b[^>]*>.*?</style>', '', body, flags=re.S)
    left = sorted(set(re.findall(r'[А-Яа-яЁё][А-Яа-яЁё -]{3,}', body)))
    print('собрано: %s (%d КБ)' % (OUT, len(h) // 1024))
    print('русский текст в разметке: %s' % (', '.join(left) if left else 'нет'))


if __name__ == '__main__':
    main()
