# -*- coding: utf-8 -*-
"""English version of makebiz.life in the new design. Writes <site>/en/...
Run: python3 build_en.py <site_folder>
Same pages and slugs as the Russian site, hreflang pairs ru/en."""
import os, sys, json, html, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
BASE = os.environ.get('MB_BASE', '')
PREVIEW = os.environ.get('MB_PREVIEW', '0') == '1'
OUT = os.path.join(ROOT, os.environ.get('MB_OUT', '.'), 'en')
HERE = os.path.dirname(os.path.abspath(__file__))
# ===== site constants (makebiztechnologies.com, UAE)
SITE = 'https://makebiztechnologies.com'
UPDATED = 'October 23, 2026'
UPDATED_ISO = '2026-10-23'
V = os.environ.get('MB_V', 'a1')
PRICE_DATE = 'October 23, 2026'
PHONE = '+971 50 262 0927'
PHONE_TEL = '+971502620927'
WA = '971502620927'
TG = 'Anton_MakeBiz'
EMAIL = 'info@makebiztechnologies.com'
YM_ID = '112503709'
GA_ID = 'G-YPNHBR4DXK'
LEGAL = 'MakeBiz Technologies FZE LLC · Ajman NuVentures Centre · registration no. 2624215090888 · Amber Gem Tower, Ajman, UAE'
USD_AED = 3.6725
def aed(usd): return f'AED\u00a0{round(usd * USD_AED):,}'
def lic(usd): return aed(usd)
from en_slugs import EN_SLUG, en_path

def U(p):
    """English page address"""
    if p.startswith('/assets') or p.startswith('/img') or p.startswith('/media'): return BASE + p
    if p.startswith('/en'): return BASE + p
    return BASE + en_path(p)
def RU(p): return BASE + (p if p != '/' else '/')
def esc(s): return html.escape(s, quote=True)
def nb(x): return x
def notag(s): return re.sub('<[^>]+>', '', s or '')

BITRIX_MENU = [
    ('/bitrix', 'Bitrix24 implementation', 'CRM, pipelines, processes turnkey'),
    ('/bitrix-support', 'Support', 'Hour packages, administration'),
    ('/bitrix-messengers', 'WhatsApp and messengers', 'WhatsApp, Telegram, social media'),
    ('/bitrix-integrations', 'Accounting integrations', 'Zoho Books, QuickBooks, Odoo, 1C'),
    ('/bitrix-korobka', 'On-premise Bitrix24', 'Implementation on your server'),
    ('/bitrix-licenses', 'Licenses and prices', 'Cloud from AED 180, on-premise from AED 13,184'),
    ('/bi-analitika', 'BI analytics', 'Dashboards for management'),
]
AI_MENU = [
    ('/ai-agents', 'AI agent implementation', 'Agents in sales, finance, procurement'),
    ('/ai-agents/rop', 'AI sales head', 'Chats, plan, error review'),
    ('/ai-agents/svyaznoy', 'Liaison agent', 'Contacts and relationships'),
    ('/ai-agents/zvonki', 'Speech analytics', 'Every call scored'),
    ('/ai-agents/hr', 'HR agent', 'Screening and bot interviews'),
    ('/ai-agents/zakupki', 'Procurement', 'Requests and quote comparison'),
    ('/ai-agents/marketing', 'Marketing agent', 'Content and AI visibility'),
    ('/ai-agents/finansy', 'Finance', 'Company pulse'),
]

def header(active):
    def dd(title, items, key):
        cls = ' is-active' if active.startswith(key) else ''
        links = ''.join(f'<a class="dd-item" href="{U(p)}"><b>{esc(t)}</b><span>{esc(s)}</span></a>' for p, t, s in items)
        return (f'<div class="nav-dd{cls}"><button class="nav-link" type="button" aria-expanded="false">{title}'
                f'<svg width="10" height="10" viewBox="0 0 10 10" aria-hidden="true"><path d="M2 3.5 5 6.5 8 3.5" fill="none" stroke="currentColor" stroke-width="1.6"/></svg></button>'
                f'<div class="dd-panel">{links}</div></div>')
    def a(p, t, key):
        cls = ' is-active' if active == key else ''
        return f'<a class="nav-link{cls}" href="{p}">{t}</a>'
    return f'''<header class="hdr" id="top">
  <div class="wrap hdr-in">
    <a class="logo" href="{U('/')}" aria-label="MakeBiz home"><img src="{U('/img/logo.png')}" width="234" height="80" alt="MakeBiz"></a>
    <nav class="nav" aria-label="Main menu">
      {dd('Bitrix24', BITRIX_MENU, 'bitrix')}
      {dd('AI agents', AI_MENU, 'ai')}
      {a(U('/keysy'), 'Cases', 'keysy')}
      {a(U('/en/news'), 'News', 'news')}
      {a(U('/partners'), 'Partners', 'partners')}
      {a(U('/contacts'), 'Contacts', 'contacts')}
    </nav>
    <div class="hdr-right">
      <div class="lang" role="group" aria-label="Site language"><svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M3 12h18M12 3c2.6 2.6 3.8 5.6 3.8 9s-1.2 6.4-3.8 9c-2.6-2.6-3.8-5.6-3.8-9S9.4 5.6 12 3z" fill="none" stroke="currentColor" stroke-width="1.8"/></svg><a href="/" hreflang="ru" lang="ru" title="Русская версия">RU</a><span class="on" aria-current="true">EN</span></div>
      <a class="hdr-phone" href="tel:{PHONE_TEL}">{PHONE}</a>
      <a class="btn btn-sm" href="#form">Discuss a project</a>
      <button class="burger" type="button" aria-label="Open menu" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
  <div class="mnav" hidden>
    <div class="mnav-group"><div class="mnav-t">Bitrix24</div>{''.join(f'<a href="{U(p)}">{esc(t)}</a>' for p,t,_ in BITRIX_MENU)}</div>
    <div class="mnav-group"><div class="mnav-t">AI agents</div>{''.join(f'<a href="{U(p)}">{esc(t)}</a>' for p,t,_ in AI_MENU)}</div>
    <div class="mnav-group"><a href="{U('/ceny')}">Pricing</a><a href="{U('/keysy')}">Cases</a><a href="{U('/en/news')}">News</a><a href="{U('/partners')}">Partners</a><a href="{U('/o-kompanii')}">About</a><a href="{U('/contacts')}">Contacts</a><a href="https://wa.me/{WA}">WhatsApp</a><a href="{RU('/')}" lang="ru">Русская версия</a><a href="tel:{PHONE_TEL}">{PHONE}</a></div>
  </div>
</header>'''

def footer():
    return f'''<footer class="ftr">
  <div class="wrap ftr-grid">
    <div class="ftr-brand">
      <a class="logo" href="{U('/')}"><img src="{U('/img/logo.png')}" width="234" height="80" alt="MakeBiz"></a>
      <p>We implement Bitrix24 and AI agents for companies in Dubai and across the Emirates. 8 years in IT, we work in English and Russian</p>
      <p class="ftr-contacts"><a href="tel:{PHONE_TEL}">{PHONE}</a><br><a href="https://wa.me/{WA}">WhatsApp</a> · <a href="https://t.me/{TG}">Telegram @{TG}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
    </div>
    <div><div class="ftr-t">Bitrix24</div>{''.join(f'<a href="{U(p)}">{esc(t)}</a>' for p,t,_ in BITRIX_MENU)}</div>
    <div><div class="ftr-t">AI agents</div><a href="{U('/ai-agents')}">AI agent implementation</a><a href="{U('/ai-agents/rop')}">AI sales head</a><a href="{U('/ai-agents/zvonki')}">Speech analytics</a><a href="{U('/ai-agents/hr')}">HR agent</a><a href="{U('/ai-agents/marketing')}">Marketing agent</a></div>
    <div><div class="ftr-t">Company</div><a href="{U('/o-kompanii')}">About</a><a href="{U('/ceny')}">Pricing</a><a href="{U('/keysy')}">Cases</a><a href="{U('/en/news')}">News</a><a href="{U('/partners')}">Partners</a><a href="https://t.me/makebizchannel">Telegram channel</a><a href="{U('/contacts')}">Contacts</a><a href="{RU('/')}" lang="ru">Русская версия</a></div>
  </div>
  <div class="wrap ftr-legal">
    <span>{LEGAL}</span>
    <span><a href="/en/privacy">Privacy policy</a> · <a href="/en/terms">Terms of use</a> · © 2026 MakeBiz</span>
  </div>
</footer>
<div class="mbar"><a href="tel:{PHONE_TEL}">Call</a><a href="https://wa.me/{WA}">WhatsApp</a><a class="mbar-cta" href="#form">Request</a></div>'''

def crumbs(items):
    parts = [f'<a href="{h}">{esc(t)}</a>' if h else f'<span aria-current="page">{esc(t)}</span>' for h, t in items]
    return '<nav class="crumbs wrap" aria-label="Breadcrumbs">' + '<i>/</i>'.join(parts) + '</nav>'

def hero(eyebrow, h1, lead, answer, cta, cta2, img, chips, alt):
    chips_html = ''.join(f'<li><b>{esc(a)}</b><span>{esc(b)}</span></li>' for a, b in chips)
    c2 = f'<a class="btn btn-ghost" href="{cta2[0]}">{esc(cta2[1])}</a>' if cta2 else ''
    return f'''<section class="hero">
  <div class="wrap hero-grid">
    <div class="hero-text">
      <span class="eyebrow">{esc(eyebrow)}</span>
      <h1>{h1}</h1>
      <p class="lead">{lead}</p>
      <p class="answer">{answer}</p>
      <div class="cta-row"><a class="btn" href="{cta[0]}">{esc(cta[1])}</a>{c2}</div>
      <p class="updated">Updated {UPDATED}</p>
    </div>
    {img}
  </div>
  <div class="wrap"><ul class="chips">{chips_html}</ul></div>
</section>'''

def section(title, sub='', body='', id_='', tone=''):
    idattr = f' id="{id_}"' if id_ else ''
    cls = 'sec' + (' ' + tone if tone else '')
    sub_html = f'<p class="sec-sub">{sub}</p>' if sub else ''
    return f'<section class="{cls}"{idattr}><div class="wrap"><h2>{title}</h2>{sub_html}{body}</div></section>'

def cards(items, cols=3, numbered=False):
    out = []
    for i, it in enumerate(items, 1):
        tag = f'<span class="num">{i:02d}</span>' if numbered else ''
        out.append(f'<div class="card">{tag}<h3>{esc(it[0])}</h3><p>{it[1]}</p></div>')
    return f'<div class="grid g{cols}">' + ''.join(out) + '</div>'

def steps(items):
    out = ''.join(f'<li><span class="step-n">{i}</span><h3>{esc(t)}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(items, 1))
    return f'<div class="track"><i></i></div><ol class="steps">{out}</ol>'

def prices(items, note=''):
    out = []
    for name, price, unit, lines, hot in items:
        li = ''.join(f'<li>{esc(x)}</li>' for x in lines)
        out.append(f'<div class="price{" is-hot" if hot else ""}"><div class="price-name">{esc(name)}</div>'
                   f'<div class="price-val">{price}</div><div class="price-unit">{esc(unit)}</div><ul>{li}</ul>'
                   f'<a class="btn {"" if hot else "btn-ghost"}" href="#form">Choose</a></div>')
    n = f'<p class="note">{note}</p>' if note else ''
    return f'<div class="grid g{min(len(items),4)} prices">' + ''.join(out) + '</div>' + n

# ---------- cases (English data from en/keysy/cases-data.js)
CASEJ = json.load(open(os.path.join(HERE, 'data', 'cases_en.json'), encoding='utf-8'))
SPHERES = [('prodazhi', 'Sales and B2B'), ('logistika', 'Logistics'), ('avto', 'Automotive'), ('ecom', 'E-commerce'), ('uslugi', 'Services'),
           ('nedvizhimost', 'Real estate'), ('obrazovanie', 'Education'), ('medicina', 'Healthcare'), ('proizvodstvo', 'Manufacturing and wholesale')]
SPH = dict(SPHERES)
PRODS = [('crm', 'Bitrix24 and CRM'), ('ai-agents', 'AI agents'), ('analytics', 'BI and analytics')]
PRD = dict(PRODS)
IND_FIX = {'haval-vector': ['avto', 'prodazhi']}
CASE_METRIC = {'haval-vector': ('300,000+', 'call minutes a month'), 'apartika-crm': ('1,000+', 'properties in one CRM'),
               'cdek-b2b': ('5', 'AI agents at work'), 'unilin-crm': ('4', 'BI analytics views'), 'performia-crm': ('110', 'working days to launch')}
for c in CASEJ:
    if c['slug'] in IND_FIX: c['ind'] = IND_FIX[c['slug']]
    if c['slug'] in CASE_METRIC: c['metric_v'], c['metric_t'] = CASE_METRIC[c['slug']]
    for k, v in list(c.items()):
        if isinstance(v, str):
            c[k] = v.replace('Vector speech analytics', 'speech analytics').replace('Vector checks', 'the system checks').replace('<b>Vector</b>', 'speech analytics').replace('Vector', 'speech analytics')
CJ = {c['slug']: c for c in CASEJ}
def case_card(c):
    org = c['client'].split(',')[0]
    tags = ' · '.join([SPH.get(i, i) for i in c['ind'][:2]] + [PRD.get(p, p) for p in c['products']])
    return (f'<a class="case tilt" href="{U("/keysy/" + c["slug"])}" data-ind="{" ".join(c["ind"])}" data-prod="{" ".join(c["products"])}">'
            f'<div class="case-org">{esc(org)}</div>' + (f'<div class="case-metric"><b>{esc(c["metric_v"])}</b><span>{esc(c["metric_t"])}</span></div>' if c.get("metric_v") else '')
            + f'<h3>{esc(notag(c["title"]).split(":", 1)[-1].strip())}</h3>'
            f'<div class="case-ba"><p><span>Before</span>{esc(c["was"])}</p><p><span>After</span>{esc(c["now"])}</p></div>'
            f'<div class="case-tags">{esc(tags)}</div><span class="case-more">Read the case →</span></a>')
def case_cards(slugs):
    return '<div class="grid g3 cases">' + ''.join(case_card(CJ[s]) for s in slugs if s in CJ) + '</div>'

def contract_block():
    items = [
        ('Under contract', 'Contract with MakeBiz Technologies FZE LLC, invoices in dirhams, payment to a UAE company account. We can send the draft contract before the call'),
        ('Fixed estimate', 'Standard work at list price, complex work after a short survey: you see the scope and price before we start'),
        ('Access and data stay yours', 'Portal, server and accounts belong to your company. We work under a separate account and close access at the end'),
        ('One team', 'Implementation, support, integrations and AI agents by one team, no need to gather contractors'),
    ]
    return section('Contract and guarantees', 'What you get besides the work itself', cards(items, 4), tone='tint')

def faq(items):
    out = ''.join(f'<details><summary>{esc(q)}</summary><p>{a}</p></details>' for q, a in items)
    return section('Questions and answers', '', f'<div class="faq">{out}</div>', id_='faq')

def form_block(page, title='Let us discuss your project', sub='Leave a contact and we reply within a business day. We run a short diagnostic and tell you where to start'):
    return f'''<section class="sec formsec" id="form"><div class="wrap form-grid">
  <div class="form-text"><h2>{esc(title)}</h2><p class="sec-sub">{esc(sub)}</p>
    <ul class="form-direct"><li><a href="https://wa.me/{WA}">WhatsApp {PHONE}</a></li><li><a href="https://t.me/{TG}">Telegram @{TG}</a></li><li><a href="tel:{PHONE_TEL}">{PHONE}</a></li></ul></div>
  <form class="lead-form" data-page="en-{esc(page)}" novalidate>
    <label>Name<input name="name" autocomplete="name" required></label>
    <label>Phone or Telegram<input name="phone" autocomplete="tel" required placeholder="+971 ... or @username"></label>
    <label>Task<textarea name="comment" rows="3" placeholder="Briefly: what needs to be done"></textarea></label>
    <input class="hp" name="_gotcha" tabindex="-1" autocomplete="off" aria-hidden="true">
    <button class="btn btn-wide" type="submit">Send request</button>
    <p class="form-note">By clicking the button you agree to the <a href="/en/privacy">privacy policy</a></p>
    <p class="form-ok" hidden>Thank you! Request received, we will contact you soon</p>
    <p class="form-err" hidden>Could not send. Message us on <a href="https://wa.me/{WA}">WhatsApp</a></p>
  </form>
</div></section>'''

def crosslink(to):
    if to == 'ai':
        return section('Second direction: AI agents', 'Once the CRM is set up, the next step is removing routine. Agents work inside Bitrix24, WhatsApp and Telegram',
            f'<div class="cross"><div><h3>AI agents for sales, finance and procurement</h3><p>They answer clients on WhatsApp, review calls, watch the pipeline and the money. One agent from AED 5,000</p></div><a class="btn" href="{U("/ai-agents")}">See AI agents</a></div>', tone='dark')
    return section('Second direction: Bitrix24', 'Agents work better when processes live in a CRM',
        f'<div class="cross"><div><h3>Bitrix24 implementation and support</h3><p>CRM, pipelines, WhatsApp, accounting integrations, licenses and BI analytics. Standard setup from AED 10,000</p></div><a class="btn" href="{U("/bitrix")}">See Bitrix24</a></div>', tone='dark')

ORG = {
    "@type": ["Organization", "ProfessionalService"], "@id": SITE + "/#organization", "name": "MakeBiz", "alternateName": "MakeBiz Technologies",
    "legalName": "MakeBiz Technologies FZE LLC", "url": SITE + "/", "logo": SITE + "/favicon.png", "image": SITE + "/og-image.jpg",
    "telephone": PHONE_TEL, "email": EMAIL, "priceRange": "AED",
    "address": {"@type": "PostalAddress", "streetAddress": "Amber Gem Tower, Sheikh Khalifa Street", "addressLocality": "Ajman", "addressCountry": "AE"},
    "identifier": {"@type": "PropertyValue", "propertyID": "Ajman NuVentures Centre registration number", "value": "2624215090888"},
    "areaServed": [{"@type": "City", "name": "Dubai"}, {"@type": "Country", "name": "United Arab Emirates"}],
    "knowsLanguage": ["en", "ru"],
    "founder": {"@type": "Person", "@id": SITE + "/#founder", "name": "Anton Chernobaev"},
    "knowsAbout": ["Bitrix24", "CRM implementation in the UAE", "on-premise Bitrix24", "Bitrix24 and Zoho Books integration", "WhatsApp in CRM", "VAT in CRM", "BI analytics", "AI agents", "call speech analytics"],
    "disambiguatingDescription": "IT integrator: Bitrix24, AI agents and BI. Does not provide company formation, visas or trade licenses",
    "sameAs": ["https://t.me/makebizchannel", "https://makebiz.life/"],
}

COUNTERS = ('<script defer src="https://makebiz-makebiz-platform-3628.twc1.net/px/t.js" data-site="makebiz-com" data-endpoint="https://makebiz-makebiz-platform-3628.twc1.net/px"></script>\n'
            '<script>' + open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'consent_ym.js'), encoding='utf-8').read() + '</script>\n'
            '<script>' + open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'consent_banner.js'), encoding='utf-8').read() + '</script>\n'
            '<script async src="https://www.googletagmanager.com/gtag/js?id=' + GA_ID + '"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag(\'js\',new Date());gtag(\'config\',\'' + GA_ID + '\');</script>')

