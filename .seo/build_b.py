# Часть B: структурированные данные (JSON-LD) для всех индексируемых страниц
import os
import sys, os, re, json, subprocess, html as H
sys.path.insert(0, os.path.dirname(__file__))
from seo_lib import *
ROOT = sys.argv[1]; os.chdir(ROOT)
ORG = BASE + '/#organization'; SITE = BASE + '/#website'
LOGO = {'@type': 'ImageObject', 'url': BASE + '/favicon.png', 'width': 310, 'height': 310}
T = lambda lang, ru, en: en if lang == 'en' else ru

def org_full(lang):
    return {'@type': 'Organization', '@id': ORG, 'name': 'MakeBiz Group', 'alternateName': ['MakeBiz', 'MakeBiz Technologies'],
      'legalName': 'MakeBiz Technologies FZE LLC', 'url': BASE + '/', 'logo': LOGO, 'image': BASE + '/og-image.jpg',
      'description': T(lang, 'IT-компания в ОАЭ: внедряет AI-агентов, CRM Битрикс24, речевую аналитику звонков Vector, AI-обработку документов IntDoc, BI-аналитику и IT-инфраструктуру для бизнеса.',
                        'UAE IT company implementing AI agents, Bitrix24 CRM, Vector call speech analytics, IntDoc document AI, BI analytics and IT infrastructure for business.'),
      'email': 'info@makebiztechnologies.com', 'telephone': '+971502620927',
      'address': {'@type': 'PostalAddress', 'streetAddress': 'Amber Gem Tower, 26th Floor, Office CWS-1V-226413, Sheikh Khalifa Street', 'addressLocality': 'Ajman', 'addressRegion': 'Ajman', 'addressCountry': 'AE'},
      'areaServed': [{'@type': 'City', 'name': 'Dubai'}, {'@type': 'Country', 'name': 'United Arab Emirates'}, {'@type': 'Country', 'name': 'Russia'}],
      'disambiguatingDescription': T(lang, 'IT-интегратор: CRM Битрикс24, AI-агенты, речевая аналитика и BI. Не занимается регистрацией компаний, визами и лицензиями в ОАЭ.',
                                     'IT integrator: Bitrix24 CRM, AI agents, speech analytics and BI. Not a company formation, visa or licensing service.'),
      'knowsLanguage': ['ru', 'en'],
      'knowsAbout': ['Bitrix24', 'Bitrix24 partner in the UAE', 'CRM implementation', 'Real estate CRM', 'WhatsApp CRM integration', 'UAE VAT and e-invoicing readiness', 'AI agents', 'Business process automation', 'Speech analytics', 'Call analytics', 'Document AI', 'BI analytics', 'IT infrastructure'],
      'identifier': {'@type': 'PropertyValue', 'propertyID': 'Ajman NuVentures Centre registration number', 'value': '2624215090888'},
      'sameAs': ['https://t.me/makebizchannel'],
      'contactPoint': [{'@type': 'ContactPoint', 'contactType': 'sales', 'telephone': '+971502620927', 'email': 'info@makebiztechnologies.com',
                        'url': 'https://t.me/Anton_MakeBiz', 'availableLanguage': ['ru', 'en'], 'areaServed': ['AE', 'RU']}],
      'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': T(lang, 'Услуги MakeBiz', 'MakeBiz services'),
         'itemListElement': [{'@type': 'Offer', 'itemOffered': {'@id': BASE + T(lang, '', '/en') + p + '#service'}} for p in ['/bitrix', '/ai-agents', '/vector', '/intdoc', '/vps']]}}

ORG_C = {'@type': 'Organization', '@id': ORG, 'name': 'MakeBiz Group', 'url': BASE + '/', 'logo': LOGO}

def webpage(url, lang, name, desc, typ='WebPage', extra=None):
    o = {'@type': typ, '@id': url + '#webpage', 'url': url, 'name': name, 'inLanguage': lang, 'isPartOf': {'@id': SITE}, 'about': {'@id': ORG}}
    if desc: o['description'] = desc
    if extra: o.update(extra)
    return o

def crumbs(url, lang, items):
    home = BASE + ('/en' if lang == 'en' else '/')
    els = [{'@type': 'ListItem', 'position': 1, 'name': T(lang, 'Главная', 'Home'), 'item': home}]
    for i, (nm, u) in enumerate(items, 2): els.append({'@type': 'ListItem', 'position': i, 'name': nm, 'item': BASE + u})
    return {'@type': 'BreadcrumbList', '@id': url + '#breadcrumb', 'itemListElement': els}

