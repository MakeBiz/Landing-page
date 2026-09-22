# Страницы-решения под спрос ОАЭ (недвижимость, WhatsApp, VAT и e-invoicing), RU и EN.
# Собираются как bitrix-support: тело из body.<key>.<lang>.html, шапка, форма, подвал и аналитика
# из общих скриптов главной. После сборки: build_faq.py, build_d.py, uae/mobile/bump_attr_v.py
import io, os, json, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
src = io.open(os.path.join(HERE, 'build_support.py'), encoding='utf-8').read()
lib_src = src.split('def page(lang):')[0]          # только помощники, без сборки поддержки
lib = {'__file__': os.path.join(HERE, 'build_support.py')}
exec(compile(lib_src, 'build_support_lib', 'exec'), lib)
ROOT, SITE, STYLE = lib['ROOT'], lib['SITE'], lib['STYLE']
shared_scripts, org_nodes = lib['shared_scripts'], lib['org_nodes']
import re

PAGES = {
 'real-estate': {
  'slug': 'bitrix-real-estate',
  'ru': ('Битрикс24 для агентства недвижимости в Дубае',
         'CRM для брокеров в Дубае: заявки с Property Finder, Bayut и Dubizzle, WhatsApp в карточке, разрешения Trakheesi, формы RERA и комиссии в AED. Настройка от 10 000 AED.',
         'Битрикс24 для агентства недвижимости', 'CRM для агентства недвижимости'),
  'en': ('Bitrix24 for real estate agencies in Dubai',
         'CRM for Dubai brokers: Property Finder, Bayut and Dubizzle leads, WhatsApp in the record, Trakheesi permits, RERA forms and commissions in AED. Setup from AED 10,000.',
         'Bitrix24 for real estate agencies', 'Real estate CRM'),
  'offer': True},
 'whatsapp': {
  'slug': 'bitrix-whatsapp',
  'ru': ('WhatsApp в Битрикс24 для бизнеса в ОАЭ',
         'Подключаем WhatsApp к Битрикс24 через официальный API: один номер на команду, диалоги в карточке CRM, контроль времени ответа, шаблоны и правило 24 часов.',
         'Интеграция WhatsApp с Битрикс24', 'Интеграция WhatsApp и CRM'),
  'en': ('WhatsApp in Bitrix24 for UAE businesses',
         'We connect WhatsApp to Bitrix24 through the official API: one number for the team, chats in the CRM record, response-time control, templates and the 24-hour rule.',
         'WhatsApp integration with Bitrix24', 'WhatsApp CRM integration'),
  'offer': True},
 'vat': {
  'slug': 'bitrix-vat-einvoicing',
  'ru': ('VAT, дирхамы и e-invoicing в Битрикс24 для ОАЭ',
         'Настройка Битрикс24 под VAT 5%, TRN клиента и валюты. Готовим CRM к e-invoicing в ОАЭ: 1 января 2027 для выручки от 50 млн AED, 1 июля 2027 для остальных.',
         'Настройка VAT и подготовка CRM к e-invoicing', 'Настройка CRM под VAT ОАЭ'),
  'en': ('VAT, dirhams and e-invoicing in Bitrix24 for the UAE',
         'Bitrix24 set up for 5% VAT, client TRN and currencies. We prepare the CRM for UAE e-invoicing: 1 January 2027 for revenue of AED 50M+, 1 July 2027 for the rest.',
         'VAT setup and CRM readiness for e-invoicing', 'UAE VAT CRM setup'),
  'offer': False},
 'telephony': {
  'slug': 'bitrix-telephony',
  'ru': ('Телефония в Битрикс24 для компании в ОАЭ',
         'Подключаем телефонию к Битрикс24 в ОАЭ через лицензированного оператора (du, e&) и вашу АТС: звонки из CRM, запись разговоров, задачи на пропущенные.',
         'Подключение телефонии к Битрикс24', 'Интеграция телефонии и CRM'),
  'en': ('Telephony in Bitrix24 for UAE companies',
         'We connect telephony to Bitrix24 in the UAE through a licensed operator (du, e&) and your PBX: calls from the CRM, call recording, tasks for missed calls.',
         'Bitrix24 telephony setup', 'CRM telephony integration'),
  'offer': True},
 'zoho': {
  'slug': 'bitrix-vs-zoho',
  'ru': ('Битрикс24 или Zoho CRM: что выбрать в ОАЭ',
         'Сравнение Битрикс24 и Zoho CRM для компании в ОАЭ: цена за компанию или за пользователя, свой сервер, WhatsApp и телефония, учёт в Zoho Books. Когда лучше каждая система.',
         'Помощь в выборе CRM и внедрение Битрикс24', 'Выбор CRM'),
  'en': ('Bitrix24 vs Zoho CRM: which to choose in the UAE',
         'Bitrix24 vs Zoho CRM for a UAE company: per-company or per-user pricing, own server, WhatsApp and telephony, Zoho Books accounting. When each system fits better.',
         'CRM selection and Bitrix24 implementation', 'CRM selection'),
  'offer': False},
}

