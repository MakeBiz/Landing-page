"""SEO-файлы нового makebiztechnologies.com: sitemap.xml (RU + EN с hreflang), llms.txt, llms-full.txt (RU) и en/llms-full.txt.
Запуск: python3 make_seo_ae.py <корень сайта> <папка нового сайта, обычно site-v2> [дата YYYY-MM-DD]
Страницы-решения берутся из .seo/uae/link_solutions.py, новости из папок news/ и en/news/"""
import os, re, sys, html, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from en_slugs import en_path
ROOT = os.path.abspath(sys.argv[1])
NEWD = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else ROOT
D = sys.argv[3] if len(sys.argv) > 3 else datetime.date.today().isoformat()
os.environ.setdefault('MB_SITE', ROOT)
from solutions_src import solutions
SITE = 'https://makebiztechnologies.com'
AG = ['rop', 'svyaznoy', 'zvonki', 'hr', 'zakupki', 'marketing', 'finansy']
CASES = ['cdek-b2b', 'unilin-crm', 'haval-vector', 'performia-crm', 'apartika-crm']
NEW = ['/', '/bitrix', '/bitrix-support', '/bitrix-messengers', '/bitrix-integrations', '/bitrix-licenses', '/bitrix-korobka', '/bi-analitika', '/ceny',
       '/ai-agents'] + ['/ai-agents/' + a for a in AG] + ['/keysy'] + ['/keysy/' + c for c in CASES] + ['/vps', '/o-kompanii', '/partners', '/contacts']
from landings_ae_list import LANDINGS_AE
NEW += [x[0] for x in LANDINGS_AE]
PRIO = {'/': '1.0', '/bitrix': '0.9', '/ai-agents': '0.9', '/bitrix-licenses': '0.9', '/bitrix-korobka': '0.8', '/ceny': '0.8'}

def ru_file(p, base=None): return os.path.join(base or NEWD, 'index.html' if p == '/' else p.strip('/') + '.html')
def en_file(p):
    e = en_path(p)
    return os.path.join(NEWD, 'en', 'index.html') if e == '/en' else os.path.join(NEWD, e.strip('/') + '.html')
def mtime(f):
    try: return datetime.date.fromtimestamp(os.path.getmtime(f)).isoformat()
    except OSError: return D
def title_of(f):
    try: return html.unescape(re.search(r'<title>(.*?)</title>', open(f, encoding='utf-8').read(), re.S).group(1)).strip()
    except Exception: return ''
def alt(ru, en):
    a = f'<xhtml:link rel="alternate" hreflang="ru" href="{SITE}{ru}"/>'
    if en: a += f'<xhtml:link rel="alternate" hreflang="en" href="{SITE}{en}"/>'
    return a + f'<xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{ru}"/>'

pairs = []  # (ru_url, en_url|None, ru_file, en_file|None, priority, changefreq)
for p in NEW:
    pr = PRIO.get(p, '0.6' if p.startswith('/keysy/') else '0.8')
    pairs.append((p, en_path(p), ru_file(p), en_file(p), pr, 'monthly'))
SOL = [u for _, _, _, u in solutions('ru')]
for u in SOL:
    if os.path.exists(ru_file(u, ROOT)):
        e = '/en' + u if os.path.exists(os.path.join(ROOT, 'en', u.strip('/') + '.html')) else None
        pairs.append((u, e, ru_file(u, ROOT), os.path.join(ROOT, 'en', u.strip('/') + '.html') if e else None, '0.8', 'monthly'))
pairs.append(('/news', '/en/news' if os.path.exists(os.path.join(ROOT, 'en', 'news.html')) else None, os.path.join(ROOT, 'news.html'), os.path.join(ROOT, 'en', 'news.html'), '0.7', 'weekly'))
NEWS = []
nd = os.path.join(ROOT, 'news')
for f in sorted(os.listdir(nd)) if os.path.isdir(nd) else []:
    if not f.endswith('.html'): continue
    s = f[:-5]; ef = os.path.join(ROOT, 'en', 'news', f)
    pairs.append(('/news/' + s, '/en/news/' + s if os.path.exists(ef) else None, os.path.join(nd, f), ef if os.path.exists(ef) else None, '0.6', 'monthly'))
    NEWS.append((s, os.path.join(nd, f), ef if os.path.exists(ef) else None))
for p in ('/privacy', '/terms'):
    pairs.append((p, '/en' + p, ru_file(p, ROOT), os.path.join(ROOT, 'en', p.strip('/') + '.html'), '0.3', 'yearly'))

out = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
n = 0
for ru, en, fr, fe, pr, cf in pairs:
    if not os.path.exists(fr): continue
    out.append(f'  <url><loc>{SITE}{ru}</loc>{alt(ru, en)}<lastmod>{mtime(fr)}</lastmod><changefreq>{cf}</changefreq><priority>{pr}</priority></url>'); n += 1
    if en and fe and os.path.exists(fe):
        out.append(f'  <url><loc>{SITE}{en}</loc>{alt(ru, en)}<lastmod>{mtime(fe)}</lastmod><changefreq>{cf}</changefreq><priority>{max(float(pr) - 0.1, 0.1):.1f}</priority></url>'); n += 1