def hreflang(path):
    ru = SITE + (path if path != '/' else '/')
    en = SITE + en_path(path)
    return (f'\n<link rel="alternate" hreflang="ru" href="{ru}"><link rel="alternate" hreflang="en" href="{en}">'
            f'<link rel="alternate" hreflang="x-default" href="{ru}">')

def page(path, slug, title, desc, active, body, ld_extra, crumb_items, faq_items=None):
    canon = SITE + en_path(path)
    graph = [ORG, {"@type": "WebPage", "@id": canon + "#webpage", "url": canon, "name": title, "description": desc,
                   "inLanguage": "en", "dateModified": UPDATED_ISO, "isPartOf": {"@id": SITE + "/en#website"},
                   "publisher": {"@id": SITE + "/#organization"}}]
    if crumb_items:
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": t, "item": SITE + en_path(p)} for i, (p, t) in enumerate(crumb_items)]})
    if faq_items:
        graph.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": notag(a)}} for q, a in faq_items]})
    graph += ld_extra
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False).replace('</', '<\\/')
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="{'noindex, nofollow' if PREVIEW else 'index, follow, max-image-preview:large'}">
<link rel="canonical" href="{canon}">{hreflang(path)}
<meta property="og:type" content="website"><meta property="og:locale" content="en_US"><meta property="og:locale:alternate" content="ru_RU"><meta property="og:site_name" content="MakeBiz">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{canon}"><meta property="og:image" content="{SITE}/img/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="icon" href="/favicon-32.png" sizes="32x32"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="{U('/assets/onest-latin.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{U('/assets/site.css')}?v={V}">
<meta name="theme-color" content="#04050A">
<script type="application/ld+json">{ld}</script>
{'' if PREVIEW else COUNTERS}
</head>
<body data-page="en-{slug}"><div class="flag" aria-hidden="true"><i></i><i></i><i></i></div>
{'<div class="pv">Preview of the new site · hidden from search engines · <a href="/en">current site</a></div>' if PREVIEW else ''}
{header(active)}
<main>
{crumbs([(U(p) if p != crumb_items[-1][0] else None, t) for p, t in crumb_items]) if crumb_items and len(crumb_items) > 1 else ''}
{body}
</main>
{footer()}
<script src="{U('/assets/site-en.js')}?v={V}" defer></script>
</body>
</html>'''
    doc = doc.replace('<a href="/" hreflang="ru"', '<a href="' + RU(path) + '" hreflang="ru"', 1)
    if BASE:
        for a_ in ('src="/img/', 'data-src="/img/', 'poster="/media/', 'src="/media/'):
            doc = doc.replace(a_, a_.replace('="/', '="' + BASE + '/'))
    ep = en_path(path)[3:] or '/'
    if ep == '/': fn = 'index.html'
    else: fn = ep.strip('/') + '.html'
    os.makedirs(os.path.dirname(os.path.join(OUT, fn)), exist_ok=True)
    open(os.path.join(OUT, fn), 'w', encoding='utf-8').write(doc)
    built.append(en_path(path))
    return fn

def service_ld(name, desc, url, price=None):
    s = {"@type": "Service", "name": name, "description": desc, "url": SITE + en_path(url), "provider": {"@id": SITE + "/#organization"},
         "areaServed": {"@type": "Country", "name": "United Arab Emirates"}, "serviceType": name, "inLanguage": "en"}
    if price: s["offers"] = {"@type": "Offer", "price": str(price), "priceCurrency": "AED", "url": SITE + en_path(url)}
    return s

# ---------- hero panels (same markup and animations as RU; text comes from site-en.js)
def VIS(kind, top_left, top_right, body, f1=None, f2=None):
    fl = ''
    if f1: fl += f'<div class="flt f1"><small>{esc(f1[0])}</small><b>{esc(f1[1])}</b></div>'
    if f2: fl += f'<div class="flt f2"><small>{esc(f2[0])}</small><b>{esc(f2[1])}</b></div>'
    return (f'<div class="vis-wrap"><div class="vis" data-vis="{kind}"><div class="vis-top"><span class="live">{esc(top_left)}</span><span>{top_right}</span></div>'
            f'<div class="vis-body">{body}</div><span class="vis-note">demo data</span></div>{fl}</div>')
V_BOARD = VIS('board', 'Bitrix24 · live pipeline', 'Deals in progress <b data-cnt>24</b>',
    '<div class="cols"><div class="col"><h4>New</h4></div><div class="col"><h4>Qualified</h4></div><div class="col"><h4>Quote sent</h4></div><div class="col"><h4>Paid ✓</h4></div></div>',
    ('Deal from WhatsApp', 'created in 2 sec'), ('Invoice with 5% VAT', 'paid ✓'))
V_TICKETS = VIS('tickets', 'Bitrix24 support', 'Solved this month <b data-cnt>128</b>', '<div class="rows"></div>',
    ('Reply to a request', 'within a day'), ('10-hour package', 'AED 2,300'))
V_CHAT = VIS('chat', 'Messengers in Bitrix24', 'Channels <b>5</b>',
    '<div class="deal"><div class="deal-h"><b>Deal: Al Noor Trading LLC</b><span>stage “New”</span></div><div class="msgs"></div></div>',
    ('New message', 'deal created'), ('Conversation', 'in the client card'))
V_SYNC = VIS('sync', 'Bitrix24 ↔ Zoho Books exchange', 'Documents <b data-cnt>1,240</b>',
    '<div class="sync"><div class="sys"><h4>Bitrix24</h4><div class="it">Deal · Al Noor</div><div class="it">Company · Palm Supply</div><div class="it">Invoice INV-418</div><div class="it">Products and prices</div><div class="it">Payment received</div></div>'
    '<div class="pipe"><span class="pk"></span><span class="pk b"></span></div>'
    '<div class="sys"><h4>Zoho Books</h4><div class="it">Customer</div><div class="it">TRN and 5% VAT</div><div class="it">Invoice INV-418</div><div class="it">Stock</div><div class="it">Payment</div></div></div>',
    ('Double entry', 'no longer needed'), ('Payment in accounting', 'moved the deal'))
V_LIC = VIS('license', 'Bitrix24 licenses', 'a month <b>AED</b>',
    f'<div class="tiers"><div class="tier"><span><b>Basic</b><small>5 users</small></span><span class="us">{lic(49)}</span></div>'
    f'<div class="tier"><span><b>Standard</b><small>50 users</small></span><span class="us">{lic(99)}</span></div>'
    f'<div class="tier"><span><b>Professional</b><small>100 users</small></span><span class="us">{lic(199)}</span></div>'
    f'<div class="tier"><span><b>On-premise</b><small>your server, a year</small></span><span class="us">{lic(3590)}</span></div></div>',
    ('Prices', 'bitrix24.ae'), ('Renewal', 'without downtime'))
V_BOX = VIS('license', 'Bitrix24 · your server', 'License <b>✓</b>',
    f'<div class="tiers"><div class="tier"><span><b>Business</b><small>50 users</small></span><span class="us">{lic(3590)}</span></div>'
    '<div class="tier"><span><b>Business</b><small>100, 250, 500</small></span><span class="us">on request</span></div>'
    f'<div class="tier"><span><b>Enterprise</b><small>from 1,000 users</small></span><span class="us">{lic(24990)}</span></div>'
    '<div class="tier"><span><b>Server</b><small>yours or in the UAE</small></span><span class="us">turnkey</span></div></div>',
    ('Server', 'your data center'), ('Data', 'inside your perimeter'))
V_BI = VIS('bi', 'Management dashboard', 'Updated <b>now</b>',
    '<div class="kpis"><div class="kpi"><small>Revenue, K AED</small><b data-to="860">0</b></div><div class="kpi"><small>Conversion</small><b data-to="23" data-suf="%">0</b></div><div class="kpi"><small>Deals</small><b data-to="148">0</b></div></div>'
    '<div class="chart"><svg viewBox="0 0 400 190" preserveAspectRatio="none"><defs><linearGradient id="ga" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7FA0FF"/><stop offset="1" stop-color="#7FA0FF" stop-opacity="0"/></linearGradient></defs>'
    + ''.join(f'<rect class="bar" x="{18+i*38}" y="{190-h}" width="22" height="{h}" rx="5" style="animation-delay:{i*0.15:.2f}s"/>' for i, h in enumerate([60, 80, 70, 105, 95, 130, 120, 150, 165, 175]))
    + '<path class="ar" d="M0 160 C60 150 90 120 140 118 S220 90 260 70 S340 40 400 25 L400 190 L0 190Z"/><path class="ln" d="M0 160 C60 150 90 120 140 118 S220 90 260 70 S340 40 400 25"/></svg></div>',
    ('Monthly plan', '104% done'), ('Source', 'CRM + accounting + ads'))
V_AGENTS = VIS('agents', 'AI agents · working', 'Agents <b>7</b>', '<span class="core"></span><div class="rows" style="margin-right:84px"></div>',
    ('Reply to a client', 'in 12 sec'), ('Working', '24/7'))

# ---------- dashboard screenshots (Russian interface, demo data)
SHOT_ALT = {
 'ai-chat': 'Chats: sales head hint and a ready reply from the AI agent',
 'rop-razbor': 'Chat review: where the manager went wrong and what to do',
 'rop-plan': 'Sales: monthly plan, leads, deals and payments by manager',
 'bi-sales': 'Sales department: leads, payments, touches and reply speed',
 'bi-puls': 'Company pulse: revenue, profit, costs and assets by line of business',
 'bi-fin': 'Finance: turnover, profit, margin and cash runway',
 'bi-direct': 'Marketing: spend, clicks and cost per click by ad campaign',
 'mk-search': 'Search: impressions and clicks in search engines for each site',
 'mk-seo': 'SEO by site: pages in search, impressions, clicks and new pages',
 'mk-geo': 'AI visibility: how often ChatGPT, Perplexity and other assistants cite the site',
 'mk-queries': 'Ads: search queries, spend, clicks and cost per click',
 'hr-obzor': 'Hiring: job board responses, bot sessions, average score and hires',
 'hr-kand': 'Hiring: candidates with bot score, motivation type and decision',
 'hr-tests': 'Hiring: bot tests, score distribution and match with manager decisions',
 'calls-analytics': 'Calls: top client questions and top objections',
 'calls-pok': 'Calls: average conversation score by day and top employees',
 'calls-reco': 'Calls: recommendations by employee and company report',
 'zak': 'Procurement: supplier map by price and reliability',
 'zak-obzor': 'Procurement: savings, procedures, volume and agent work',
 'svyaz-today': 'Liaison: waiting for reply, steps for today, hot and new chats',
 'svyaz-set': 'Liaison: network map, who is who and warmth of each contact',
}
TABS = {'ai-chat': 'Chats', 'rop-razbor': 'Chat review', 'rop-plan': 'Sales plan', 'bi-sales': 'Sales dept', 'bi-puls': 'Company pulse', 'bi-fin': 'Finance',
        'bi-direct': 'Ads', 'mk-search': 'Search', 'mk-seo': 'SEO by site', 'mk-geo': 'AI visibility', 'mk-queries': 'Ad queries',
        'hr-obzor': 'Hiring overview', 'hr-kand': 'Candidates', 'hr-tests': 'Bot tests', 'calls-analytics': 'Questions and objections', 'calls-pok': 'Average score',
        'calls-reco': 'Recommendations', 'zak': 'Supplier map', 'zak-obzor': 'Procurement overview', 'svyaz-today': 'Today', 'svyaz-set': 'Network map'}
def shots(keys, label):
    main = keys[0]
    th = ''.join(f'<button type="button" class="sh-t{" on" if i==0 else ""}" data-src="/img/agents/{k}.webp" data-alt="{esc(SHOT_ALT[k])}">{esc(TABS[k])}</button>' for i, k in enumerate(keys)) if len(keys) > 1 else ''
    return (f'<figure class="shot"><div class="shot-bar"><i></i><i></i><i></i><span>{esc(label)}</span><em>demo data</em></div>'
            f'<img src="/img/agents/{main}.webp" alt="{esc(SHOT_ALT[main])}" width="1400" height="685" loading="lazy" decoding="async">'
            f'{"<div class=sh-tabs>"+th+"</div>" if th else ""}</figure>')
def feature(id_, ey, title, lead, bullets, keys, label, reverse=False, extra=''):
    li = ''.join(f'<li>{b}</li>' for b in bullets)
    return (f'<section class="sec feat-sec" id="{id_}"><div class="wrap feat{" feat-r" if reverse else ""}">'
            f'<div class="feat-tx"><div class="eyebrow">{esc(ey)}</div><h2>{title}</h2><p class="sec-sub">{lead}</p><ul class="ticks">{li}</ul>{extra}</div>'
            f'<div class="feat-vis">{shots(keys, label)}</div></div></section>')

ICON = {
 'server': '<svg viewBox="0 0 40 40"><rect x="7" y="7" width="26" height="9" rx="3" class="i1"/><rect x="7" y="19" width="26" height="9" rx="3" class="i2"/><circle cx="12" cy="11.5" r="1.6" class="i3"/><circle cx="12" cy="23.5" r="1.6" class="i3"/><rect x="17" y="31" width="6" height="3" rx="1" class="i3"/></svg>',
 'flow': '<svg viewBox="0 0 40 40"><rect x="5" y="9" width="8" height="22" rx="3" class="i1"/><rect x="16" y="9" width="8" height="15" rx="3" class="i2"/><rect x="27" y="9" width="8" height="9" rx="3" class="i3"/></svg>',
 'pulse': '<svg viewBox="0 0 40 40"><path d="M4 21h8l3-8 5 15 4-11 3 4h9" fill="none" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" class="ip"/></svg>',
 'chat': '<svg viewBox="0 0 40 40"><rect x="5" y="8" width="20" height="13" rx="5" class="i1"/><rect x="15" y="19" width="20" height="13" rx="5" class="i2"/></svg>',
 'sync': '<svg viewBox="0 0 40 40"><g class="ir"><path d="M30 15a11 11 0 0 0-19-3M10 25a11 11 0 0 0 19 3" fill="none" stroke-width="2.8" stroke-linecap="round"/><path d="M9 7v6h6M31 33v-6h-6" fill="none" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/></g></svg>',
 'key': '<svg viewBox="0 0 40 40"><circle cx="14" cy="20" r="7" class="i1"/><path d="M20 20h15M29 20v5M34 20v4" stroke-width="3" stroke-linecap="round" class="ik"/></svg>',
 'bars': '<svg viewBox="0 0 40 40"><rect x="6" y="20" width="6" height="14" rx="2" class="b1"/><rect x="17" y="12" width="6" height="22" rx="2" class="b2"/><rect x="28" y="6" width="6" height="28" rx="2" class="b3"/></svg>',
}
MOD_IC = {'/bitrix': 'flow', '/bitrix-support': 'pulse', '/bitrix-messengers': 'chat', '/bitrix-integrations': 'sync', '/bitrix-licenses': 'key', '/bitrix-korobka': 'server', '/bi-analitika': 'bars'}
def mods_html():
    return '<div class="mods">' + ''.join(f'<a class="md gl tilt" href="{U(p)}"><div class="ic">{ICON[MOD_IC[p]]}</div><h3>{esc(t)}</h3><p>{esc(s)}</p><b>Learn more →</b></a>' for p, t, s in BITRIX_MENU) + '</div>'
INDS = ''.join(f'<span>{x}</span>' for x in ['Real estate', 'Trading and distribution', 'Logistics', 'Car dealers', 'Clinics', 'Education', 'B2B services', 'Retail'] * 2)
STATS3 = ('<div class="stats gl"><div><div class="n3"><b>8</b></div><span>years in IT and CRM</span></div><div><div class="n3"><b>1</b><b>5</b><b>0</b><i>+</i></div><span>implementation projects</span></div>'
          '<div><div class="n3"><b>7</b></div><span>Bitrix24 services</span></div><div><div class="n3"><b>2</b><b>4</b><i>/7</i></div><span>AI agents at work</span></div></div>'
          f'<div class="mq"><div>{INDS}</div></div>')
def sec_head(ey, h2, sub=''):
    return f'<div class="sec-head"><span class="eyebrow">{esc(ey)}</span><h2>{h2}</h2>' + (f'<p class="sec-sub">{sub}</p>' if sub else '') + '</div>'

built = []

# ================================================================ PAGES
# ---------- HOME
home_faq = [
    ('What does MakeBiz do in the UAE?', 'Two directions. First: Bitrix24 implementation and support for companies in Dubai and across the Emirates, including WhatsApp, accounting integrations, licenses and BI analytics. Second: AI agents that take over routine in sales, finance, procurement and hiring.'),
    ('How much does Bitrix24 implementation cost?', 'Standard Bitrix24 CRM setup starts from AED 10,000. Work beyond the standard is charged at AED 200 per hour, with a fixed estimate after a short survey. The Bitrix24 license is paid separately.'),
    ('How much do AI agents cost?', 'One agent on your process starts from AED 5,000, maintenance is 10% of the implementation cost per month. A demo on your process is free.'),
    ('Can you connect WhatsApp to Bitrix24?', 'Yes. Connecting WhatsApp or another messenger costs AED 500, the provider subscription is paid separately. Every message creates a deal and lands in the client card.'),
    ('Do you work only in Dubai?', 'We work with companies across all Emirates, meetings in Dubai or by video call. We speak English and Russian, documents and invoices in dirhams.'),
    ('Where do we start?', 'Leave a request. We run a free diagnostic, find where requests and time are lost, and propose the first step with price and timeline.'),
]
home_body = f'''
<section class="hero hero-home">
  <div class="wrap hero-grid">
    <div class="hero-text">
      <span class="eyebrow">Bitrix24 in Dubai and the UAE</span>
      <h1>Bitrix24 that <span>sells for you</span></h1>
      <p class="lead">We implement and support Bitrix24 for companies in the UAE: deals, calls, WhatsApp, invoices in dirhams and analytics in one system. And AI agents take over the routine</p>
      <p class="answer">MakeBiz Technologies implements and supports Bitrix24 for companies in Dubai and across the Emirates and builds AI agents for business. Standard CRM setup from AED 10,000, one AI agent from AED 5,000, we work in English and Russian.</p>
      <div class="cta-row"><a class="btn" href="#form">Book a diagnostic →</a><a class="btn btn-ghost" href="#bitrix24">What we implement</a></div>
    </div>
    {V_BOARD}
  </div>
  <div class="wrap">{STATS3}</div>