def build(key, lang):
    cfg = PAGES[key]; slug = cfg['slug']
    title, desc, svc_name, svc_type = cfg[lang]
    ru = lang == 'ru'
    srcfile = os.path.join(ROOT, 'index.html' if ru else os.path.join('en', 'index.html'))
    srch = io.open(srcfile, encoding='utf-8').read()
    body = io.open(os.path.join(HERE, 'body.%s.%s.html' % (key, lang)), encoding='utf-8').read()
    css = io.open(STYLE, encoding='utf-8').read()
    icons = re.search(r'<!--mb-icons-->[\s\S]*?<!--/mb-icons-->', srch).group(0)
    pre = '' if ru else '/en'
    url = SITE + pre + '/' + slug
    h1 = re.sub(r'<[^>]+>', '', re.search(r'<h1>(.*?)</h1>', body, re.S).group(1))
    crumbs = [('Главная' if ru else 'Home', SITE + ('/' if ru else '/en')),
              ('Внедрение Битрикс24' if ru else 'Bitrix24 implementation', SITE + pre + '/bitrix'), (h1, url)]
    service = {"@type": "Service", "@id": url + "#service", "name": svc_name, "serviceType": svc_type, "url": url,
               "description": desc, "provider": {"@id": SITE + "/#organization"},
               "areaServed": [{"@type": "City", "name": "Dubai"}, {"@type": "Country", "name": "United Arab Emirates"}],
               "availableLanguage": ["ru", "en"]}
    if cfg['offer']:
        service["offers"] = {"@type": "Offer", "url": url, "priceCurrency": "AED", "price": "10000",
                             "name": ("Стандартная настройка CRM Битрикс24" if ru else "Standard Bitrix24 CRM setup"),
                             "priceSpecification": {"@type": "PriceSpecification", "priceCurrency": "AED", "minPrice": "10000"}}
    graph = org_nodes(srch) + [
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": title, "inLanguage": lang, "description": desc,
         "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": SITE + "/#organization"},
         "primaryImageOfPage": SITE + "/og/og-bitrix.jpg", "breadcrumb": {"@id": url + "#breadcrumb"},
         "mainEntity": {"@id": url + "#service"}},
        service,
        {"@type": "BreadcrumbList", "@id": url + "#breadcrumb",
         "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)]},
    ]
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(',', ':'))
    full_title = title + ' | MakeBiz Group'
    head = [
        '<!DOCTYPE html>', '<html lang="%s">' % lang, '<head>', icons,
        '<meta charset="utf-8">', '<meta name="viewport" content="width=device-width, initial-scale=1">',
        '<meta name="color-scheme" content="dark"><meta name="theme-color" content="#07090D">',
        '<!--mb-attr--><script src="/mb-attr.js"></script><!--/mb-attr-->',
        '<title>%s</title>' % full_title, '<meta name="description" content="%s">' % desc,
        '<link rel="canonical" href="%s">' % url,
        '<link rel="alternate" hreflang="ru" href="%s/%s">' % (SITE, slug),
        '<link rel="alternate" hreflang="en" href="%s/en/%s">' % (SITE, slug),
        '<link rel="alternate" hreflang="x-default" href="%s/%s">' % (SITE, slug),
        '<meta property="og:title" content="%s">' % title, '<meta property="og:description" content="%s">' % desc,
        '<meta property="og:url" content="%s">' % url, '<meta property="og:type" content="website">',
        '<meta property="og:site_name" content="MakeBiz Group">',
        '<meta property="og:image" content="%s/og/og-bitrix.jpg">' % SITE,
        '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">',
        '<meta property="og:locale" content="%s">' % ('ru_RU' if ru else 'en_US'),
        '<meta name="twitter:card" content="summary_large_image">',
        '<meta name="twitter:image" content="%s/og/og-bitrix.jpg">' % SITE,
        '<meta name="yandex-verification" content="4da996bcccf8e587" />',
        '<link rel="preconnect" href="https://fonts.googleapis.com">',
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
        '<link href="https://fonts.googleapis.com/css2?family=Oxygen:wght@300;400;700&display=swap" rel="stylesheet">',
        '<!--mb-ld--><script type="application/ld+json">' + ld + '</script><!--/mb-ld-->',
        '<style>html,body{margin:0;padding:0}body{background:#07090D;color:#EAF1FF;'
        'font-family:Oxygen,system-ui,-apple-system,Segoe UI,Roboto,sans-serif;-webkit-font-smoothing:antialiased}',
        css, '#mbabout a{color:#8FE7AE;text-decoration:underline;text-underline-offset:3px}', '</style>', '</head>',
    ]
    tail = ['<script>window.__MBM_ACTIVE="bitrix";</script>',
            '<script>window.__MBCF_REMOVE=false;window.__MBCF_TARGET=null;</script>'] + shared_scripts(srch)
    html = '\n'.join(head) + '\n<body>\n<header></header>\n' + body + '\n<footer></footer>\n' + '\n'.join(tail) + '\n</body>\n</html>\n'
    out = os.path.join(ROOT, slug + '.html') if ru else os.path.join(ROOT, 'en', slug + '.html')
    io.open(out, 'w', encoding='utf-8').write(html)
    print(os.path.relpath(out, ROOT), len(html), 'bytes, scripts:', html.count('<script'), 'title', len(full_title), 'desc', len(desc))

for k in PAGES:
    for l in ('ru', 'en'):
        build(k, l)
