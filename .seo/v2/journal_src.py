# -*- coding: utf-8 -*-
"""Журнал гайдов makebiztechnologies.com (/journal, /en/journal).
Статьи: .seo/v2/journal/<slug>.json = {slug, date, rubric_ru, rubric_en, ru:{title, desc, h1?, crumb?, lead, answer, body, faq:[[q,a]], cta:[title,text], related:[[url,title]]}, en:{...}}
body: HTML (p, h2, h3, ul, ol, li, b, a, table); маркер <!--cta--> ставит CTA посередине. Внутренние ссылки пишем RU-адресами (/bitrix-licenses, /news/<slug>, /journal/<slug>):
сборщик сам переводит их на EN-адреса через U(). Используют journal_ae.py, journal_ae_en.py и make_seo_ae.py"""
import os, json, re, html as _h
JDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'journal')

def load_journal():
    out = []
    if os.path.isdir(JDIR):
        for f in sorted(os.listdir(JDIR)):
            if f.endswith('.json') and not f.startswith('_'):
                out.append(json.load(open(os.path.join(JDIR, f), encoding='utf-8')))
    out.sort(key=lambda a: (a['date'], a['slug']), reverse=True)
    return out

JOURNAL = load_journal()
MONTHS_RU = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
MONTHS_EN = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
def date_ru(iso):
    y, m, d = iso.split('-'); return f'{int(d)} {MONTHS_RU[int(m) - 1]} {y}'
def date_en(iso):
    y, m, d = iso.split('-'); return f'{int(d)} {MONTHS_EN[int(m) - 1]} {y}'
def plain(s): return re.sub(r'\s+', ' ', _h.unescape(re.sub('<[^>]+>', ' ', s or ''))).strip()
def words(a, lang):
    L = a[lang]
    t = ' '.join([L['lead'], L['answer'], L['body']] + [q + ' ' + x for q, x in L['faq']])
    return len(re.findall(r'\w+', plain(t)))
def read_min(a, lang): return max(3, round(words(a, lang) / 180))
def rubrics(lang):
    out = []
    for a in JOURNAL:
        r = a['rubric_' + lang]
        if r not in out: out.append(r)
    return out
def jpath(slug): return '/journal/' + slug