</section>
<section class="sec" id="bitrix24"><div class="wrap">
  {sec_head('Bitrix24 · main direction', 'Everything about Bitrix24 <span>in one team</span>', 'From the first CRM setup to daily support: we implement, connect WhatsApp and accounting systems, help with licenses and build analytics')}
  {mods_html()}
  <div class="pricebar gl"><span>Standard Bitrix24 CRM setup · <b>from AED 10,000</b> · support from AED 1,250 a month</span><a class="btn" href="{U('/bitrix')}">See implementation</a></div>
</div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><div class="aiblk"><div><span class="eyebrow">Second direction</span>
  <h2 style="margin-top:4px">AI agents on top of <span>your Bitrix24</span></h2><p>Once the CRM is set up, agents take over the routine: they answer clients on WhatsApp, review calls, watch the pipeline and the money. One agent from AED 5,000</p>
  <a class="btn btn-ghost" href="{U('/ai-agents')}">More about agents</a></div>
  <ul><li><a href="{U('/ai-agents/rop')}">AI sales head<small>replies when a manager is silent</small></a></li><li><a href="{U('/ai-agents/zvonki')}">Calls<small>every conversation scored</small></a></li>
  <li><a href="{U('/ai-agents/hr')}">Hiring<small>a bot runs the first interview</small></a></li><li><a href="{U('/ai-agents/marketing')}">Marketing<small>content and AI visibility</small></a></li></ul></div></div></section>