sm = '\n'.join(out) + '\n</urlset>\n'
import xml.dom.minidom; xml.dom.minidom.parseString(sm.encode())
open(os.path.join(NEWD, 'sitemap.xml'), 'w', encoding='utf-8').write(sm)

# ---------- llms.txt (английский, как раньше: его читают ассистенты по всему миру)
def U(p): return SITE + en_path(p)
L = ['# MakeBiz Technologies', '',
     '> MakeBiz Technologies (legal entity MakeBiz Technologies FZE LLC) is an IT integrator in the UAE: Bitrix24 CRM implementation and support, AI agents and BI analytics for companies in Dubai and across the Emirates. The website is available in Russian (main version) and English, all prices are in UAE dirhams (AED).', '',
     'Key facts:', '',
     '- Legal entity: MakeBiz Technologies FZE LLC, a free zone company of Ajman NuVentures Centre (UAE), registration number 2624215090888, Amber Gem Tower, Ajman',
     '- Official Bitrix24 partner in the UAE',
     '- Founder: Anton Chernobaev. 8 years in IT and CRM, 150+ implementation projects',
     '- Contacts: WhatsApp and phone +971 50 262 0927, Telegram @Anton_MakeBiz (https://t.me/Anton_MakeBiz), email info@makebiztechnologies.com',
     '- Meetings in Dubai or by video call; languages: English and Russian',
     '- MakeBiz does not provide company formation, visas or trade licenses', '',
     '## Bitrix24', '',
     f'- [Bitrix24 implementation in Dubai and the UAE]({U("/bitrix")}): turnkey CRM setup, pipelines, WhatsApp, 5% VAT invoices, training. Standard CRM setup from AED 10,000, work beyond the standard AED 200 per hour, basic launch from 14 days',
     f'- [Bitrix24 support]({U("/bitrix-support")}): monthly packages of 5, 10 or 20 hours for AED 1,250, 2,300 or 4,200; an hour beyond the package AED 250',
     f'- [WhatsApp and messengers in Bitrix24]({U("/bitrix-messengers")}): official WhatsApp Business Platform, Telegram, social media and website chat; connection AED 500, provider subscription separate',
     f'- [Accounting integrations]({U("/bitrix-integrations")}): Bitrix24 with Zoho Books, QuickBooks, Odoo and 1C, invoices with 5% VAT, payments and stock; from AED 10,000',
     f'- [Bitrix24 prices in the UAE]({U("/bitrix-licenses")}): vendor prices from bitrix24.ae in USD, shown in AED at 3.6725. Cloud billed annually: Basic AED 180 ($49), Standard AED 364 ($99), Professional AED 731 ($199) a month, Enterprise from AED 1,465 ($399). On-premise per year: Business AED 13,184 ($3,590), Enterprise AED 91,776 ($24,990)',
     f'- [On-premise Bitrix24]({U("/bitrix-korobka")}): installation on the client server or in a UAE data center, migration from cloud, customization, support',
     f'- [BI analytics]({U("/bi-analitika")}): management dashboards on CRM, accounting, telephony and ad data; from AED 1,000',
     f'- [Servers and VPS]({U("/vps")}): VPS selection from vetted providers (same list as servercalc.com, including UAE locations), deployment of on-premise Bitrix24 and AI agents, setup AED 200 per hour', '',
     '## AI agents', '',
     f'- [AI agents for business]({U("/ai-agents")}): one agent from AED 5,000; packages Start AED 5,000, Business AED 10,000, Holding priced individually; maintenance 10% of the implementation cost per month; demo free',
     f'- [AI sales head]({U("/ai-agents/rop")}): drafts replies, takes over a chat after 15 minutes of silence, reviews manager chats, tracks the sales plan',
     f'- [Call speech analytics]({U("/ai-agents/zvonki")}): every call scored by your script; AED 1,000 a month for 5,000 minutes, AED 1,700 for 10,000 minutes, from AED 4,000 for 30,000+ minutes',
     f'- [HR agent]({U("/ai-agents/hr")}), [procurement agent]({U("/ai-agents/zakupki")}), [marketing agent]({U("/ai-agents/marketing")}), [finance agent]({U("/ai-agents/finansy")}), [liaison agent]({U("/ai-agents/svyaznoy")})', '']
L += ['## Bitrix24 by task and industry', ''] + [f'- [{t}]({U(p)}): {s}' for p, _, _, t, s in LANDINGS_AE] + ['']
SOL_EN = solutions('en')
if SOL_EN:
    L += ['## Bitrix24 solutions for the UAE', '']
    for e, t, d, u in SOL_EN:
        L.append(f'- [{t}]({SITE}/en{u}): {d}')
    L.append('')