def offer(lang, url, name, price, monthly=False, minimum=False):
    o = {'@type': 'Offer', 'name': name, 'url': url, 'priceCurrency': 'AED', 'price': price}
    if monthly or minimum:
        ps = {'@type': 'UnitPriceSpecification' if monthly else 'PriceSpecification', 'priceCurrency': 'AED'}
        if minimum: ps['minPrice'] = price
        else: ps['price'] = price
        if monthly: ps.update({'unitCode': 'MON', 'unitText': T(lang, 'месяц', 'month')})
        o['priceSpecification'] = ps
    return o

SVC = {
 'bitrix': (('Внедрение и настройка Битрикс24', 'Внедрение CRM'), ('Bitrix24 implementation and setup', 'CRM implementation'),
    lambda l, u: [offer(l, u, T(l, 'Стандартная настройка CRM Битрикс24', 'Standard Bitrix24 CRM setup'), 10000, minimum=True),
                  offer(l, u, T(l, 'Сопровождение: 5 часов в месяц', 'Support: 5 hours a month'), 1250, monthly=True),
                  offer(l, u, T(l, 'Сопровождение: 10 часов в месяц', 'Support: 10 hours a month'), 2300, monthly=True),
                  offer(l, u, T(l, 'Сопровождение: 20 часов в месяц', 'Support: 20 hours a month'), 4200, monthly=True)]),
 'agents': (('Разработка и внедрение AI-агентов для бизнеса', 'Внедрение AI-агентов'), ('AI agent development and implementation for business', 'AI agents implementation'),
    lambda l, u: [offer(l, u, T(l, 'Команда AI-агентов: внедрение базового ядра', 'AI agent team: core system implementation'), 6000, minimum=True)]),
 'vector': (('Речевая аналитика звонков Vector', 'Речевая аналитика звонков'), ('Vector AI speech analytics for sales calls', 'Call speech analytics'),
    lambda l, u: [offer(l, u, T(l, 'Тариф Старт: 5 000 минут в месяц', 'Start plan: 5,000 minutes a month'), 1000, monthly=True),
                  offer(l, u, T(l, 'Тариф Команда: 10 000 минут в месяц', 'Team plan: 10,000 minutes a month'), 1700, monthly=True),
                  offer(l, u, T(l, 'Тариф Масштаб: от 30 000 минут в месяц', 'Scale plan: from 30,000 minutes a month'), 4000, monthly=True, minimum=True)]),
 'intdoc': (('IntDoc: AI-сравнение поставщиков по документам', 'AI-обработка документов для закупок'), ('IntDoc: AI supplier comparison from documents', 'Document AI for procurement'), None),
 'vps': (('Подбор, развёртывание и сопровождение серверов и VPS', 'IT-инфраструктура'), ('Server and VPS selection, deployment and support', 'IT infrastructure services'), None),
}

def service(key, url, lang, desc):
    (ru, en, offers) = SVC[key]
    name, stype = en if lang == 'en' else ru
    o = {'@type': 'Service', '@id': url + '#service', 'name': name, 'serviceType': stype, 'url': url, 'description': desc,
         'provider': {'@id': ORG}, 'brand': {'@id': ORG},
         'areaServed': [{'@type': 'City', 'name': 'Dubai'}, {'@type': 'Country', 'name': 'United Arab Emirates'}, {'@type': 'Country', 'name': 'Russia'}],
         'availableLanguage': ['ru', 'en']}
    if offers: o['offers'] = offers(lang, url)
    return o

MONTHS_RU = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
MONTHS_EN = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
def parse_date(t):
    t = t.strip().lower().replace(',', '')
    m = re.match(r'(\d{1,2}) (\S+) (\d{4})', t)
    if m and m.group(2) in MONTHS_RU: return '%s-%02d-%02d' % (m.group(3), MONTHS_RU.index(m.group(2)) + 1, int(m.group(1)))
    m = re.match(r'(\S+) (\d{1,2}) (\d{4})', t)
    if m and m.group(1) in MONTHS_EN: return '%s-%02d-%02d' % (m.group(3), MONTHS_EN.index(m.group(1)) + 1, int(m.group(2)))
    m = re.match(r'(\d{1,2}) (\S+) (\d{4})', t)
    if m and m.group(2) in MONTHS_EN: return '%s-%02d-%02d' % (m.group(3), MONTHS_EN.index(m.group(2)) + 1, int(m.group(1)))
    return None