<section class="sec" style="padding-top:0"><div class="wrap">{sec_head('Cases', 'Projects we have run <span>for years</span>')}{case_cards(['cdek-b2b','unilin-crm','haval-vector'])}<p class="more"><a href="{U('/keysy')}">All cases →</a></p></div></section>
<section class="sec" style="padding-top:0"><div class="wrap">{sec_head('How we work', 'From diagnostic <span>to profit growth</span>')}{steps([
    ('Diagnostic', 'We review processes and find where requests, money and time are lost. Free, 30-60 minutes, in Dubai or by video call'),
    ('Solution and estimate', 'We propose the first step with price in dirhams and timeline. Standard work at list price, complex work after a survey'),
    ('Implementation', 'We set up the CRM, integrations and agents, migrate data and test on live deals'),
    ('Training and support', 'We train the team and stay on support with hour packages'),
])}</div></section>
{contract_block()}
{faq(home_faq)}
{form_block('index', 'Book a diagnostic', 'We show what to set up in Bitrix24 first and how much it costs. Reply within a business day')}
'''
page('/', 'index', 'Bitrix24 implementation in Dubai and the UAE, AI agents | MakeBiz',
    'Bitrix24 implementation and support in Dubai and the UAE: WhatsApp, Zoho Books and QuickBooks integration, licenses, BI analytics. AI agents for sales. Prices in AED.',
    'home', home_body, [{"@type": "WebSite", "@id": SITE + "/en#website", "url": SITE + "/en", "name": "MakeBiz", "inLanguage": "en"}],
    [('/', 'Home')], home_faq)

# ---------- BITRIX24 IMPLEMENTATION
bx_faq = [
    ('How much does Bitrix24 implementation cost in the UAE?', 'Standard Bitrix24 CRM setup starts from AED 10,000. Anything more complex (several departments, accounting integrations, data migration, custom development) is charged at AED 200 per hour with a fixed estimate after a short survey. The Bitrix24 license is paid separately.'),
    ('How fast can the CRM be launched?', 'Basic launch from 14 days. Accounting integrations, telephony and non-standard processes take longer, we name the timeline after the survey.'),
    ('Is the license included?', f'No, the Bitrix24 license is paid separately at the vendor price. Cloud starts from {lic(49)} a month billed annually, we help pick the plan for your headcount.'),
    ('Do you handle VAT and UAE specifics?', 'Yes. We set up AED currency, 5% VAT on invoices and products, free zone and mainland company details, the Saturday-Sunday weekend, and work in English, Russian and Arabic where needed.'),
    ('Cloud or on-premise Bitrix24?', 'We work with both. Cloud is faster to launch, on-premise goes on your server when data must stay with you or deep customization is needed.'),
    ('What happens after launch?', 'We train the team and stay on support with hour packages: from 5 hours a month for AED 1,250.'),
]
bx_body = hero('Bitrix24 · implementation in the UAE', 'Turnkey Bitrix24 <span>implementation in Dubai</span>',
    'We set up Bitrix24 as a working system: deals, WhatsApp, calls, VAT invoices and reports in one place, with a clear role for every employee',
    'MakeBiz Technologies implements Bitrix24 turnkey for companies in Dubai and across the Emirates: pipelines, business processes, WhatsApp and telephony, Zoho Books, QuickBooks and Odoo integration, BI analytics and team training. Standard setup from AED 10,000, basic launch from 14 days.',
    ('#form', 'Discuss implementation'), ('#price', 'Prices'), V_BOARD,
    [('from AED 10,000', 'standard setup'), ('from 14 days', 'basic launch'), ('AED 200/h', 'work beyond standard'), ('EN · RU', 'working language')],
    'Bitrix24 workspace: sales pipeline, chats and analytics')
bx_body += section('Sound familiar?', 'What people come to us with most often', cards([
    ('Requests get lost in WhatsApp', 'Clients write to managers on personal numbers, part of the requests is never handled, history leaves with the employee'),
    ('There is a CRM but nobody uses it', 'Managers keep clients in spreadsheets and phones, data in the portal goes stale'),
    ('Management cannot see the picture', 'To understand the plan, conversion and money in dirhams you collect reports by hand'),
], 3))
bx_body += section('What the standard setup includes', 'The starter package prepares a working platform, the team works in one environment right away', cards([
    ('Profile and structure', 'Company details, AED currency, Dubai time zone, departments, up to 20 users'),
    ('Roles and access', 'Groups, permissions and security settings: everyone sees their own'),
    ('CRM and pipeline', 'Modules, directories, company and contact fields, card logic and sales stages'),
    ('Invoices with 5% VAT', 'Products and services with tax, invoice template in English and Russian'),
    ('Notifications', 'Basic notifications and role logic so tasks are not lost'),
    ('Training', 'Introductory team training on your deals, in English or Russian'),
], 3, numbered=True))
bx_body += section('How implementation works', '', steps([
    ('Request review', 'We look at current processes and tasks, free, in Dubai or by video call'),
    ('Survey', 'We describe processes and the future CRM architecture, prepare an estimate in AED and a plan'),
    ('Setup', 'Pipelines, roles, robots, WhatsApp, integrations, data migration'),
    ('Training and support', 'We hand the system over to the team and support it after launch'),
]), tone='tint')
bx_body += section('Prices', 'Transparent: standard at list price, anything complex after a survey', prices([
    ('Standard CRM setup', 'from AED 10,000', 'one-off', ['Structure, roles and access', 'CRM, pipeline, cards', 'Up to 20 users', 'Introductory training'], True),
    ('Complex project', 'AED 200', 'per hour of work', ['Pre-project survey', 'Several departments', 'Integrations and data migration', 'Fixed estimate before start'], False),
    ('Support after launch', 'from AED 1,250', 'a month, 5 hours', ['Administration and permissions', 'Process improvements', 'Team consultations', 'Packages of 5, 10 and 20 hours'], False),
], 'The Bitrix24 license is paid separately at the vendor price. Paid services, complex integrations, data migration and custom development are paid separately'), id_='price')
bx_body += section('Everything about Bitrix24 in one team', '', '<div class="grid g3 links">' + ''.join(
    f'<a class="lcard tilt" href="{U(p)}"><b>{esc(t)}</b><span>{esc(s)}</span></a>' for p, t, s in BITRIX_MENU[1:]) + '</div>')
from solutions_src import solutions
SOL = solutions('en')
if SOL:
    bx_body += section('Solutions for the UAE', 'Bitrix24 for the way business runs in Dubai: industries, tax, calls, migration', '<div class="grid g3 links">' + ''.join(
        f'<a class="lcard tilt" href="{U(u)}"><small>{esc(e)}</small><b>{esc(t)}</b><span>{esc(d)}</span></a>' for e, t, d, u in SOL) + '</div>', id_='solutions')
bx_body += section('Cases', '', case_cards(['cdek-b2b', 'unilin-crm', 'performia-crm']), tone='tint')
bx_body += contract_block() + faq(bx_faq) + form_block('bitrix', 'Let us discuss Bitrix24 implementation') + crosslink('ai')
page('/bitrix', 'bitrix', 'Bitrix24 implementation in Dubai and the UAE | MakeBiz',
    'Turnkey Bitrix24 implementation in Dubai and the UAE: CRM, pipelines, WhatsApp, 5% VAT, accounting integrations, training. Standard setup from AED 10,000, launch from 14 days.',
    'bitrix', bx_body, [service_ld('Bitrix24 implementation', 'Turnkey Bitrix24 CRM implementation in the UAE', '/bitrix', 10000)],
    [('/', 'Home'), ('/bitrix', 'Bitrix24 implementation')], bx_faq)

# ---------- SUPPORT
sp_faq = [
    ('How much does Bitrix24 support cost?', 'Monthly hour packages: 5 hours for AED 1,250, 10 hours for AED 2,300, 20 hours for AED 4,200. An hour beyond the package is AED 250.'),
    ('Will you take a portal set up by others?', 'Yes. We start with an audit: how processes, permissions and integrations are set up, and what to fix first.'),
    ('What if the hours run out early?', 'You buy extra hours at AED 250 or move to a bigger package. Before a large task we give an estimate in hours.'),
    ('How fast do you respond?', 'We take requests in a work chat on WhatsApp or Telegram, reply within a business day, urgent failures go first.'),
    ('Can we see where the hours went?', 'Yes, every task and the time spent is logged openly, at the end of the month we send a report.'),
]
sp_body = hero('Bitrix24 · ongoing support', 'Bitrix24 support <span>in Dubai and the UAE</span>',
    'The portal is live, but processes break, employees work around the CRM or nobody develops the system? We take your Bitrix24 on support',
    'MakeBiz Technologies supports Bitrix24 portals of UAE companies after launch: administration, pipeline and robot improvements, email, telephony and WhatsApp integrations, employee training. Packages from 5 hours a month for AED 1,250, an hour beyond the package AED 250.',
    ('#form', 'Get support'), ('#price', 'Packages'), V_TICKETS,
    [('AED 1,250', '5 hours a month'), ('AED 250', 'hour beyond package'), ('1 day', 'reply to a request'), ('EN · RU', 'working language')], 'Bitrix24 portal support')
sp_body += section('When you need support', '', cards([
    ('The portal lives its own life', 'Processes changed, the system did not. Deals bypass the pipeline, reports do not match reality'),
    ('Implemented long ago, not by us', 'We start with an audit and make a prioritized work plan'),
    ('Improvements are needed', 'New fields, pipelines, permissions, robots, and nobody has time'),
    ('No in-house administrator', 'A full-time specialist costs more than an hour package, and tasks come every week'),
    ('Integrations are broken', 'WhatsApp, telephony, email or the accounting exchange stopped working'),
    ('The company is growing', 'New departments, roles and sales lines, and every change needs system updates'),
], 3))
sp_body += section('Support packages', 'Packages by hours per month. An extra hour beyond the package is AED 250', prices([
    ('5 hours', 'AED 1,250', 'a month', ['New employees and permissions', 'Field and notification edits', 'Team consultations'], False),
    ('10 hours', 'AED 2,300', 'a month', ['Process and report improvements', 'Integrations', 'Training new people'], True),
    ('20 hours', 'AED 4,200', 'a month', ['Several business lines', 'Complex automations', 'Constant changes'], False),
]), id_='price')
sp_body += section('What is included', '', cards([
    ('Users and permissions', 'Access, roles, company structure, onboarding new employees'),
    ('CRM', 'Fields, cards, directories, deal and contact logic'),
    ('Processes and robots', 'Business process and automation updates as things change'),
    ('Communication channels', 'Email, telephony, WhatsApp and other messengers: connection and troubleshooting'),
    ('Reports', 'Reports and dashboards for new management questions'),
    ('Consultations', 'We advise how to do it right and train new employees'),
], 3), tone='tint')
sp_body += contract_block() + faq(sp_faq) + form_block('bitrix-support', 'We will take your portal on support') + crosslink('ai')
page('/bitrix-support', 'bitrix-support', 'Bitrix24 support in Dubai and the UAE: hour packages | MakeBiz',
    'Bitrix24 support for UAE companies: administration, improvements, WhatsApp, integrations, training. Packages of 5, 10 and 20 hours from AED 1,250 a month.',
    'bitrix', sp_body, [service_ld('Bitrix24 support', 'Bitrix24 portal support with hour packages', '/bitrix-support', 1250)],
    [('/', 'Home'), ('/bitrix', 'Bitrix24'), ('/bitrix-support', 'Support')], sp_faq)

# ---------- MESSENGERS
ms_faq = [
    ('Can WhatsApp be connected to Bitrix24?', 'Yes. We connect the company number through the official WhatsApp Business Platform from Meta and a connector in the Bitrix24 Contact Center. Conversations land in the deal card, managers reply right from the CRM.'),
    ('How much does it cost?', 'Connecting WhatsApp or another messenger costs AED 500. The provider subscription and paid template messages are separate, we calculate the costs before connecting.'),
    ('Which channels do you connect?', 'WhatsApp, Telegram, social media messages, website live chat and email. All conversations in one Bitrix24 window.'),
    ('Why not via the web version QR code?', 'That connection is unofficial, with broadcasts and complaints the sales number can be blocked. For the main number we use only the official API.'),
    ('Will the history stay if a manager leaves?', 'Yes, the whole history stays in the client card in Bitrix24, not on a personal phone.'),
]
ms_body = hero('Bitrix24 · messengers', 'WhatsApp and messengers <span>in Bitrix24</span>',
    'In the UAE clients write on WhatsApp, not email. We connect the company number to the CRM: every conversation in the client card, management sees who replied and how fast',
    'MakeBiz Technologies connects WhatsApp to Bitrix24 through the official WhatsApp Business Platform, plus Telegram, social media and website chat: a new message creates a lead or deal, assigns an owner, and the history stays with the company. Connection AED 500.',
    ('#form', 'Connect WhatsApp'), ('#rules', 'WhatsApp rules'), V_CHAT,
    [('AED 500', 'channel connection'), ('1 number', 'for the whole team'), ('API', 'official, from Meta'), ('100%', 'of chats in the CRM')], 'Messenger conversations in the deal card')
ms_body += section('What happens without integration', '', cards([
    ('Clients on personal phones', 'Each manager chats from their own number. When an employee leaves, their clients and all agreements leave too'),
    ('No reply, and nobody knows', 'A message came on Friday evening, the manager saw it on Monday. Management learns when the client has already bought elsewhere'),
    ('History lives in the chat', 'Prices, discounts and deadlines were agreed on WhatsApp, and the CRM is empty. The next manager starts from scratch'),
], 3))
ms_body += section('How we connect', '', cards([
    ('Official WhatsApp Business Platform', 'The company number connects to the Meta API via a connector in the Bitrix24 Contact Center. We pick the provider by message volume and price'),
    ('Open channels', 'Conversations are distributed among managers in turn, by language or by business line. Reply time is visible, a chat can be handed over'),
    ('A lead or deal from the first message', 'A new number creates a lead or deal with the WhatsApp source, a returning client lands in their card'),
    ('After-hours auto reply', 'Considering UAE weekends and holidays, in English, Russian and Arabic where needed'),
    ('Reply speed control', 'If a message has no reply in 15 minutes, a notification goes to the manager'),
    ('Channel report', 'How many chats, how many without reply and how many became deals'),
], 3), tone='tint')
ms_body += section('WhatsApp rules to know in advance', '', '''<div class="grid g2"><div class="card"><h3>The 24-hour window</h3><p>You can reply in free text within 24 hours after the client's last message. When the window closes, you can write first only with a template approved by Meta: a reminder, order status, an invoice</p></div>
<div class="card"><h3>Templates and broadcasts</h3><p>Template messages are paid, the provider sets the price. Broadcasts only to people who opted in, otherwise complaints grow and the number gets limited</p></div></div>''', id_='rules')
ms_body += section('What we do', 'Connecting a channel is not enough, it has to be built into sales', steps([
    ('Number and provider', 'We choose the company number and API provider and pass Meta verification'),
    ('Open channels', 'Queue, distribution, working hours and auto replies'),
    ('CRM and robots', 'Chats linked to leads and deals, reply time control'),
    ('Templates and launch', 'Templates submitted for approval, team trained, we stay on support'),
]))
ms_body += contract_block() + faq(ms_faq) + form_block('bitrix-messengers', 'We will connect WhatsApp to your Bitrix24') + crosslink('ai')
page('/bitrix-messengers', 'bitrix-messengers', 'WhatsApp in Bitrix24 for businesses in the UAE | MakeBiz',
    'We connect WhatsApp to Bitrix24 via the official Meta API, plus Telegram, social media and website chat: conversations in the deal card, reply control. From AED 500.',
    'bitrix', ms_body, [service_ld('WhatsApp and messengers in Bitrix24', 'Connecting WhatsApp Business Platform, Telegram and social media to Bitrix24', '/bitrix-messengers', 500)],
    [('/', 'Home'), ('/bitrix', 'Bitrix24'), ('/bitrix-messengers', 'Messengers')], ms_faq)

# ---------- ACCOUNTING INTEGRATIONS
c1_faq = [
    ('Which accounting systems do you integrate with Bitrix24?', 'In the UAE most often Zoho Books, QuickBooks and Odoo, some companies use 1C. We also connect bank statements, warehouse and internal services via API.'),
    ('What data is exchanged?', 'Clients and companies, products and prices, VAT invoices, payments and stock. The scope and direction of the exchange are defined in the survey.'),
    ('How much does integration cost?', 'Integrating Bitrix24 with an accounting system starts from AED 10,000. The exact price depends on the system and exchange scope, the estimate is fixed after the survey.'),
    ('Is 5% VAT handled?', 'Yes. Tax rates, company TRNs and VAT invoices pass between systems consistently, so accounting does not fix documents by hand.'),
    ('What if the exchange breaks after an update?', 'We take the integration on support: we monitor the exchange and fix it within the hour package.'),
]
c1_body = hero('Bitrix24 · accounting integrations', 'Bitrix24 integration <span>with your accounting</span>',
    'Managers see prices, stock and payments in the CRM, and accounting gets deals and VAT invoices without manual entry',
    'MakeBiz Technologies connects Bitrix24 with Zoho Books, QuickBooks, Odoo and 1C: clients, products, invoices with 5% VAT, payments and stock sync automatically, without double entry. Integration from AED 10,000, the exact estimate is fixed after a survey.',
    ('#form', 'Discuss integration'), None, V_SYNC,
    [('No double entry', 'data both ways'), ('from AED 10,000', 'integration'), ('5% VAT', 'in invoices and products'), ('Zoho · QuickBooks', 'Odoo · 1C')], 'Data exchange between Bitrix24 and an accounting system')
c1_body += section('What integration gives you', '', cards([
    ('No double entry', 'A client, invoice or order is created once and appears in both systems'),
    ('Prices and stock in the CRM', 'Managers do not ask the warehouse or accounting, everything is in the card'),
    ('Payments in the deal', 'A payment arrives and the Bitrix24 deal moves on by itself'),
    ('VAT invoices', 'Tax rates and details are not retyped by hand'),
    ('Money analytics', 'Sales from the CRM and money from accounting in one report'),
    ('Fits your processes', 'Exchange scope and direction set up the way you work'),
], 3))
c1_body += section('What we connect', '', cards([
    ('Zoho Books', 'Clients, invoices, payments and items between Zoho Books and the CRM'),
    ('QuickBooks', 'Invoices, payments and clients for companies on QuickBooks Online'),
    ('Odoo', 'Sales, warehouse and accounting where Odoo already runs as the ERP'),
    ('1C and banks', 'Exchange with 1C and bank statement import for payment reconciliation'),
], 4), tone='tint')
c1_body += section('How we connect', '', steps([
    ('Survey', 'We review the accounting system, processes and what needs to be exchanged'),
    ('Exchange design', 'We describe objects, directions and rules and fix the estimate in AED'),
    ('Setup and test', 'We set up the exchange and test on test and real documents'),
    ('Launch and support', 'We put it into operation and monitor the exchange on support'),
]))
c1_body += section('Cases', '', case_cards(['unilin-crm', 'performia-crm', 'cdek-b2b']), tone='tint')
c1_body += contract_block() + faq(c1_faq) + form_block('bitrix-integrations', 'We will connect Bitrix24 to your accounting') + crosslink('ai')
page('/bitrix-integrations', 'bitrix-integrations', 'Bitrix24 integration with Zoho Books, QuickBooks, Odoo | MakeBiz',
    'Bitrix24 integration with Zoho Books, QuickBooks, Odoo and 1C for UAE companies: clients, 5% VAT invoices, payments and stock without double entry. From AED 10,000.',
    'bitrix', c1_body, [service_ld('Bitrix24 accounting integrations', 'Data exchange between Bitrix24 and Zoho Books, QuickBooks, Odoo, 1C', '/bitrix-integrations', 10000)],
    [('/', 'Home'), ('/bitrix', 'Bitrix24'), ('/bitrix-integrations', 'Accounting integrations')], c1_faq)

# ---------- LICENSES (bitrix24.ae prices, USD -> AED at 3.6725)
CLOUD = [
    ('Basic', lic(49), f'a month billed annually ($49) · {lic(69)} monthly ($69)', ['5 users', 'CRM, tasks, chats, drive', 'Sites and online booking'], False),
    ('Standard', lic(99), f'a month billed annually ($99) · {lic(144)} monthly ($144)', ['50 users', 'Marketing, online documents', 'Everything in Basic'], False),
    ('Professional', lic(199), f'a month billed annually ($199) · {lic(289)} monthly ($289)', ['100 users', 'Sales and process automation', 'End-to-end analytics'], True),
    ('Enterprise', f'from {lic(399)}', f'a month billed annually (from $399) · from {lic(579)} monthly', ['from 250 to 10,000 users', 'Branches and holdings', 'Advanced security'], False),
]
ENT = [('250', 399, 579), ('500', 639, 919), ('1,000', 799, 1149), ('10,000', 7999, 11499)]
BOX = [('Business', '50 (options for 100, 250 and 500)', f'{lic(3590)} ($3,590)'), ('Enterprise', 'from 1,000', f'{lic(24990)} ($24,990)')]
def ent_table():
    rows = ''.join(f'<tr><td><b>Enterprise {u}</b></td><td class="pt-p">{lic(a)} <small>(${a:,})</small></td><td>{lic(m)} <small>(${m:,})</small></td></tr>' for u, a, m in ENT)
    return f'<div class="ptw gl"><table class="ptab"><thead><tr><th>Plan</th><th>A month billed annually</th><th>Monthly</th></tr></thead><tbody>{rows}</tbody></table></div>'
def box_table():
    rows = ''.join(f'<tr><td><b>{esc(n)}</b></td><td>{esc(u)}</td><td class="pt-p">{esc(p)}</td></tr>' for n, u, p in BOX)
    return (f'<div class="ptw gl"><table class="ptab"><thead><tr><th>Edition</th><th>Users</th><th>License per year</th></tr></thead><tbody>{rows}</tbody></table></div>'
            f'<p class="note">Vendor prices from bitrix24.ae as of {PRICE_DATE} in US dollars, converted to AED at 3.6725. Prices for Business options with 100, 250 and 500 users and the exact amount are fixed in the invoice</p>')
lc_faq = [
    ('How much does Bitrix24 cost in the UAE?', f'Vendor prices from bitrix24.ae as of {PRICE_DATE}, billed annually: Basic {lic(49)} a month, Standard {lic(99)}, Professional {lic(199)}, Enterprise from {lic(399)}. There is a free plan for 1-2 users. The on-premise Business edition is {lic(3590)} a year.'),
    ('What currency are the prices in?', 'The vendor publishes UAE prices in US dollars. We show them in dirhams at 3.6725 with the dollar price next to it, the exact amount is fixed in the invoice.'),
    ('How much does annual billing save?', 'Annual billing makes the monthly price of a cloud plan about 30% lower than monthly billing.'),
    ('Which plan should we choose?', 'A sales team of up to 5 people is fine on Basic. A company of up to 50 people: Standard. For process automation and end-to-end analytics: Professional. Branches and hundreds of employees: Enterprise or on-premise.'),
    ('Cloud or on-premise?', 'Cloud is faster to launch and needs no server. On-premise is chosen when data must stay in-house, deep code customization is needed or there are many users. Details on the on-premise Bitrix24 page.'),
    ('Will you help with renewal and plan changes?', 'Yes, we remind you about renewal in advance and help move to a higher or lower plan without losing data.'),
]
lc_body = hero('Bitrix24 · licenses and prices', f'Bitrix24 prices in the UAE <span>from {lic(49)} a&nbsp;month</span>',
    'We pick the plan for your tasks, help with the purchase and renew on time so the portal never stops',
    f'Cloud Bitrix24 prices for the UAE from bitrix24.ae as of {PRICE_DATE}: Basic {lic(49)}, Standard {lic(99)}, Professional {lic(199)} a month billed annually, Enterprise from {lic(399)}. On-premise from {lic(3590)} a year. MakeBiz Technologies helps pick, purchase and renew the license.',
    ('#form', 'Pick a plan'), ('#ceny', 'See prices'), V_LIC,
    [(lic(49), 'cloud a month'), ('−30%', 'with annual billing'), (lic(3590), 'on-premise a year'), ('USD → AED', 'rate 3.6725')], 'Bitrix24 license')
lc_body += section('Cloud Bitrix24 prices', f'Vendor prices as of {PRICE_DATE}, for all users of the plan. There is a Free plan for 1-2 users', prices(CLOUD, 'Prices from bitrix24.ae in US dollars, in dirhams at 3.6725. The exact amount and current promotions are fixed in the invoice'), id_='ceny')
lc_body += section('Enterprise plans', 'For branches, holdings and hundreds of employees', ent_table(), tone='tint')
lc_body += section('On-premise Bitrix24 prices', 'Bitrix24 on your server: your data, access to code and customization', box_table() +
    f'<p class="more"><a href="{U("/bitrix-korobka")}">On-premise Bitrix24 implementation →</a></p>')
lc_body += section('What we do', '', cards([
    ('Plan selection', 'We count users and needed features so you do not overpay'),
    ('Purchase', 'We help buy the license for your company and sort out payment'),
    ('Renewal', 'We remind you in advance so the portal does not go into limited mode'),
    ('Plan change', 'Moving up or down without losing data and settings'),
    ('Cloud or on-premise', 'We help choose and migrate the portal if needed'),
    ('Setup right away', 'The license can come together with the standard CRM setup from AED 10,000'),
], 3), tone='tint')
lc_body += contract_block() + faq(lc_faq) + form_block('bitrix-licenses', 'We will pick a Bitrix24 plan', 'Tell us how many employees will use the portal and what you need, we send a plan suggestion') + crosslink('ai')
page('/bitrix-licenses', 'bitrix-licenses', 'Bitrix24 prices in the UAE 2026: plans in AED | MakeBiz',
    f'Bitrix24 prices in the UAE: cloud from {lic(49)} a month, Enterprise from {lic(399)}, on-premise from {lic(3590)} a year. bitrix24.ae prices in AED and USD, plan selection and renewal.',
    'bitrix', lc_body, [service_ld('Bitrix24 licenses', 'Selection, purchase and renewal of Bitrix24 licenses in the UAE', '/bitrix-licenses', 180),
        {"@type": "OfferCatalog", "name": "Bitrix24 plans in the UAE", "itemListElement": [
            {"@type": "Offer", "name": 'Bitrix24 ' + n, "price": str(round(u * USD_AED)), "priceCurrency": "AED", "seller": {"@id": SITE + "/#organization"}} for n, u in [('Basic', 49), ('Standard', 99), ('Professional', 199), ('Enterprise 250', 399), ('Business (on-premise, year)', 3590), ('Enterprise (on-premise, year)', 24990)]]}],
    [('/', 'Home'), ('/bitrix', 'Bitrix24'), ('/bitrix-licenses', 'Licenses and prices')], lc_faq)

# ---------- ON-PREMISE
kb_faq = [
    ('How is on-premise Bitrix24 different from cloud?', 'On-premise runs on your server or in your data center: data stays with you, you get code access, can customize deeply and connect internal services. Cloud runs on Bitrix24 servers, it is faster to launch, but customization is limited to apps.'),
    ('How much does on-premise Bitrix24 cost?', f'License at bitrix24.ae prices as of {PRICE_DATE}: Business for 50 users {lic(3590)} a year ($3,590), with options for 100, 250 and 500 users. Enterprise from 1,000 users {lic(24990)} ($24,990). Implementation is charged at AED 200 per hour, the estimate is fixed after a survey.'),
    ('What server is needed?', 'Your own physical server, a cloud virtual machine or a data center in the UAE. We size the configuration for your users, deploy the environment and set up backups.'),
    ('Can a cloud portal be moved to on-premise?', 'Yes. We migrate CRM, tasks, users and files, rebuild what does not move automatically and check the data before switching the team.'),
    ('Who will update and maintain it?', 'We can take it on support: updates, backups, monitoring, security and improvements. Packages from AED 1,250 a month.'),
]
kb_body = hero('Bitrix24 · on your server', 'On-premise Bitrix24: <span>implementation on your server</span>',
    'Data stays with you, the system adapts to any process and connects to internal services. We install, migrate, customize and support',
    f'MakeBiz Technologies implements on-premise Bitrix24 on a company server in the UAE: we pick the edition and server, deploy the system, migrate data from the cloud or another CRM, customize it for your processes, integrate with accounting systems and take it on support. License from {lic(3590)} a year, work at AED 200 per hour.',
    ('#form', 'Discuss on-premise'), ('#ceny', 'License prices'), V_BOX,
    [('Your server', 'your data'), ('Code', 'unlimited customization'), (lic(3590), 'license a year'), ('CDEK, Unilin', 'on-premise in operation')], 'On-premise Bitrix24 on a server')
kb_body += section('When you need on-premise', 'If two or more of these apply, the cloud will feel tight', cards([
    ('Data only in-house', 'Security policy requires keeping clients and documents in your perimeter or in the UAE'),
    ('Code customization', 'Custom modules, non-standard entities, logic that an app cannot do'),
    ('Many internal systems', 'Your own ERP, accounting, telephony and services that need deep exchange'),
    ('Hundreds of employees', 'With many users an on-premise license costs less than a subscription'),
    ('Branches and holdings', 'Free zone and mainland companies, different entities and permissions in one system'),
    ('Control over updates', 'You decide when to update the system'),
], 3))
kb_body += section('Cloud or on-premise', '', '''<div class="vs"><div class="vs-col"><h3>Cloud</h3><ul><li>Launch in a day, no server needed</li><li>Updates and backups by Bitrix24</li><li>Customization via apps and webhooks</li><li>Monthly or annual subscription</li></ul></div>
<div class="vs-col vs-good"><h3>On-premise</h3><ul><li>Your server or data center, data in your perimeter</li><li>Code access and customization of any depth</li><li>Direct integrations with internal systems</li><li>Annual license, cheaper with a large team</li></ul></div></div>''', tone='tint')
kb_body += section('What we do', '', cards([
    ('Edition and server', 'We count users and load, choose the edition and server configuration'),
    ('Deployment', 'We install Bitrix24, set up the environment, SSL, email and backups'),
    ('Data migration', 'From cloud Bitrix24, Zoho CRM, HubSpot or spreadsheets: clients, deals, tasks, files'),
    ('Setup and customization', 'Pipelines, permissions, business processes, custom modules and code changes'),
    ('Integrations', 'Zoho Books, QuickBooks, Odoo, 1C, telephony, WhatsApp and BI'),
    ('Support', 'Updates, monitoring, security and improvements with an hour package'),
], 3))
kb_body += section('On-premise license prices', f'Vendor prices as of {PRICE_DATE}', box_table(), id_='ceny', tone='tint')
kb_body += section('How we implement', '', steps([
    ('Survey', 'We review processes, security requirements and integrations and fix the estimate'),
    ('Server and installation', 'We deploy on-premise on your server or in a data center'),
    ('Migration and setup', 'We migrate data, set up CRM, processes and permissions, make customizations'),
    ('Launch and support', 'We train the team, launch and take the system on support'),
]))
kb_body += section('On-premise cases', '', case_cards(['cdek-b2b', 'unilin-crm']))
kb_body += contract_block() + faq(kb_faq) + form_block('bitrix-korobka', 'Let us discuss on-premise Bitrix24', 'Tell us how many users and which systems to connect, we propose the edition, server and estimate') + crosslink('ai')
page('/bitrix-korobka', 'bitrix-korobka', 'On-premise Bitrix24 in the UAE: implementation on your server | MakeBiz',
    f'On-premise Bitrix24 on a company server in the UAE: edition selection, installation, cloud migration, customization, integrations and support. License from {lic(3590)} a year.',
    'bitrix', kb_body, [service_ld('On-premise Bitrix24 implementation', 'Installation, customization and support of Bitrix24 on the client server', '/bitrix-korobka', 13184)],
    [('/', 'Home'), ('/bitrix', 'Bitrix24'), ('/bitrix-korobka', 'On-premise Bitrix24')], kb_faq)

# ---------- BI
bi_faq = [
    ('What is BI analytics in Bitrix24?', 'Management dashboards on data from the CRM and other systems: sales, pipeline, manager performance, money in dirhams. We build them in the Bitrix24 BI builder or an external BI system.'),
    ('Which sources can be connected?', 'Bitrix24, Zoho Books, QuickBooks, Odoo, 1C, telephony, Google Ads, Meta, Google Analytics, spreadsheets and bank statements. The set depends on your questions.'),
    ('How much does BI analytics cost?', 'BI analytics starts from AED 1,000. The final price depends on the number of sources and metrics, the estimate is fixed after we agree on the metric list.'),
    ('Will the numbers be right?', 'We start by checking CRM data: a dashboard tells the truth only if the system has no garbage. If needed, we first clean up cards and stages.'),
]
bi_body = hero('Bitrix24 · BI analytics', 'BI analytics <span>for management</span>',
    'Sales, pipeline, managers and money on one screen. Numbers from the CRM and accounting, not from manual spreadsheets',
    'MakeBiz Technologies builds BI dashboards for UAE companies on data from Bitrix24, accounting systems, telephony and ads: management sees the plan, conversion, every manager and money in dirhams in real time. BI analytics from AED 1,000, estimate after the metric list is agreed.',
    ('#form', 'Discuss a dashboard'), None, V_BI,
    [('1 screen', 'instead of reports'), ('CRM + accounting', 'and other sources'), ('from AED 1,000', 'BI analytics'), ('AED', 'money in dirhams')], 'BI analytics dashboards')
bi_body += section('What dashboards show', '', cards([
    ('Sales and plan', 'Revenue, plan and actuals by department and manager'),
    ('Pipeline', 'Stage conversion and where deals get stuck'),
    ('Managers', 'Reply speed, activity, calls and results'),
    ('Money', 'Payments, receivables and VAT from the accounting system'),
    ('Advertising', 'Where clients come from and which channels pay off'),
    ('Operations', 'Workload, timelines and quality of your processes'),
], 3))
bi_body += feature('pult', 'Example from our company', 'Company pulse <span>on one screen</span>',
    'We run MakeBiz through this cabinet: data comes from Bitrix24, banks, accounting, telephony and ads and updates without manual spreadsheets. Russian interface, demo data',
    ['Revenue, profit, costs and assets for every business line and project',
     'Sales: leads, payments, touches, reply speed and drops by week',
     'Finance: turnover, profitability, dividends and cash runway in months',
     'Marketing: spend, clicks and cost per click by campaign, SEO and AI visibility',
     'An AI agent reads the same numbers and flags risks by itself'],
    ['bi-puls', 'bi-sales', 'bi-fin', 'bi-direct'], 'Company pulse')
bi_body += section('How we build it', '', steps([
    ('Management questions', 'We fix which decisions the dashboard must support'),
    ('Data', 'We check sources and clean up the CRM if needed'),
    ('Dashboards', 'We build metrics and views and verify numbers with you'),
    ('Growth', 'We add metrics as you grow and train the team'),
]), tone='tint')
bi_body += section('Cases', '', case_cards(['performia-crm', 'unilin-crm', 'apartika-crm']))
bi_body += contract_block() + faq(bi_faq) + form_block('bi-analitika', 'We will build a dashboard for your questions') + crosslink('ai')
page('/bi-analitika', 'bi-analitika', 'BI analytics for Bitrix24 in the UAE: management dashboards | MakeBiz',
    'BI analytics for UAE companies from AED 1,000: dashboards on Bitrix24, accounting, telephony and ad data. Sales, pipeline, managers and money on one screen.',
    'bitrix', bi_body, [service_ld('BI analytics for Bitrix24', 'Management dashboards on CRM and accounting data', '/bi-analitika', 1000)],
    [('/', 'Home'), ('/bitrix', 'Bitrix24'), ('/bi-analitika', 'BI analytics')], bi_faq)

# ---------- AI AGENTS
VIDEO_LD = {"@type": "VideoObject", "name": "MakeBiz AI agents: how agents run a company",
    "description": "A tour of the MakeBiz cabinet: company pulse, chats with sales head hints, chat review, sales pipeline, finance, marketing, hiring, call speech analytics and procurement. Russian interface.",
    "thumbnailUrl": [SITE + '/media/agents-poster.jpg'], "uploadDate": "2026-10-22", "duration": "PT3M10S",
    "contentUrl": SITE + '/media/agents.mp4', "inLanguage": "ru", "publisher": {"@id": SITE + "/#organization"}}
def video_block():
    return ('<section class="sec" id="video"><div class="wrap"><div class="sec-head"><div class="eyebrow">Video · 3 minutes</div><h2>The cabinet where <span>our agents work</span></h2>'
            '<p class="sec-sub">This is how MakeBiz is run from the inside: money, sales, calls, hiring, marketing and procurement in one system. This is what we implement for clients. Interface in Russian</p></div>'
            '<div class="vid"><video controls preload="none" playsinline poster="/media/agents-poster.jpg" width="1280" height="720"><source src="/media/agents.mp4" type="video/mp4"></video></div></div></section>')
YT = {'hr': ('DTJ6tVOx6dg', 'HR block with an AI agent: hiring from a response to the first working day', 'A Telegram bot interviews and scores candidates, and the manager sees every step: funnel, candidate scores, motivation types, salaries, talent pool and probation results. Video in Russian.', '2026-10-20', 'PT2M48S'),
      'zvonki': ('HknIeajCo18', 'Call speech analytics for sales growth', 'How speech analytics shows where managers lose clients, which objections repeat and which scripts work poorly. Video in Russian.', '2026-05-26', None)}
def yt_block(k):
    vid, name, desc, d, dur = YT[k]
    return (f'<section class="sec"><div class="wrap"><h2>Video: <span>how it works</span></h2><p class="sec-sub">{esc(desc)}</p>'
            f'<div class="yt" data-id="{vid}"><img src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" alt="{esc(name)}" width="480" height="360" loading="lazy"><button type="button" aria-label="Play video">▶</button></div>'
            f'<p class="more"><a href="https://www.youtube.com/watch?v={vid}" rel="noopener">Watch on YouTube →</a></p></div></section>')
def yt_ld(k):
    vid, name, desc, d, dur = YT[k]
    o = {"@type": "VideoObject", "name": name, "description": desc, "thumbnailUrl": [f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"], "uploadDate": d,
         "embedUrl": f"https://www.youtube.com/embed/{vid}", "contentUrl": f"https://www.youtube.com/watch?v={vid}", "inLanguage": "ru", "publisher": {"@id": SITE + "/#organization"}}
    if dur: o["duration"] = dur
    return o

AGENTS = [
 dict(slug='rop', name='AI sales head', short='Sales and chats', sub='Hints in every chat, chat review, plan control',
  title='AI sales head agent: sales team and chat control in Bitrix24 | MakeBiz',
  desc='An AI agent acting as head of sales: drafts replies, takes over a chat when a manager is silent, reviews manager chats and tracks the plan in Bitrix24.',
  h1='An AI sales head that <span>never misses a client</span>',
  lead='The agent sees every chat and deal, suggests a reply to the manager, answers by itself if nobody reacts, and reviews the team mistakes every morning',
  answer='The MakeBiz AI sales head works inside Bitrix24 and messengers: it drafts a reply right in the chat window, takes over the conversation after 15 minutes of silence, reviews manager chats and tracks the sales plan.',
  chips=[('15 minutes', 'and the agent replies'), ('Every morning', 'chat review'), ('Plan', 'for every manager'), ('Bitrix24', 'everything in the deal')],
  feats=[('A hint in every chat', 'A ready reply with price in AED and next step in the chat window: insert, shorten or soften in one click'),
         ('Takes over the chat', 'If a manager has not replied in 15 minutes, the agent answers the client and sets a task for the owner'),
         ('Waiting queue', 'Who is waiting and for how many minutes, across all channels at once'),
         ('Chat review', 'Every morning: where mistakes were made, how to answer, which leads were closed too early and who to bring back'),
         ('Plan and pipeline', 'Monthly plan, leads, deals and payments by manager, which deals to close first'),
         ('Who to call today', 'A list of clients to contact with the reason and a hint on what to say')],
  ticks=['WhatsApp, Telegram, social media, email and site chats in one queue', 'Every chat scored, typical manager mistakes', 'Plan and actuals by manager and pipeline stage', 'Everything is written to the Bitrix24 deal'],
  shots=['ai-chat', 'rop-razbor', 'rop-plan', 'bi-sales'],
  faq=[('Will the AI sales head replace the head of sales?', 'No, it takes over routine: watches reply speed, reviews chats and gives hints. Decisions and people stay with the head.'),
       ('Which channels does it work with?', 'WhatsApp, Telegram, social media, email and site chats connected to Bitrix24. Other channels on request.'),
       ('What language does the agent reply in?', 'In the client language: English, Russian and Arabic where needed. Tone and reply rules are set for your company.'),
       ('Does the agent write to clients by itself?', 'Only by the rules you set: for example, if a manager is silent for 15 minutes. Everything the agent wrote is visible in the deal.')]),
 dict(slug='svyaznoy', name='Liaison agent', short='Contacts and relationships', sub='Who waits for a reply, who to contact, the full contact picture',
  title='Liaison AI agent: contacts, reminders and client relationships | MakeBiz',
  desc='The liaison AI agent watches all contacts: who is waiting for a reply, who to get in touch with, who is hot and who is cooling down. Network map and warmth of each contact.',
  h1='Liaison: an agent that <span>remembers every person</span>',
  lead='The agent keeps all your contacts in mind: clients, partners, contractors. It reminds you who to answer and who to contact, and shows which relationships are cooling down',
  answer='The MakeBiz liaison agent collects contacts from WhatsApp, Telegram, CRM and email, shows who is waiting for a reply and which steps are planned for today, and rates the warmth of each contact so relationships are not lost.',
  chips=[('Waiting', 'visible at once'), ('Steps', 'for today'), ('Warmth', 'of each contact'), ('Telegram', 'and CRM')],
  feats=[('Waiting for reply', 'Who wrote and got no answer, how long they wait and what to reply'),
         ('Steps for today', 'Agreed to call or send a quote: the agent reminds you on the right day'),
         ('Hot and new', 'New conversations and contacts ready to talk right now'),
         ('Network map', 'Who is who: clients, partners, contractors, personal contacts and spam'),
         ('Contact warmth', 'Cold, warm, close: see which relationships are cooling down'),
         ('Morning brief', 'A short Telegram summary: what matters today and who not to forget')],
  ticks=['Contacts from WhatsApp, Telegram, CRM and email in one picture', 'Status and warmth of every card', 'Birthdays and reasons to get in touch', 'Deals and leads created in Bitrix24 in one click'],
  shots=['svyaz-today', 'svyaz-set'],
  faq=[('How is the liaison agent different from a CRM?', 'A CRM stores deals. The liaison agent watches people: who is waiting, who you have not talked to for a while, what is agreed for today, and passes to the CRM what becomes a deal.'),
       ('Where does the agent get contacts?', 'From WhatsApp, Telegram, Bitrix24 and email. The source set is defined at the start.'),
       ('Who is it for?', 'Owners, managers and salespeople with hundreds of contacts and agreements that must not be lost.')]),
 dict(slug='zvonki', name='Speech analytics', short='Call analytics', sub='Every conversation scored, objections, recommendations',
  title='AI speech analytics for calls: conversation and script scoring | MakeBiz',
  desc='An AI agent listens to every sales call: transcript, conversation score, script stages, top questions and objections, recommendations for each manager.',
  h1='Speech analytics: <span>every call scored</span>',
  lead='The system listens to every call and shows where managers lose clients, which objections repeat and which scripts do not work',
  answer='MakeBiz speech analytics transcribes and scores every sales call: script stages, emotions, client questions and objections. Management sees the average score by manager and gets recommendations on who to train and what to change in the script. From AED 1,000 a month for 5,000 minutes.',
  chips=[('100%', 'of calls checked'), ('AED 1,000', 'a month, 5,000 minutes'), ('Objections', 'top for the company'), ('EN · RU', 'call languages')],
  feats=[('Conversation score', 'A score for every call and stage completion: greeting, needs discovery, presentation, objection handling, agreement'),
         ('Call details', 'Transcript, what went well, where the mistake was and a specific hint for the manager'),
         ('Questions and objections', 'Top client questions and objections across all calls: what to add to the script'),
         ('Trends', 'Average score by day and manager, compared with the previous period'),
         ('Recommendations', 'Who needs training, who needs control, where quality drops'),
         ('Company report', 'How many calls were checked, how many were problematic, sale probability')],
  ticks=['We connect telephony and recordings from Bitrix24', 'Scoring criteria built on your script', 'Call summary and score in the deal card', 'Hundreds of thousands of minutes a month without manual listening'],
  shots=['calls-analytics', 'calls-pok', 'calls-reco'],
  faq=[('How much does speech analytics cost?', 'Monthly by call volume: AED 1,000 a month for 5,000 minutes, AED 1,700 for 10,000 minutes, from AED 4,000 for 30,000 minutes and more. Connection is free.'),
       ('What languages are calls analyzed in?', 'English and Russian, Arabic on request. Reports and recommendations in the language of management.'),
       ('Which telephony does it work with?', 'With telephony connected to Bitrix24 and most cloud PBXs that provide call recordings.'),
       ('What criteria are calls scored by?', 'By your script: stages, required phrases, objection handling. Criteria are set at the start and adjusted over time.'),
       ('Is there an implementation example?', 'Yes, the HAVAL dealer network: over 300,000 call minutes a month against 40+ criteria. The case is in the cases section.')]),
 dict(slug='hr', name='HR agent', short='Hiring and interviews', sub='A bot interviews, scores and runs the funnel',
  title='AI agent for hiring: candidate screening and bot interviews | MakeBiz',
  desc='HR agent: responses from job boards and your site, the first interview in a Telegram or WhatsApp bot, candidate scoring, motivation types, talent pool and a funnel from response to first day.',
  h1='Hiring with an AI agent: <span>from response to first day</span>',
  lead='Every candidate gets a link to the bot, the bot runs the first interview and gives a score, and the manager sees every step in numbers',
  answer='The MakeBiz HR agent collects responses from job boards and your site, runs the first interview and tests in a bot in English or Russian, scores the candidate and proposes a decision: invite, reserve or reject. The manager only does the final meeting.',
  chips=[('Responses', 'from boards and site'), ('Bot', 'interview in EN and RU'), ('Score', 'for every candidate'), ('Funnel', 'to the first day')],
  feats=[('Responses in one place', 'Responses from job boards and the site gather in a funnel, every candidate gets a link to the bot'),
         ('Interview in a bot', 'The bot asks vacancy questions, runs tests and records answers'),
         ('Score and decision', 'Candidate score, strengths, red flags and a one-click decision: invite, reserve or reject'),
         ('Motivation types', 'Security, money, results or status driven: you know what keeps a person'),
         ('Salaries', 'Candidate expectations in AED, market range and the price of skills'),
         ('Talent pool and results', 'Strong candidates in reserve with a reminder when to reach out again. Probation results show how accurately the bot selects people')],
  ticks=['End-to-end funnel for every vacancy and channel', 'Match between bot and manager decisions in numbers', 'Employees and probation results', 'Candidates and employees in Bitrix24'],
  shots=['hr-obzor', 'hr-kand', 'hr-tests'],
  faq=[('Do candidates drop off because of the bot?', 'The bot takes 20-30 minutes at a convenient time, without waiting for a call. You see how many started the test and how many finished.'),
       ('Can questions be set for our vacancy?', 'Yes, questions, tests and scoring criteria are set for each vacancy, in English or Russian.'),
       ('Which job boards does it work with?', 'Responses from any board and your site go through the bot by link. A direct integration with a specific board is connected on request.')]),
 dict(slug='zakupki', name='Procurement agent', short='Suppliers and quotes', sub='Sends requests, collects quotes, compares suppliers',
  title='AI procurement agent: supplier requests and quote comparison | MakeBiz',
  desc='The AI procurement agent sends requests to suppliers, collects commercial quotes, compares prices, lead times and reliability and shows the savings.',
  h1='Procurement agent: <span>weeks of work in hours</span>',
  lead='The agent sends requests to suppliers, collects price lists and quotes and compares them: who is cheaper, who delivers faster, who keeps prices',
  answer='The MakeBiz procurement agent sends requests to suppliers by specification, collects and parses quotes, compares price, lead time and reliability and shows the savings for every procurement.',
  chips=[('Requests', 'sent by the agent'), ('Quotes', 'collected and compared'), ('Savings', 'on every purchase'), ('Map', 'of suppliers')],
  feats=[('Supplier requests', 'The agent sends requests by specification and reminds those who have not replied'),
         ('Quote collection', 'Price lists and offers in any format parsed into one table'),
         ('Comparison', 'Price, lead time, logistics and terms for every item'),
         ('Supplier map', 'Price versus market against reliability: who is cheaper, who keeps deadlines'),
         ('Attention', 'Who raises prices, who does not reply, who misses deadlines'),
         ('Savings', 'The difference between the chosen and average quote for every procedure and month')],
  ticks=['Procedures and their statuses in one list', 'Supplier base with reply history', 'Items and prices over time', 'Procurement documents saved in the CRM'],
  shots=['zak-obzor', 'zak'],
  faq=[('How does the agent find suppliers?', 'It works with your base and adds new ones from open sources by item list.'),
       ('What format do quotes need to be in?', 'Any: PDF, Excel, an email or a photo. The agent parses items and prices.'),
       ('Who makes the decision?', 'You do. The agent prepares the comparison and a recommendation, the choice stays with the buyer.')]),
 dict(slug='marketing', name='Marketing agent', short='Content and AI visibility', sub='Articles, publishing and visibility in search and AI assistants',
  title='AI marketing agent: content and visibility in search and ChatGPT | MakeBiz',
  desc='AI marketing agent: a content plan from real customer questions, articles and news in English and Russian, publishing, GEO visibility in ChatGPT, Claude and Perplexity, dashboards.',
  h1='AI marketing agent: <span>content and visibility on autopilot</span>',
  lead='The agent plans, writes and publishes expert content for your company every week, then tracks how it performs in search and in AI assistants such as ChatGPT, Claude and Perplexity',
  answer='The MakeBiz marketing agent finds the questions your customers ask in search and in AI chats, drafts articles and news in English and Russian, publishes them on your site with structured data and checks whether ChatGPT, Claude and Perplexity name your brand for your key queries.',
  chips=[('Topics', 'from customer demand'), ('EN · RU', 'articles and news'), ('GEO', 'ChatGPT, Claude, Perplexity'), ('Leads', 'traced to the topic')],
  feats=[('Topic research', 'Finds the questions your customers ask in search and in AI chats, groups them into a content plan and shows the demand behind each topic'),
         ('Articles and news', 'Drafts long-form articles, news and FAQ answers in your tone of voice, in English and Russian, with sources and internal links'),
         ('Publishing', 'Puts approved texts on your site on a schedule, with titles, meta tags, structured data and images, and pings search engines so pages are indexed fast'),
         ('GEO, visibility in AI answers', 'Writes in the answer-first format AI assistants quote, keeps llms.txt and schema up to date and checks whether your brand appears in AI answers'),
         ('Dashboards', 'One screen with traffic, positions, indexed pages, leads from content and AI mentions, so you see which topics bring customers'),
         ('Control stays with you', 'Nothing goes live without approval if you want it that way; every text can be edited before publishing')],
  ticks=['Search impressions and clicks for every site', 'Indexed pages and new pages', 'Mentions in AI assistants by month', 'Leads traced back to the topic that brought them'],
  shots=['mk-search', 'mk-seo', 'mk-geo', 'bi-direct', 'mk-queries'],
  faq=[('Do we have to rebuild the site?', 'No. New content is added to what you have, the main site stays untouched.'),
       ('What is GEO?', 'Visibility in AI assistant answers: so that ChatGPT, Claude and Perplexity name your company when a client asks about your niche.'),
       ('Will the texts be in English?', 'Yes, in English and Russian, in your tone of voice. Every text can be edited before publishing.'),
       ('How do we know it works?', 'Every number in the dashboard has a source: search, site analytics, CRM. You see how many leads and which topic brought them.')]),
 dict(slug='finansy', name='Finance agent', short='Company pulse', sub='Money, profit and risks by line of business',
  title='AI finance agent: company pulse, profit and cash runway | MakeBiz',
  desc='AI finance agent: revenue, profit, costs and balances by line of business on one screen, margin, profitability, cash runway and risk alerts.',
  h1='Finance agent: <span>company money on one screen</span>',
  lead='Revenue, profit, costs and account balances for every line of business. The agent calculates margin and cash runway and flags risks at once',
  answer='The MakeBiz finance agent collects data from banks, accounting and Bitrix24, counts in dirhams, shows revenue, profit, profitability and cash runway for each line of business and warns about risks before they become problems.',
  chips=[('Banks', 'accounting and CRM'), ('Profit', 'by business line'), ('Cash runway', 'in months'), ('Risks', 'visible at once')],
  feats=[('Company pulse', 'Revenue, profit, costs and assets for the month with a forecast'),
         ('By business line', 'Each project and business separately and together'),
         ('Margin and profitability', 'Where you earn and where you break even'),
         ('Cash runway', 'How many months the money lasts at current costs'),
         ('Dividends and payouts', 'How much was withdrawn and how much stays in the company'),
         ('Alerts', 'The agent writes if costs grow faster than revenue, margin drops or a VAT deadline approaches')],
  ticks=['Bank statements and accounting data without manual spreadsheets', 'Monthly dynamics and comparison with last year', 'Transaction reconciliation', 'The same screen for the owner and the CFO'],
  shots=['bi-puls', 'bi-fin'],
  faq=[('Where do the numbers come from?', 'From bank statements, Zoho Books, QuickBooks, Odoo or 1C and Bitrix24. Sources are connected at the start.'),
       ('Does it replace accounting?', 'No, it is a management view of the money for the owner. Accounting keeps working as before.'),
       ('Can it go together with BI dashboards?', 'Yes, finance is usually built together with sales BI in Bitrix24.')]),
]
def agent_url(s): return f'/ai-agents/{s}'
def agent_grid(exclude=None):
    out = ''
    for a in AGENTS:
        if a['slug'] == exclude: continue
        out += (f'<a class="agc" href="{U(agent_url(a["slug"]))}"><img src="/img/agents/{a["shots"][0]}.webp" alt="{esc(SHOT_ALT[a["shots"][0]])}" width="1400" height="685" loading="lazy">'
                f'<span class="agc-tx"><small>{esc(a["short"])}</small><b>{esc(a["name"])}</b><span>{esc(a["sub"])}</span></span></a>')
    return f'<div class="agrid">{out}</div>'

ai_faq = [
    ('How is an AI agent different from a chatbot?', 'A chatbot answers a question and forgets it. An agent has a role, memory and access to your systems: it runs a process to the result, for example takes over a chat if a manager has not replied.'),
    ('How much does AI agent implementation cost?', 'One agent from AED 5,000. Packages: Start AED 5,000, Business AED 10,000, Holding priced individually. Maintenance is 10% of the implementation cost per month. A demo on your process is free.'),
    ('Where do the agents work?', 'In WhatsApp, Telegram and your CRM. The system is deployed on your server, including in the UAE, access stays with you.'),
    ('Which systems do agents work with?', 'Bitrix24, WhatsApp, Telegram, Zoho Books, QuickBooks, Odoo, 1C, bank statements, telephony, Google Ads, Google Analytics, Search Console. Others on request.'),
    ('Do the agents work in English?', 'Yes. Agents talk to clients in their language (English, Russian, Arabic where needed) and count in dirhams.'),
    ('Where do we start?', 'With one agent where there is the most routine or loss: chats, calls, hiring or procurement. We launch, measure and add the next ones.'),
]
ai_body = hero('AI agents · implementation', 'AI agents that <span>work inside your business</span>',
    'Not a chatbot on the website, but a team of digital employees: sales head, liaison, speech analytics, HR, procurement, marketing and finance',
    'MakeBiz Technologies builds and implements AI agents for companies in Dubai and the UAE: the sales head agent runs WhatsApp chats and the sales plan, the liaison agent watches contacts, the calls agent scores every conversation, the HR agent runs first interviews, and the procurement, marketing and finance agents work on BI dashboards. One agent from AED 5,000.',
    ('#form', 'Book a demo'), ('#agenty', 'All agents'), V_AGENTS,
    [('7 agents', 'by department'), ('from AED 5,000', 'one agent'), ('Your server', 'your data'), ('EN · RU', 'working languages')], 'A team of AI agents at work')
ai_body += section('Our agents', 'Our own company is run by these agents: they are built into the CRM, banks, sales, marketing, hiring and procurement. Each can be implemented separately', agent_grid(), id_='agenty')
ai_body += video_block()
ai_body += section('An agent, not a chatbot', '', '''<div class="vs"><div class="vs-col"><h3>Chatbot</h3><ul><li>Answers by script and forgets the conversation</li><li>Lives on the website, does not see the CRM</li><li>Does not finish the task</li><li>Waits until someone comes</li></ul></div>
<div class="vs-col vs-good"><h3>AI agent</h3><ul><li>Remembers the client and the history</li><li>Works in the CRM, WhatsApp, accounting and the bank</li><li>Runs the process to the result</li><li>Notices a problem and brings in a person</li></ul></div></div>''', tone='tint')
ai_body += section('Implementation packages', 'Small entry: one agent, a clear result, then we expand. A demo on your process is free', prices([
    ('Start', 'AED 5,000', 'one-off', ['One agent on a key process', 'CRM and messenger connection', 'Result measurement'], False),
    ('Business', 'AED 10,000', 'one-off', ['A team of agents for several departments', 'Shared data and dashboard', 'Launched one by one'], True),
    ('Holding', 'individual', 'by estimate', ['Several companies and contours', 'Free zone and mainland kept separate', 'Your own server in the UAE'], False),
], 'Agent maintenance is 10% of the implementation cost per month: tuning, troubleshooting and monthly improvements'))
ai_body += section('How we implement', '', steps([
    ('Diagnostic', 'We find the process where an agent pays off fastest'),
    ('Build', 'We set up agent roles, access and integrations on your server, including in the UAE'),
    ('Launch', 'Agents work with the team, we watch the quality'),
    ('Growth', 'We add agents and processes and train employees'),
]), tone='tint')
ai_body += section('Cases', '', case_cards(['haval-vector', 'apartika-crm', 'cdek-b2b']))
ai_body += contract_block() + faq(ai_faq) + form_block('ai-agents', 'We will show agents on your process') + crosslink('bitrix')
page('/ai-agents', 'ai-agents', 'AI agents for business in Dubai and the UAE: sales, calls, HR | MakeBiz',
    'AI agents for business in Dubai and the UAE: sales head on WhatsApp, liaison, call speech analytics, HR, procurement, marketing and finance in Bitrix24. One agent from AED 5,000.',
    'ai', ai_body, [service_ld('AI agent implementation', 'Development and implementation of AI agents for business in the UAE', '/ai-agents', 5000), VIDEO_LD,
                    {"@type": "ItemList", "name": "MakeBiz AI agents", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": a['name'], "url": SITE + en_path(agent_url(a['slug']))} for i, a in enumerate(AGENTS)]}],
    [('/', 'Home'), ('/ai-agents', 'AI agents')], ai_faq)

for a in AGENTS:
    s = a['slug']
    b = hero(f'AI agents · {a["name"]}', a['h1'], a['lead'], a['answer'], ('#form', 'Show it on our process'), (U('/ai-agents') + '#agenty', 'All agents'),
             '<div class="hero-shot">' + shots(a['shots'][:1], SHOT_ALT[a['shots'][0]].split(':')[0]) + '</div>', a['chips'], a['name'])
    b += section('What the agent does', '', cards(a['feats'], 3))
    b += feature('ekrany', 'Cabinet', 'What management <span>sees</span>', 'Screens from our own cabinet on demo data, Russian interface. You get your own numbers', a['ticks'], a['shots'], SHOT_ALT[a['shots'][0]].split(':')[0])
    if s in YT: b += yt_block(s)
    b += section('How we launch', '', steps([
        ('Demo', 'We show the agent on a live system and review your process'),
        ('Connection', 'Access to the CRM, messengers and needed services on your server'),
        ('Setup', 'Rules, criteria and texts for your company'),
        ('Work', 'The agent works with the team, we watch the quality'),
    ]), tone='tint')
    b += section('Other agents', 'Agents work on shared data and reinforce each other', agent_grid(exclude=s))
    b += contract_block() + faq(a['faq']) + form_block('ai-' + s, f'We will show the {a["name"]} on your process') + crosslink('bitrix')
    page(agent_url(s), 'ai-' + s, a['title'], a['desc'], 'ai', b,
        [service_ld(a['name'], a['desc'], agent_url(s))] + ([yt_ld(s)] if s in YT else []),
        [('/', 'Home'), ('/ai-agents', 'AI agents'), (agent_url(s), a['name'])], a['faq'])

# ---------- CASES
used_ind = [k for k, _ in SPHERES if any(k in c['ind'] for c in CASEJ)]
used_prd = [k for k, _ in PRODS if any(k in c['products'] for c in CASEJ)]
chips_ind = '<button type="button" class="fchip on" data-f="ind" data-v="">All industries</button>' + ''.join(
    f'<button type="button" class="fchip" data-f="ind" data-v="{k}">{esc(SPH[k])}<i>{sum(k in c["ind"] for c in CASEJ)}</i></button>' for k in used_ind)
chips_prd = '<button type="button" class="fchip on" data-f="prod" data-v="">All solutions</button>' + ''.join(
    f'<button type="button" class="fchip" data-f="prod" data-v="{k}">{esc(PRD[k])}<i>{sum(k in c["products"] for c in CASEJ)}</i></button>' for k in used_prd)
ks_body = f'''<section class="hero hero-small"><div class="wrap"><div class="eyebrow">Cases</div><h1>MakeBiz <span>cases</span></h1>
<p class="lead">Bitrix24, AI agent and BI analytics projects we have run for years. Choose your industry or the solution you need</p></div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><div class="kfilter gl" data-target="#cases-all">
<div class="kf-row"><span class="kf-t">Industry</span>{chips_ind}</div><div class="kf-row"><span class="kf-t">Solution</span>{chips_prd}</div></div>
<div id="cases-all">{case_cards([c["slug"] for c in CASEJ])}</div><p class="kf-empty" hidden>A case for this industry is in progress. We will tell you about similar projects on a call</p></div></section>
{form_block('keysy', 'Want the same?')}'''
page('/keysy', 'keysy', 'Bitrix24 and AI agent implementation cases by industry | MakeBiz',
    'MakeBiz cases by industry: logistics, manufacturing, automotive, real estate, education. Bitrix24, integrations, BI analytics and AI agents.',
    'keysy', ks_body, [{"@type": "ItemList", "name": "MakeBiz cases", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": notag(c['title']), "url": SITE + en_path('/keysy/' + c['slug'])} for i, c in enumerate(CASEJ)]}],
    [('/', 'Home'), ('/keysy', 'Cases')])
for c in CASEJ:
    s = c['slug']; org = c['client'].split(',')[0]
    h1 = c['title'].replace('<b>', '<span>').replace('</b>', '</span>')
    facts = ([('Result', (c.get('metric_v', '') + ' ' + c.get('metric_t', '')).strip())] if c.get('metric_v') else []) + [('Client', c['client']), ('Region', c['region']), ('What we built', notag(c['built'])), ('Timeline', c['term'])]
    facts_html = ''.join(f'<div class="kfact"><small>{esc(x)}</small><b>{esc(y)}</b></div>' for x, y in facts if y)
    tags = ''.join(f'<a class="ktag" href="{U("/keysy")}#{k}">{esc(SPH.get(k, k))}</a>' for k in c['ind']) + ''.join(f'<span class="ktag ktag-p">{esc(PRD.get(p, p))}</span>' for p in c['products'])
    soft = (c.get('soft') or '').replace('<b>Vector</b>', 'speech analytics').replace('Vector', 'speech analytics')
    body = f'''<section class="hero hero-small"><div class="wrap"><div class="eyebrow">Case · {esc(SPH.get(c["ind"][0], ""))}</div><h1>{h1}</h1>