L += ['## Company', '',
      f'- [Pricing in AED]({U("/ceny")})', f'- [Cases]({U("/keysy")}): CDEK, Unilin, HAVAL, Performia, Apartico',
      f'- [Partner program]({U("/partners")}): 20% of the first payment and 10% of payments for 12 months',
      f'- [About]({U("/o-kompanii")})', f'- [Contacts]({U("/contacts")})', f'- [News]({SITE}/en/news)', '',
      '## Russian version', '', f'- Main page in Russian: {SITE}/', f'- Full text of the Russian site: {SITE}/llms-full.txt', f'- Full text of the English site: {SITE}/en/llms-full.txt', '']
if NEWS:
    L += ['## Latest news', '']
    items = sorted(NEWS, key=lambda x: mtime(x[1]), reverse=True)[:20]
    for s, fr, fe in items:
        t = title_of(fe or fr).split(' | ')[0]
        L.append(f'- [{t}]({SITE}{"/en" if fe else ""}/news/{s})')
    L.append('')
open(os.path.join(NEWD, 'llms.txt'), 'w', encoding='utf-8').write('\n'.join(L))

# ---------- llms-full.txt: полный текст новых страниц
from html.parser import HTMLParser
SKIP = {'vis-wrap', 'vis', 'shot', 'hero-shot', 'stats', 'mq', 'crumbs', 'track', 'kfilter', 'rel-sec', 'flt', 'chips', 'cta-row', 'updated', 'more', 'agc', 'yt', 'vid', 'sh-tabs', 'case-more', 'formsec'}
VOID = {'img', 'br', 'input', 'meta', 'link', 'hr', 'source'}
class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.out = []; s.stack = []; s.skip = 0; s.on = False
    def handle_starttag(s, tag, attrs):
        a = dict(attrs)
        if tag == 'main': s.on = True
        if not s.on or tag in VOID: return
        cls = set((a.get('class') or '').split())
        sk = bool(cls & SKIP) or tag in ('script', 'style', 'form', 'svg', 'button')
        s.stack.append((tag, sk))
        if sk: s.skip += 1
        if s.skip: return
        if tag in ('h1', 'h2', 'h3'): s.out.append('\n' + '#' * int(tag[1]) + ' ')
        elif tag == 'summary': s.out.append('\n**')
        elif tag == 'li': s.out.append('\n- ')
        elif tag in ('p', 'div', 'tr', 'section', 'article', 'details', 'figure'): s.out.append('\n')
        elif tag in ('td', 'th'): s.out.append(' | ')
        elif tag in ('small', 'span'): s.out.append(' ')
    def handle_endtag(s, tag):
        if tag == 'main': s.on = False
        if not s.on and tag != 'main': return
        while s.stack:
            t, sk = s.stack.pop()
            if sk: s.skip -= 1
            if t == tag: break
        if s.skip: return
        if tag in ('h1', 'h2', 'h3', 'p', 'div', 'li'): s.out.append('\n')
        elif tag == 'summary': s.out.append('**\n')
        elif tag in ('span', 'b', 'small', 'a', 'em', 'i'): s.out.append(' ')
    def handle_data(s, d):
        if s.on and not s.skip: s.out.append(d)
def md(t):
    pr = P(); pr.feed(t)
    txt = html.unescape(''.join(pr.out))
    lines = [re.sub(r'[ \t]+', ' ', l).strip() for l in txt.split('\n')]
    out, prev = [], None
    for l in lines:
        if not l or l == prev or l in ('#', '##', '###', '-', '**', '****', 'Подробнее →', 'Читать кейс →', 'Выбрать', 'Читать →', 'Learn more →', 'Read the case →', 'Choose'): continue
        out.append(l); prev = l
    return '\n'.join(out)
for EN in (False, True):
    parts = (['# MakeBiz Technologies (makebiztechnologies.com): full text of the English site for AI search', '',
              f'> MakeBiz Technologies FZE LLC: Bitrix24, AI agents and BI analytics for companies in Dubai and the UAE, prices in AED. Short version: {SITE}/llms.txt', '']
             if EN else ['# MakeBiz Technologies (makebiztechnologies.com): полный текст сайта для ИИ-поиска', '',
              f'> MakeBiz Technologies FZE LLC: Битрикс24, ИИ-агенты и BI-аналитика для компаний в Дубае и ОАЭ, цены в AED. Краткая версия: {SITE}/llms.txt', ''])
    for p in NEW:
        f = en_file(p) if EN else ru_file(p)
        if not os.path.exists(f): continue
        t = open(f, encoding='utf-8').read()
        title = html.unescape(re.search(r'<title>(.*?)</title>', t).group(1))
        url = SITE + (en_path(p) if EN else p)
        parts += ['', '---', '', (f'Page: {url}' if EN else f'Страница: {url}'), (f'Title: {title}' if EN else f'Заголовок: {title}'), '', md(t)]
    os.makedirs(os.path.join(NEWD, 'en'), exist_ok=True)
    open(os.path.join(NEWD, 'en' if EN else '', 'llms-full.txt'), 'w', encoding='utf-8').write('\n'.join(parts) + '\n')
print('sitemap.xml %d urls, llms.txt %d lines, llms-full.txt ru+en' % (n, len(L)))
