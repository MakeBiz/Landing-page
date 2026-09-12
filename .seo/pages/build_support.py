# Сборка страниц «О компании» из общих скриптов сайта (шапка, форма, подвал, аналитика).
import re, json, io, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HERE = os.path.dirname(os.path.abspath(__file__))
STYLE = os.path.join(os.path.dirname(HERE), 'company', 'style.css')
SITE = 'https://makebiztechnologies.com'

KEEP = ['__mbmDone', '__mbcfDone', 'Лучи', 'единый подвал', '__mbYM=function', '__mbCookieInit',
        'googletagmanager.com/gtag', "gtag('js'", 'MakeBiz — чистка', 'переключатель языков',
        'навигация по языку', 'призывы', '__mbTopDone']
DROP = ['<script>window.__MBM_ACTIVE', '<script>window.__MBCF_REMOVE', 'точечные правки главной', '__mbCasesBlock',
        'cases-data.js', 'cases-engine.js', '__bundler', 'mb-attr.js']

def shared_scripts(src):
    out = []
    for b in re.findall(r'<script[^>]*>[\s\S]*?</script>', src):
        if any(d in b for d in DROP):
            continue
        if any(k in b for k in KEEP):
            out.append(b)
    return out

def org_nodes(src):
    m = re.search(r'<!--mb-ld-->\s*<script type="application/ld\+json">([\s\S]*?)</script>', src)
    g = json.loads(m.group(1))['@graph']
    return [n for n in g if n.get('@type') in ('Organization', 'WebSite')]

def page(lang):
    srcfile = os.path.join(ROOT, 'index.html' if lang == 'ru' else os.path.join('en', 'index.html'))
    src = io.open(srcfile, encoding='utf-8').read()
    body = io.open(os.path.join(HERE, 'body.support.%s.html' % lang), encoding='utf-8').read()
    css = io.open(STYLE, encoding='utf-8').read()
    icons = re.search(r'<!--mb-icons-->[\s\S]*?<!--/mb-icons-->', src).group(0)

    if lang == 'ru':
        url = SITE + '/bitrix-support'
        title = 'Техподдержка Битрикс24 в Дубае и ОАЭ: пакеты часов'
        desc = ('Сопровождение Битрикс24 в ОАЭ: процессы, права, интеграции и отчёты. Пакеты 5, 10 и 20 часов '
                'в месяц за 1 250, 2 300 и 4 200 AED, час сверх пакета 250 AED.')
        crumbs = [('Главная', SITE + '/'), ('Внедрение Битрикс24', SITE + '/bitrix'), ('Техподдержка Битрикс24', url)]
        locale = 'ru_RU'
    else:
        url = SITE + '/en/bitrix-support'
        title = 'Bitrix24 support in Dubai and the UAE: hour packages'
        desc = ('Bitrix24 maintenance in the UAE: processes, permissions, integrations and reports. Packages of 5, '
                '10 and 20 hours a month for AED 1,250, 2,300 and 4,200, extra hour AED 250.')
        crumbs = [('Home', SITE + '/en'), ('Bitrix24 implementation', SITE + '/en/bitrix'), ('Bitrix24 support', url)]
        locale = 'en_US'

    graph = org_nodes(src) + [
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": title,
         "inLanguage": lang, "description": desc,
         "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": SITE + "/#organization"},
         "primaryImageOfPage": SITE + "/og/og-bitrix.jpg",
         "breadcrumb": {"@id": url + "#breadcrumb"}},
        {"@type": "Service", "@id": url + "#service",
         "name": ("Техподдержка и сопровождение Битрикс24" if lang == 'ru' else "Bitrix24 support and maintenance"),
         "serviceType": ("Техподдержка Битрикс24" if lang == 'ru' else "Bitrix24 support"),
         "provider": {"@id": SITE + "/#organization"},
         "areaServed": [{"@type": "Country", "name": "United Arab Emirates"}, {"@type": "City", "name": "Dubai"}],
         "offers": [
             {"@type": "Offer", "name": ("5 часов в месяц" if lang == 'ru' else "5 hours a month"),
              "price": "1250", "priceCurrency": "AED", "url": url},
             {"@type": "Offer", "name": ("10 часов в месяц" if lang == 'ru' else "10 hours a month"),
              "price": "2300", "priceCurrency": "AED", "url": url},
             {"@type": "Offer", "name": ("20 часов в месяц" if lang == 'ru' else "20 hours a month"),
              "price": "4200", "priceCurrency": "AED", "url": url}]},
        {"@type": "BreadcrumbList", "@id": url + "#breadcrumb",
         "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u}
                             for i, (n, u) in enumerate(crumbs)]},
    ]
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(',', ':'))

    head = [
        '<!DOCTYPE html>', '<html lang="%s">' % lang, '<head>', icons,
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        '<meta name="color-scheme" content="dark"><meta name="theme-color" content="#07090D">',
        '<!--mb-attr--><script src="/mb-attr.js"></script><!--/mb-attr-->',
        '<title>%s</title>' % title,
        '<meta name="description" content="%s">' % desc,
        '<link rel="canonical" href="%s">' % url,
        '<link rel="alternate" hreflang="ru" href="%s/bitrix-support">' % SITE,
        '<link rel="alternate" hreflang="en" href="%s/en/bitrix-support">' % SITE,
        '<link rel="alternate" hreflang="x-default" href="%s/bitrix-support">' % SITE,
        '<meta property="og:title" content="%s">' % title,
        '<meta property="og:description" content="%s">' % desc,
        '<meta property="og:url" content="%s">' % url,
        '<meta property="og:type" content="website">',
        '<meta property="og:site_name" content="MakeBiz Group">',
        '<meta property="og:image" content="%s/og/og-bitrix.jpg">' % SITE,
        '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">',
        '<meta property="og:locale" content="%s">' % locale,
        '<meta name="twitter:card" content="summary_large_image">',
        '<meta name="twitter:image" content="%s/og/og-bitrix.jpg">' % SITE,
        '<meta name="yandex-verification" content="4da996bcccf8e587" />',
        '<link rel="preconnect" href="https://fonts.googleapis.com">',
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
        '<link href="https://fonts.googleapis.com/css2?family=Oxygen:wght@300;400;700&display=swap" rel="stylesheet">',
        '<!--mb-ld--><script type="application/ld+json">' + ld + '</script><!--/mb-ld-->',
        '<style>html,body{margin:0;padding:0}body{background:#07090D;color:#EAF1FF;'
        'font-family:Oxygen,system-ui,-apple-system,Segoe UI,Roboto,sans-serif;-webkit-font-smoothing:antialiased}',
        css, '</style>', '</head>',
    ]
    tail = ['<script>window.__MBM_ACTIVE="";</script>',
            '<script>window.__MBCF_REMOVE=false;window.__MBCF_TARGET=null;</script>'] + shared_scripts(src)
    return '\n'.join(head) + '\n<body>\n<header></header>\n' + body + '\n<footer></footer>\n' + '\n'.join(tail) + '\n</body>\n</html>\n'

for lang, out in (('ru', 'bitrix-support.html'), ('en', os.path.join('en', 'bitrix-support.html'))):
    p = os.path.join(ROOT, out)
    html = page(lang)
    io.open(p, 'w', encoding='utf-8').write(html)
    print(out, len(html), 'bytes, scripts:', html.count('<script'))
