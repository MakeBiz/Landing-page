#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Уводит призывы «посчитать» на английской странице AI-агентов в английский калькулятор.

В шаблоне бандла две кнопки вели на /en/contacts: плашка «Agent team - from 6,000 AED»
в первом экране и большая кнопка «Calculate in the calculator» в блоке цены.
Скрипт идемпотентный: повторный запуск ничего не меняет.

    python3 .seo/calc/link_en_calc.py .
"""
import io, os, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
os.chdir(ROOT)
F = 'en/ai-agents.html'
NEW = '/en/calculator-agents'

# (что ищем, сколько раз должно встретиться в исходном состоянии)
PAIRS = [
    # плашка в первом экране
    (r'<a href=\"/en/contacts\" style=\"display:inline-flex;align-items:center;gap:13px;'
     r'background:linear-gradient(90deg,rgba(31,219,109,.13)',
     r'<a href=\"' + NEW + r'\" style=\"display:inline-flex;align-items:center;gap:13px;'
     r'background:linear-gradient(90deg,rgba(31,219,109,.13)'),
]

h = io.open(F, encoding='utf-8').read()
done = []
for old, new in PAIRS:
    if old in h:
        assert h.count(old) == 1, 'ожидалось одно вхождение: %s' % old[:60]
        h = h.replace(old, new, 1); done.append('плашка первого экрана')

# большая кнопка: ищем по тексту внутри
mark = 'Calculate in the calculator'
i = h.find(mark)
if i > 0:
    j = h.rfind('<a href=', 0, i)
    seg = h[j:i]
    if r'/en/contacts' in seg:
        h = h[:j] + seg.replace(r'/en/contacts', NEW, 1) + h[i:]
        done.append('кнопка в блоке цены')

if done:
    io.open(F, 'w', encoding='utf-8').write(h)
    print('%s: %s -> %s' % (F, ', '.join(done), NEW))
else:
    print('%s: уже ведёт на %s' % (F, NEW))
print('ссылок на калькулятор в шаблоне: %d' % h.count(NEW))