def text(x): return re.sub(r'\s+', ' ', H.unescape(re.sub(r'<[^>]+>', ' ', x))).strip()

def page_url(f):
    p = '/' + f[:-5]
    if p == '/index': return BASE + '/'
    if p.endswith('/index'): p = p[:-6]
    return BASE + p

SERV = {'bitrix': 'bitrix', 'ai-agents': 'agents', 'vector': 'vector', 'intdoc': 'intdoc', 'vps': 'vps'}
CRUMB = {'bitrix': ('Битрикс24', 'Bitrix24'), 'ai-agents': ('AI-агенты', 'AI agents'), 'vector': ('Vector', 'Vector'), 'intdoc': ('IntDoc', 'IntDoc'),
         'vps': ('Серверы', 'Servers'), 'keysy': ('Кейсы', 'Case studies'), 'news': ('Новости', 'News'), 'contacts': ('Контакты', 'Contacts'),
         'partners': ('Партнёрам', 'Partners'), 'privacy': ('Политика конфиденциальности', 'Privacy Policy'), 'terms': ('Пользовательское соглашение', 'Terms of Use')}

def load_cases(lang):
    out = subprocess.check_output(['node', '-e', "const vm=require('vm');const c={window:{}};vm.createContext(c);vm.runInContext(require('fs').readFileSync(process.argv[1],'utf8'),c);console.log(JSON.stringify(c.window.MB_CASES))",
                                   ('en/' if lang == 'en' else '') + 'keysy/cases-data.js']).decode()
    return json.loads(out)