<p class="lead">{esc(notag(c["lead"]))}</p><div class="ktags">{tags}</div>
<div class="kfacts">{facts_html}</div>
<div class="case-ba kba"><p><span>Before</span>{esc(c["was"])}</p><p><span>After</span>{esc(c["now"])}</p></div></div></section>
<section class="sec" style="padding-top:0"><div class="wrap kbody">
<article class="kart gl"><h2>The task</h2><p>{esc(notag(c["problem"]).replace("Vector", "speech analytics"))}</p><h2>What we did</h2><p>{esc(notag(c["solution"]).replace("Vector", "speech analytics"))}</p><h2>The result</h2><p>{esc(notag(c["result"]).replace("Vector", "speech analytics"))}</p>
{f'<p class="ksoft">{soft}</p>' if soft else ""}</article></div></section>'''
    others = [x['slug'] for x in CASEJ if x['slug'] != s][:3]
    body += section('Other cases', '', case_cards(others)) + form_block('case-' + s, 'Want the same?')
    tt = f'{org} case: {notag(c["title"]).split(":", 1)[-1].strip()}'
    lead = notag(c['lead']).strip()
    if len(lead) > 165: lead = lead[:165].rsplit(' ', 1)[0].rstrip(',:;') + '.'
    page('/keysy/' + s, 'case-' + s, tt + ' | MakeBiz' if len(tt) <= 62 else tt, lead, 'keysy', body,
        [{"@type": "Article", "headline": notag(c['title']), "description": notag(c['lead']), "datePublished": c['date'] + '-01', "dateModified": UPDATED_ISO,
          "author": {"@id": SITE + "/#organization"}, "publisher": {"@id": SITE + "/#organization"}, "about": {"@type": "Organization", "name": org},
          "mainEntityOfPage": SITE + en_path('/keysy/' + s), "inLanguage": "en"}],
        [('/', 'Home'), ('/keysy', 'Cases'), ('/keysy/' + s, org)])

# ---------- PARTNERS
pt_faq = [
    ('How is my client registered?', 'By name and company at the moment of introduction. The client is assigned to you for 6 months and all their payments in that period count as yours.'),
    ('What if the client had already contacted you?', 'Then we say so honestly before work starts. We do not drag out disputes.'),
    ('Do I need to know CRM and AI?', 'No. You introduce, we do all the work from the meeting to implementation.'),
    ('When do I get paid?', 'After the client pays, in dirhams to your account.'),
    ('Is there a contract?', 'Yes, a simple partner agreement with MakeBiz Technologies FZE LLC, for an individual or a company. We send the template before the start.'),
    ('Are there targets or obligations?', 'No. One client a year is fine too.'),
]
pt_body = hero('Partner program', 'Bring businesses and <span>earn from every payment</span>',
    'You recommend, we handle meetings, implementation and support. You get 20% of the first deal and 10% of all client payments for another year',
    'MakeBiz Technologies partner program in the UAE: 20% of the first payment of a referred client and 10% of all their payments for 12 months for Bitrix24, AI agent and BI analytics implementation. Under contract, payouts in dirhams, no selling required.',
    ('#form', 'Become a partner'), ('#calc', 'How much will I earn'),
    '''<div class="pcalc gl" id="calc"><div class="pc-h">Partner calculator</div>
<label>Clients a year <b data-o="n">5</b><input type="range" min="1" max="20" value="5" data-i="n"></label>
<label>Average client budget <b data-o="c">AED 15,000</b><input type="range" min="5000" max="100000" step="5000" value="15000" data-i="c"></label>
<div class="pc-rows"><p><span>From the first payment · 20%</span><b data-o="first">AED 0</b></p><p><span>From repeat payments · 10%</span><b data-o="rep">AED 0</b></p></div>
<div class="pc-tot"><span>Your income for the year</span><b data-o="tot">AED 0</b></div><small>Estimate: a client pays 4 times a year on average, a repeat payment is about half of the first</small></div>''',
    [('20%', 'of the first deal'), ('10%', 'of all payments for a year'), ('6 months', 'client assigned to you'), ('Contract', 'payouts in AED')], 'Partner calculator')
pt_body += section('How to spot our client', 'Introduce us if a business you know has at least one of these. No selling required', cards([
    ('Chaos in sales and tasks', 'Requests and agreements live in heads and WhatsApp chats'), ('No CRM or it does not work', 'Bitrix24 was bought and nobody uses it'),
    ('Requests get lost', 'Clients write in messengers and wait for hours'), ('Many calls without control', 'Nobody knows how managers talk to clients'),
    ('Manual document work', 'VAT invoices, delivery notes and reconciliations by hand'), ('Wants AI but does not know how', 'Heard about agents and does not know where to start'),
], 3))
pt_body += section('From recommendation to payout', 'You bring the client any convenient way, we do the rest', steps([
    ('Share a contact', 'In a channel, social network, website or in person'), ('The lead is assigned to you', 'The request is linked to you, no spreadsheets or disputes'),
    ('We close and implement', 'Meetings, proposal, launch and support on our side'), ('You get paid', 'Accrued when the client pays'),
]), tone='tint')
pt_body += section('A two-way relationship', 'Companies regularly come to us needing company formation, accounting, marketing and lawyers. When a client fits your profile, we pass them to you', cards([
    ('You to us', 'An introduction to a business that needs order in sales, a CRM or AI agents'),
    ('We to you', 'A share of payments and requests for your services: company formation, accounting, marketing, legal'),
], 2))
pt_body += section('How we work with partners', '', cards([
    ('No pressure', 'We do not rush, persuade or set targets'), ('We do not sell to you', 'You are a partner, not a client'),
    ('Transparent', 'You see your deals and accruals'), ('We remember you', 'A client fits your profile, we write to you'), ('Fully official', 'Contract and official payouts'),
], 3, numbered=True))
pt_body += faq(pt_faq) + form_block('partners', 'Become a partner', 'Leave a contact: we send the contract and explain how to pass on clients')
page('/partners', 'partners', 'MakeBiz partner program in the UAE: 20% of the first deal',
    'MakeBiz partner program in the UAE: 20% of the first client payment and 10% of all payments for 12 months for referrals to Bitrix24, AI agents and BI. Under contract.',
    'partners', pt_body, [service_ld('MakeBiz partner program', 'Rewards for referring clients to Bitrix24 and AI agent implementation', '/partners')],
    [('/', 'Home'), ('/partners', 'Partners')], pt_faq)

# ---------- PRICES
ce_faq = [
    ('How much does Bitrix24 implementation cost in the UAE?', f'Standard Bitrix24 CRM setup from AED 10,000, basic launch from 14 days. Work beyond the standard is AED 200 per hour. The Bitrix24 license is paid separately: cloud from {lic(49)} a month billed annually, on-premise from {lic(3590)} a year.'),
    ('How much does Bitrix24 support cost?', 'Monthly hour packages: 5 hours for AED 1,250, 10 hours for AED 2,300, 20 hours for AED 4,200. An hour beyond the package is AED 250.'),
    ('How much do AI agents cost?', 'One agent from AED 5,000. Packages: Start AED 5,000, Business AED 10,000, Holding priced individually. Maintenance is 10% of the implementation cost per month, the demo is free.'),
    ('How much do integrations, WhatsApp and BI cost?', 'Accounting integration (Zoho Books, QuickBooks, Odoo, 1C) from AED 10,000, WhatsApp or another messenger connection AED 500, BI analytics from AED 1,000. The estimate is fixed before start.'),
    ('How much does call speech analytics cost?', 'AED 1,000 a month for 5,000 minutes, AED 1,700 for 10,000 minutes, from AED 4,000 for 30,000 minutes and more.'),
    ('How do we pay?', 'Under contract with MakeBiz Technologies FZE LLC, invoice in dirhams, payment to a UAE company account.'),
]
CE_ROWS = [
    ('Bitrix24', [('Standard CRM setup', 'from AED 10,000', 'launch from 14 days', '/bitrix'),
                  ('Hour of work', 'AED 200', 'complex projects, improvements', '/bitrix'),
                  ('On-premise Bitrix24 implementation', 'by estimate', 'rate AED 200/h', '/bitrix-korobka'),
                  ('WhatsApp or messenger connection', 'AED 500', 'provider subscription separate', '/bitrix-messengers'),
                  ('Accounting integration', 'from AED 10,000', 'Zoho Books, QuickBooks, Odoo, 1C', '/bitrix-integrations'),
                  ('BI analytics', 'from AED 1,000', 'estimate after the metric list', '/bi-analitika')]),
    ('Bitrix24 support', [('5 hours', 'AED 1,250', 'a month', '/bitrix-support'), ('10 hours', 'AED 2,300', 'a month', '/bitrix-support'),
                  ('20 hours', 'AED 4,200', 'a month', '/bitrix-support'), ('Hour beyond package', 'AED 250', 'as used', '/bitrix-support')]),
    (f'Bitrix24 licenses (bitrix24.ae prices as of {PRICE_DATE})', [('Cloud Basic, 5 users', lic(49), 'a month billed annually ($49)', '/bitrix-licenses'),
                  ('Cloud Standard, 50 users', lic(99), 'a month billed annually ($99)', '/bitrix-licenses'),
                  ('Cloud Professional, 100 users', lic(199), 'a month billed annually ($199)', '/bitrix-licenses'),
                  ('Cloud Enterprise, 250 users', lic(399), 'a month billed annually ($399)', '/bitrix-licenses'),
                  ('On-premise Business, 50 users', lic(3590), 'license per year ($3,590)', '/bitrix-korobka'),
                  ('On-premise Enterprise, 1,000+ users', lic(24990), 'license per year ($24,990)', '/bitrix-korobka')]),
    ('AI agents', [('Start package, one agent', 'AED 5,000', 'one-off', '/ai-agents'), ('Business package, team of agents', 'AED 10,000', 'one-off', '/ai-agents'),
                  ('Holding package', 'individual', 'by estimate', '/ai-agents'), ('Agent maintenance', '10%', 'of implementation cost a month', '/ai-agents'),
                  ('Demo on your process', 'free', '30-40 minutes', '/ai-agents')]),
    ('Call speech analytics', [('5,000 minutes', 'AED 1,000', 'a month', '/ai-agents/zvonki'), ('10,000 minutes', 'AED 1,700', 'a month', '/ai-agents/zvonki'),
                  ('from 30,000 minutes', 'from AED 4,000', 'a month', '/ai-agents/zvonki')]),
]
def ce_table():
    out = ''
    for g, rows in CE_ROWS:
        tr = ''.join(f'<tr><td><a href="{U(u)}"><b>{esc(n)}</b></a></td><td class="pt-p">{esc(v)}</td><td>{esc(c)}</td></tr>' for n, v, c, u in rows)
        out += f'<h3 class="ce-h">{esc(g)}</h3><div class="ptw gl"><table class="ptab"><thead><tr><th>Service</th><th>Price</th><th>Terms</th></tr></thead><tbody>{tr}</tbody></table></div>'
    return out
ce_body = f'''<section class="hero hero-small"><div class="wrap"><div class="eyebrow">Prices in AED</div><h1>MakeBiz prices <span>in the UAE</span></h1>
<p class="lead">Bitrix24 implementation and support, licenses, AI agents and speech analytics: all prices in dirhams on one page. We work under contract and fix the estimate before start</p>
<p class="answer">At MakeBiz Technologies standard Bitrix24 CRM setup starts from AED 10,000, an hour of work is AED 200, support from AED 1,250 a month for 5 hours, accounting integration from AED 10,000, WhatsApp AED 500, BI analytics from AED 1,000, one AI agent from AED 5,000. Bitrix24 licenses: cloud from {lic(49)} a month, on-premise from {lic(3590)} a year. Prices as of {PRICE_DATE}.</p></div></section>
<section class="sec" style="padding-top:20px"><div class="wrap">{ce_table()}<p class="note">Service prices exclude licenses and VAT unless stated otherwise. Licenses at vendor prices from bitrix24.ae in US dollars, in dirhams at 3.6725</p></div></section>'''
ce_body += contract_block() + faq(ce_faq) + form_block('ceny', 'We will estimate your project', 'Describe the task, we send an estimate in dirhams with price and timeline')
page('/ceny', 'ceny', 'MakeBiz prices in the UAE: Bitrix24, support and AI agents in AED',
    f'MakeBiz prices in AED as of {PRICE_DATE}: Bitrix24 CRM setup from AED 10,000, support from AED 1,250 a month, AED 200 an hour, AI agent from AED 5,000, licenses from {lic(49)}.',
    'ceny', ce_body, [{"@type": "OfferCatalog", "name": "MakeBiz services in the UAE", "itemListElement": [
        {"@type": "Offer", "name": n, "price": re.sub(r'\D', '', v), "priceCurrency": "AED", "url": SITE + en_path(u), "seller": {"@id": SITE + "/#organization"}}
        for g, rows in CE_ROWS for n, v, c, u in rows if 'AED' in v and re.sub(r'\D', '', v)]}],
    [('/', 'Home'), ('/ceny', 'Pricing')], ce_faq)

# ---------- ABOUT
ab_faq = [
    ('Who is behind MakeBiz Technologies?', 'The company was founded by Anton Chernobaev. The team has 8 years in IT and CRM and more than 150 implementation projects. Legal entity: MakeBiz Technologies FZE LLC, Ajman NuVentures Centre free zone, registration number 2624215090888.'),
    ('Where do you work?', 'In Dubai and across all Emirates: meetings in Dubai or by video call. We work with UAE companies and Russian-speaking businesses worldwide, contract and invoices in dirhams.'),
    ('What languages do you work in?', 'English and Russian. The system, training and documents are prepared in the language of your team.'),
    ('How is MakeBiz different from other integrators?', 'We run our own company with the AI agents and BI cabinet we implement for clients, and do Bitrix24, integrations and AI as one team.'),
    ('Do you help with company formation and visas?', 'No, we are an IT integrator: Bitrix24, AI agents and BI. For company formation we can introduce trusted partners.'),
]
ab_body = hero('About', 'MakeBiz Technologies: <span>Bitrix24 and AI agents in the UAE</span>',
    'We implement Bitrix24 and AI agents so businesses lose less and grow faster. We run on the same agents and dashboards we set up for clients',
    'MakeBiz Technologies FZE LLC (Ajman NuVentures Centre, UAE) was founded by Anton Chernobaev: 8 years in IT and CRM, more than 150 Bitrix24, AI agent and BI analytics projects. We work with companies in Dubai and across the Emirates in English and Russian, MakeBiz clients include CDEK, Unilin and HAVAL.',
    ('#form', 'Discuss a project'), (U('/keysy'), 'Cases'), V_AGENTS,
    [('8 years', 'in IT and CRM'), ('150+', 'projects'), ('FZE LLC', 'UAE company'), ('EN · RU', 'working language')], 'MakeBiz team')
ab_body += section('What we do', '', cards([
    ('Turnkey Bitrix24', f'Cloud and <a href="{U("/bitrix-korobka")}">on-premise</a> Bitrix24 implementation, support, WhatsApp, accounting integrations, licenses and BI'),
    ('AI agents', f'<a href="{U("/ai-agents")}">A team of agents</a>: sales head, liaison, speech analytics, HR, procurement, marketing, finance'),
    ('Analytics', 'BI dashboards on CRM, accounting, bank, telephony and ad data'),
], 3))
ab_body += section('Founder', '', '''<div class="founder gl"><div><h3>Anton Chernobaev</h3><p class="f-role">Founder of MakeBiz, Dubai</p>
<p>Builds the company around two directions: Bitrix24 and AI agents. Personally reviews client processes at the start of projects and shows how MakeBiz itself runs on agents and BI</p>
<p class="f-links"><a href="https://t.me/Anton_MakeBiz" rel="noopener">Telegram</a> · <a href="https://www.youtube.com/channel/UCyXI8U1O215HBGvOwqVjq2Q" rel="noopener">YouTube</a></p></div></div>''', tone='tint')
ab_body += section('Why clients trust us', '', cards([
    ('A UAE company', 'MakeBiz Technologies FZE LLC, Ajman NuVentures Centre, registration no. 2624215090888'),
    ('Under contract', 'Contract, invoices in dirhams, the estimate is fixed before start'),
    ('Projects for years', 'CDEK for the second year, Unilin for the third: we stay on support after launch'),
    ('We run on our own agents', 'MakeBiz finance, sales, hiring, procurement and marketing are run by AI agents'),
], 4))
ab_body += section('Cases', '', case_cards(['cdek-b2b', 'unilin-crm', 'haval-vector']))
ab_body += faq(ab_faq) + form_block('o-kompanii', 'Let us discuss your task')
page('/o-kompanii', 'o-kompanii', 'About MakeBiz Technologies: Bitrix24 and AI agents in the UAE',
    'MakeBiz Technologies FZE LLC: Bitrix24 implementation, AI agents and BI for companies in Dubai and the UAE. Founder Anton Chernobaev, 8 years in IT, 150+ projects.',
    'o-kompanii', ab_body, [{"@type": "AboutPage", "url": SITE + en_path("/o-kompanii"), "about": {"@id": SITE + "/#organization"}},
        {"@type": "Person", "@id": SITE + "/#founder", "name": "Anton Chernobaev", "jobTitle": "Founder", "worksFor": {"@id": SITE + "/#organization"},
         "sameAs": ["https://t.me/Anton_MakeBiz", "https://www.youtube.com/channel/UCyXI8U1O215HBGvOwqVjq2Q"]}],
    [('/', 'Home'), ('/o-kompanii', 'About')], ab_faq)

# ---------- CONTACTS
ct_faq = [
    ('How do I contact MakeBiz Technologies?', f'Phone and WhatsApp {PHONE}, Telegram @{TG}, email {EMAIL}. Or leave a request on the site.'),
    ('Where do meetings take place?', 'In Dubai by arrangement or by video call. We work with companies across all Emirates.'),
    ('How fast do you reply?', 'During business hours within an hour on WhatsApp and Telegram, to a website request within a business day.'),
]
ct_body = f'''<section class="hero hero-small"><div class="wrap"><div class="eyebrow">Contacts</div><h1>Get in touch <span>with us</span></h1>
<p class="lead">We reply within a business day, review the task and propose a solution</p>
<div class="grid g3 contacts">
<a class="card" href="https://wa.me/{WA}"><h3>WhatsApp</h3><p>{PHONE}, quick reply</p></a>
<a class="card" href="tel:{PHONE_TEL}"><h3>Phone</h3><p>{PHONE}</p></a>
<a class="card" href="https://t.me/{TG}"><h3>Telegram</h3><p>@{TG}</p></a>
<a class="card" href="mailto:{EMAIL}"><h3>Email</h3><p>{EMAIL}</p></a>
<a class="card" href="https://t.me/makebizchannel"><h3>Telegram channel</h3><p>@makebizchannel</p></a>
<div class="card"><h3>Company details</h3><p>MakeBiz Technologies FZE LLC, Ajman NuVentures Centre, registration no. 2624215090888, Amber Gem Tower, Ajman, UAE</p></div>
</div></div></section>
<section class="sec"><div class="wrap"><h2>How to reach us faster</h2><div class="grid g3">
<div class="card"><h3>Need an answer today</h3><p>Write on WhatsApp or Telegram @{TG}: we reply within an hour during business hours</p></div>
<div class="card"><h3>Need an estimate</h3><p>Leave a request with the task: we send an estimate in dirhams with price and timeline. Prices for main services on the <a href="{U('/ceny')}">Pricing</a> page</p></div>
<div class="card"><h3>Want to see a live system</h3><p>Book a demo of AI agents and BI: 30-40 minutes, free</p></div></div></div></section>
{faq(ct_faq)}
{form_block('contacts', 'Leave a request')}'''
page('/contacts', 'contacts', 'MakeBiz Technologies contacts: WhatsApp, phone, Telegram',
    f'MakeBiz Technologies contacts in the UAE: WhatsApp and phone {PHONE}, Telegram @{TG}, email {EMAIL}. Bitrix24 and AI agent implementation in Dubai.',
    'contacts', ct_body, [{"@type": "ContactPage", "url": SITE + en_path("/contacts")}], [('/', 'Home'), ('/contacts', 'Contacts')], ct_faq)

# ---------- chrome for the English blog (/en/news), the server wraps it like the Russian journal
CH = os.path.join(ROOT, os.environ.get('MB_OUT', '.'), '_chrome')
os.makedirs(CH, exist_ok=True)
pv = '<div class="pv">Preview of the new site · hidden from search engines · <a href="/en">current site</a></div>' if PREVIEW else ''
open(os.path.join(CH, 'top-en.html'), 'w', encoding='utf-8').write('<div class="flag" aria-hidden="true"><i></i><i></i><i></i></div>' + pv + header('news').replace('href="#form"', 'href="' + U('/contacts') + '#form"'))
open(os.path.join(CH, 'bottom-en.html'), 'w', encoding='utf-8').write(footer().replace('href="#form"', 'href="' + U('/contacts') + '#form"') + f'<script src="{U("/assets/site-en.js")}?v={V}" defer></script>')
open(os.path.join(CH, 'form-en.html'), 'w', encoding='utf-8').write(form_block('', 'Let us discuss your project'))
open(os.path.join(CH, 'head-en.html'), 'w', encoding='utf-8').write(f'<link rel="preload" href="{U("/assets/onest-latin.woff2")}" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="{U("/assets/site.css")}?v={V}">')
print('built EN:', len(built), built)