def graph_for(f, s):
    lang = 'en' if f.startswith('en/') else 'ru'
    pre = '/en' if lang == 'en' else ''
    url = page_url(f)
    title = re.search(r'<title>(.*?)</title>', s, re.S); title = H.unescape(title.group(1)).strip() if title else ''
    desc = get_meta(s, 'description')
    base = f[3:] if lang == 'en' else f
    key = base[:-5]
    g = []
    if key == 'index':
        g = [org_full(lang), {'@type': 'WebSite', '@id': SITE, 'url': BASE + '/', 'name': 'MakeBiz Group', 'alternateName': 'MakeBiz', 'inLanguage': ['ru', 'en'], 'publisher': {'@id': ORG}},
             webpage(url, lang, title, desc, extra={'primaryImageOfPage': BASE + '/og-image.jpg'})]
    elif key in SERV:
        g = [ORG_C, webpage(url, lang, title, desc, extra={'breadcrumb': {'@id': url + '#breadcrumb'}, 'mainEntity': {'@id': url + '#service'}}),
             crumbs(url, lang, [(CRUMB[key][lang == 'en'], pre + '/' + key)]), service(SERV[key], url, lang, desc)]
    elif key == 'calculator-agents':
        en = lang == 'en'
        nm = 'AI agents cost calculator' if en else 'Калькулятор стоимости AI-агентов'
        g = [ORG_C, webpage(url, lang, title, desc, extra={'breadcrumb': {'@id': url + '#breadcrumb'}}),
             crumbs(url, lang, [('AI agents' if en else 'AI-агенты', pre + '/ai-agents'), (nm, pre + '/calculator-agents')]),
             {'@type': 'WebApplication', '@id': url + '#app', 'name': nm, 'url': url, 'applicationCategory': 'BusinessApplication',
              'operatingSystem': 'Any', 'inLanguage': lang, 'provider': {'@id': ORG},
              'offers': {'@type': 'AggregateOffer', 'priceCurrency': 'AED', 'lowPrice': 6000, 'highPrice': 25000, 'offerCount': 3,
                         'description': ('Start, Business and Holding implementation plans' if en
                                         else 'Тарифы внедрения Старт, Бизнес и Холдинг')}}]
    elif key == 'keysy':
        cs = load_cases(lang)
        items = [{'@type': 'ListItem', 'position': i, 'url': BASE + pre + '/keysy/' + c['slug'], 'name': text(c['title'])} for i, c in enumerate(cs, 1)]
        g = [ORG_C, webpage(url, lang, title, desc, 'CollectionPage', {'breadcrumb': {'@id': url + '#breadcrumb'},
             'mainEntity': {'@type': 'ItemList', 'numberOfItems': len(items), 'itemListElement': items}}),
             crumbs(url, lang, [(CRUMB['keysy'][lang == 'en'], pre + '/keysy')])]
    elif key == 'news':
        arts = []
        for m in re.finditer(r'href="(' + re.escape(pre) + r'/news/[a-z0-9-]+)"', s):
            u = m.group(1)
            if u not in arts: arts.append(u)
        items = []
        for i, u in enumerate(arts, 1):
            af = u.lstrip('/') + '.html'
            nm = text(re.search(r'<h1[^>]*>(.*?)</h1>', rd(af), re.S).group(1)) if os.path.exists(af) else u
            items.append({'@type': 'ListItem', 'position': i, 'url': BASE + u, 'name': nm})
        g = [ORG_C, webpage(url, lang, title, desc, 'CollectionPage', {'breadcrumb': {'@id': url + '#breadcrumb'},
             'mainEntity': {'@type': 'ItemList', 'numberOfItems': len(items), 'itemListElement': items}}),
             crumbs(url, lang, [(CRUMB['news'][lang == 'en'], pre + '/news')])]
    elif key.startswith('news/'):
        h1 = text(re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S).group(1))
        when = re.search(r'<span class="when">(.*?)</span>', s)
        d = parse_date(text(when.group(1))) if when else None
        img = get_meta(s, 'og:image', 'property')
        art = {'@type': 'NewsArticle', '@id': url + '#article', 'headline': h1[:110], 'name': h1, 'description': desc, 'url': url,
               'mainEntityOfPage': {'@id': url + '#webpage'}, 'inLanguage': lang, 'author': {'@id': ORG}, 'publisher': {'@id': ORG}}
        if d: art.update({'datePublished': d, 'dateModified': d})
        if img: art['image'] = {'@type': 'ImageObject', 'url': img, 'width': 1600, 'height': 900}
        g = [ORG_C, webpage(url, lang, title, desc, extra={'breadcrumb': {'@id': url + '#breadcrumb'}}),
             crumbs(url, lang, [(CRUMB['news'][lang == 'en'], pre + '/news'), (h1, pre + '/' + key)]), art]
    elif key == 'contacts':
        g = [org_full(lang), webpage(url, lang, title, desc, 'ContactPage', {'breadcrumb': {'@id': url + '#breadcrumb'}}),
             crumbs(url, lang, [(CRUMB['contacts'][lang == 'en'], pre + '/contacts')])]
    elif key in ('partners', 'privacy', 'terms'):
        g = [ORG_C, webpage(url, lang, title, desc, extra={'breadcrumb': {'@id': url + '#breadcrumb'}}),
             crumbs(url, lang, [(CRUMB[key][lang == 'en'], pre + '/' + key)])]
        for o in get_lds(s):   # сохраняем готовый FAQPage
            if o.get('@type') == 'FAQPage':
                o = dict(o); o.pop('@context', None); g.append(o)
    else:
        return None
    return {'@context': 'https://schema.org', '@graph': g}

SKIP = ('.', 'node_modules', '_')
files = []
for root, dirs, fs in os.walk('.'):
    dirs[:] = [d for d in dirs if not d.startswith(SKIP)]
    for f in fs:
        if f.endswith('.html'):
            files.append(os.path.relpath(os.path.join(root, f), '.'))
files = sorted(files)  # было git ls-files: в папке STAGE нет репозитория
done = []
for f in files:
    if f in ('404.html', 'calculator-agents-app.html') or f.endswith('keysy/case.html'): continue
    s = rd(f)
    g = graph_for(f, s)
    if not g: continue
    fn = lambda h: replace_lds(h, [g])
    s2 = fn(s)
    if tpl_get(s2):
        m = tpl_get(s2); raw = m.group(2); Td, pos = json_str_map(raw)
        ha = Td.find('>', Td.find('<head')) + 1; he = Td.find('</head>')
        T2 = fn(Td); he2 = T2.find('</head>')
        assert T2[:ha] == Td[:ha] and T2[he2:] == Td[he:]
        new_raw = raw[:pos[ha]] + jenc(T2[ha:he2]) + raw[pos[he]:]
        assert json.loads(new_raw) == T2
        s2 = s2[:m.start(2)] + new_raw + s2[m.end(2):]
    wr(f, s2); done.append(f + ' ' + ','.join(x['@type'] for x in g['@graph']))
print('\n'.join(done))
