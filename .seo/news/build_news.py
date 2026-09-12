#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Сборка новости makebiztechnologies.com из JSON в две страницы (RU и EN)
плюс карточки в ленты /news и /en/news.

Запуск из корня репозитория:
    python3 .seo/news/build_news.py . <slug> [--lead]

--lead делает новость «лидом» ленты (крупная карточка сверху),
прежний лид уезжает первой карточкой в сетку.

Данные статьи: .seo/news/articles/<slug>.json
Донор вёрстки: news/chto-takoe-ai-agent-i-chem-otlichaetsya-ot-chat-bota.html
Скрипт идемпотентный: повторный запуск перезаписывает страницы и карточки.
После него обязательно: build_a.py, build_b.py, build_d.py.
"""
import io, json, os, re, sys

SITE = 'https://makebiztechnologies.com'
DONOR = 'chto-takoe-ai-agent-i-chem-otlichaetsya-ot-chat-bota'

# рубрика: (цвет фона плашки, цвет текста плашки, подпись RU, подпись EN, rgb для градиента плитки)
RUBRICS = {
    'ai':     ('--r-ai',     '#0A0820', 'Искусственный интеллект', 'Artificial intelligence', '122,108,247'),
    'agents': ('--r-agents', '#04230F', 'AI-агенты',               'AI agents',               '22,193,90'),
    'crm':    ('--r-crm',    '#04122E', 'CRM и продажи',           'CRM and sales',           '76,141,255'),
    'auto':   ('--r-auto',   '#00201F', 'Автоматизация',           'Automation',              '0,194,199'),
    'it':     ('--r-it',     '#1E1400', 'IT и серверы',            'IT and servers',          '224,161,0'),
    'biz':    ('--r-biz',    '#2A0710', 'Бизнес',                  'Business',                '255,107,138'),
}

MONTHS_RU = ['января','февраля','марта','апреля','мая','июня','июля','августа','сентября','октября','ноября','декабря']
MONTHS_EN = ['January','February','March','April','May','June','July','August','September','October','November','December']


def rd(p):
    return io.open(p, encoding='utf-8').read()


def wr(p, s):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    io.open(p, 'w', encoding='utf-8').write(s)


def date_ru(iso):
    y, m, d = iso.split('-')
    return '%d %s %s' % (int(d), MONTHS_RU[int(m) - 1], y)


def date_en(iso):
    y, m, d = iso.split('-')
    return '%d %s %s' % (int(d), MONTHS_EN[int(m) - 1], y)


def short_ru(iso):
    y, m, d = iso.split('-')
    return '%d %s' % (int(d), MONTHS_RU[int(m) - 1])


def short_en(iso):
    y, m, d = iso.split('-')
    return '%d %s' % (int(d), MONTHS_EN[int(m) - 1])


def plural_ru(n, one, few, many):
    n = abs(int(n)); d10, d100 = n % 10, n % 100
    if d10 == 1 and d100 != 11:
        return one
    if 2 <= d10 <= 4 and not (12 <= d100 <= 14):
        return few
    return many


def read_ru(n, short=False):
    """«Читать 4 минуты» и «4 минуты» для карточки."""
    w = plural_ru(n, 'минута', 'минуты', 'минут') if short else plural_ru(n, 'минуту', 'минуты', 'минут')
    return ('%d %s' % (n, w)) if short else ('Читать %d %s' % (n, w))


def sub1(s, pat, new, what):
    """Замена ровно одного вхождения, иначе падаем с понятной ошибкой."""
    n = len(re.findall(pat, s, re.S))
    if n != 1:
        raise SystemExit('НЕ СОБРАЛОСЬ: %s найдено %d раз (ожидалась 1)' % (what, n))
    return re.sub(pat, lambda m: new, s, count=1, flags=re.S)


def build_ld(a, lang):
    L = a[lang]
    path = ('/news/' if lang == 'ru' else '/en/news/') + a['slug']
    url = SITE + path
    img = SITE + '/news/' + a['cover'] + '.jpg'
    home = 'Главная' if lang == 'ru' else 'Home'
    news = 'Новости' if lang == 'ru' else 'News'
    home_url = SITE + '/' if lang == 'ru' else SITE + '/en'
    news_url = SITE + ('/news' if lang == 'ru' else '/en/news')
    org = {"@id": SITE + "/#organization"}
    g = [
        {"@type": "Organization", "@id": SITE + "/#organization", "name": "MakeBiz Group", "url": SITE + "/",
         "logo": {"@type": "ImageObject", "url": SITE + "/favicon.png", "width": 310, "height": 310}},
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": L['title'] + ' · MakeBiz',
         "inLanguage": lang, "isPartOf": {"@id": SITE + "/#website"}, "about": org,
         "description": L['desc'], "breadcrumb": {"@id": url + "#breadcrumb"}},
        {"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": home, "item": home_url},
            {"@type": "ListItem", "position": 2, "name": news, "item": news_url},
            {"@type": "ListItem", "position": 3, "name": L['title'], "item": url}]},
        {"@type": "NewsArticle", "@id": url + "#article", "headline": L['title'], "name": L['title'],
         "description": L['desc'], "url": url, "mainEntityOfPage": {"@id": url + "#webpage"},
         "inLanguage": lang, "author": org, "publisher": org,
         "datePublished": a['date'], "dateModified": a.get('modified', a['date']),
         "image": {"@type": "ImageObject", "url": img, "width": 1600, "height": 900}},
    ]
    return ('<!--mb-ld--><script type="application/ld+json">'
            + json.dumps({"@context": "https://schema.org", "@graph": g}, ensure_ascii=False, separators=(',', ':'))
            + '</script><!--/mb-ld-->')


def render_page(repo, a, lang):
    donor = os.path.join(repo, 'news' if lang == 'ru' else 'en/news', DONOR + '.html')
    h = rd(donor)
    L = a[lang]
    ru_url = SITE + '/news/' + a['slug']
    en_url = SITE + '/en/news/' + a['slug']
    url = ru_url if lang == 'ru' else en_url
    img = SITE + '/news/' + a['cover'] + '.jpg'
    rub = RUBRICS[a['cat']]
    tag = rub[2] if lang == 'ru' else rub[3]
    when = date_ru(a['date']) if lang == 'ru' else date_en(a['date'])
    rt = read_ru(a['read']) if lang == 'ru' else ('%d min read' % a['read'])
    alt = a.get('cover_alt_' + lang, '')

    h = sub1(h, r'<title>[^<]*</title>', '<title>%s · MakeBiz</title>' % L['title'], 'title')
    h = sub1(h, r'<link rel="canonical"[^>]*>', '<link rel="canonical" href="%s">' % url, 'canonical')
    h = sub1(h, r'<link rel="alternate" hreflang="ru"[^>]*>',
             '<link rel="alternate" hreflang="ru" href="%s">' % ru_url, 'hreflang ru')
    h = sub1(h, r'<link rel="alternate" hreflang="en"[^>]*>',
             '<link rel="alternate" hreflang="en" href="%s">' % en_url, 'hreflang en')
    h = sub1(h, r'<link rel="alternate" hreflang="x-default"[^>]*>',
             '<link rel="alternate" hreflang="x-default" href="%s">' % ru_url, 'hreflang x-default')
    h = sub1(h, r'<meta name="description" content="[^"]*">',
             '<meta name="description" content="%s">' % L['desc'], 'description')
    h = sub1(h, r'<meta property="og:title" content="[^"]*">',
             '<meta property="og:title" content="%s · MakeBiz">' % L['title'], 'og:title')
    h = sub1(h, r'<meta property="og:description" content="[^"]*">',
             '<meta property="og:description" content="%s">' % L['desc'], 'og:description')
    h = sub1(h, r'<meta property="og:url" content="[^"]*">',
             '<meta property="og:url" content="%s">' % url, 'og:url')
    h = sub1(h, r'<meta property="og:image" content="[^"]*">',
             '<meta property="og:image" content="%s">' % img, 'og:image')
    h = re.sub(r'<meta name="twitter:image" content="[^"]*">',
               '<meta name="twitter:image" content="%s">' % img, h)
    h = re.sub(r'<meta name="twitter:title" content="[^"]*">',
               '<meta name="twitter:title" content="%s · MakeBiz">' % L['title'], h)
    h = re.sub(r'<meta name="twitter:description" content="[^"]*">',
               '<meta name="twitter:description" content="%s">' % L['desc'], h)
    h = sub1(h, r'<!--mb-ld-->.*?<!--/mb-ld-->', build_ld(a, lang), 'JSON-LD')

    n = len(re.findall(r'<div class="crumbs">.*?</div>', h, re.S))
    if n != 1:
        raise SystemExit('НЕ СОБРАЛОСЬ: хлебные крошки найдены %d раз' % n)
    h = re.sub(r'(<div class="crumbs">.*?/\s*)[^<]*(</div>)',
               lambda m: m.group(1) + L['title'] + m.group(2), h, count=1, flags=re.S)
    h = sub1(h, r'<span class="tagr">[^<]*</span>', '<span class="tagr">%s</span>' % tag, 'плашка рубрики')
    h = sub1(h, r'<span class="when">[^<]*</span>', '<span class="when">%s</span>' % when, 'дата')
    h = sub1(h, r'<span class="rt">[^<]*</span>', '<span class="rt">%s</span>' % rt, 'время чтения')
    h = sub1(h, r'<h1 class="art-title">.*?</h1>', '<h1 class="art-title">%s</h1>' % L['title'], 'H1')
    h = sub1(h, r'<div class="cover">.*?</div>',
             '<div class="cover">\n      <img src="/news/%s.webp" alt="%s" width="1536" height="1024" loading="eager">\n    </div>'
             % (a['cover'], alt), 'обложка')
    # подзаголовки и списки внутри статьи: в доноре стилей нет, добавляем один раз
    if 'mb-artx' not in h:
        style = ('<style id="mb-artx">.art h2{font:700 20px/1.35 Oxygen;color:#F2F6FC;'
                 'letter-spacing:-.01em;margin:32px 0 14px}'
                 '.art ul{margin:0 0 20px;padding-left:20px}'
                 '.art li{font:300 16.5px/1.78 Oxygen;color:#D7E1EF;margin:0 0 8px}'
                 '.art b{color:#F2F6FC;font-weight:700}'
                 '.art a{color:#6AA6FF}</style>')
        h = h.replace('</head>', style + '</head>', 1)
    h = sub1(h, r'<div class="art">.*?(?=<div class="artcta">)',
             '<div class="art">\n%s\n    </div>\n\n    ' % L['body'], 'тело статьи')
    h = sub1(h, r'<div class="artcta">.*?(?=<a class="back")',
             '<div class="artcta">\n      <div><b>%s</b><p>%s</p></div>\n      <a class="btn p" href="https://t.me/Anton_MakeBiz" target="_blank" rel="noopener">%s</a>\n    </div>\n\n    '
             % (L['cta_b'], L['cta_p'], 'Обсудить задачу' if lang == 'ru' else 'Discuss a task'), 'блок призыва')
    return h


def card(a, lang, lead=False):
    L = a[lang]
    rub = RUBRICS[a['cat']]
    var, ink = rub[0], rub[1]
    tag = rub[2] if lang == 'ru' else rub[3]
    rgb = rub[4]
    href = ('/news/' if lang == 'ru' else '/en/news/') + a['slug']
    when = short_ru(a['date']) if lang == 'ru' else short_en(a['date'])
    rt = read_ru(a['read']) if lang == 'ru' else ('%d min read' % a['read'])
    rt_card = read_ru(a['read'], short=True) if lang == 'ru' else ('%d min' % a['read'])
    tile = ('<div class="tile" style="background:linear-gradient(150deg,rgba(%s,.2),rgba(%s,.03))">'
            '<img class="tile-bg" src="/news/%s.webp" alt="" aria-hidden="true" loading="lazy">'
            '<div class="grid"></div><span class="mark" style="color:var(%s)">%s</span></div>'
            % (rgb, rgb, a['cover'], var, tag))
    meta = ('<div class="meta"><span class="tagr" style="color:%s;background:var(%s)">%s</span>'
            '<span class="when">%s</span></div>' % (ink, var, tag, when))
    if lead:
        return ('<a class="lead" id="n-%s" href="%s" data-r="%s" data-date="%s">\n    %s\n    '
                '<div class="body">\n      %s\n      <h2>%s</h2>\n      <p>%s</p>\n      '
                '<div class="rt">%s</div>\n    </div>\n  </a>'
                % (a['date'], href, a['cat'], a['date'], tile, meta, L['title'], L['desc'], rt))
    return ('<a id="n-%s" class="card" href="%s" data-r="%s" data-date="%s">\n      %s\n      '
            '<div class="body">%s\n        <h3>%s</h3>\n        <p>%s</p>\n        '
            '<div class="rt">%s</div></div>\n    </a>'
            % (a['date'], href, a['cat'], a['date'], tile, meta, L['title'], L['desc'], rt_card))


def drop_existing(html, slug, lang):
    """Убрать карточку и лид этой же статьи, чтобы повторный запуск не плодил дубли."""
    href = ('/news/' if lang == 'ru' else '/en/news/') + slug
    pat = r'<a[^>]*href="' + re.escape(href) + r'"[^>]*>.*?</a>\s*'
    return re.sub(pat, '', html, flags=re.S)


LEADMARK = '<!--MB-LEAD-SLOT-->'


def to_card(lead_html):
    """Прежний лид превращаем в обычную карточку сетки."""
    c = lead_html.replace('<a class="lead" id=', '<a class="card" id=', 1)
    c = re.sub(r'<h2>(.*?)</h2>', r'<h3>\1</h3>', c, flags=re.S)
    return c.strip()


def put_into_feed(repo, a, lang, lead):
    """Идемпотентно кладёт статью в ленту. Повторный запуск не плодит дубли и не теряет лид."""
    p = os.path.join(repo, 'news.html' if lang == 'ru' else 'en/news.html')
    h = rd(p)
    href = ('/news/' if lang == 'ru' else '/en/news/') + a['slug']
    anchor = '<div class="grid3" id="feed">'
    if anchor not in h:
        raise SystemExit('НЕ СОБРАЛОСЬ: в %s нет контейнера ленты' % p)

    m = re.search(r'<a class="lead".*?</a>', h, re.S)
    old_lead = m.group(0) if m else ''
    old_is_ours = bool(old_lead) and ('href="%s"' % href) in old_lead
    if m:
        h = h[:m.start()] + LEADMARK + h[m.end():]
    else:
        h = h.replace(anchor, LEADMARK + '\n\n  ' + anchor, 1)

    h = drop_existing(h, a['slug'], lang)

    if lead:
        h = h.replace(LEADMARK, card(a, lang, lead=True), 1)
        if old_lead and not old_is_ours:
            h = h.replace(anchor, anchor + '\n    ' + to_card(old_lead), 1)
    else:
        if old_is_ours:
            h = h.replace(LEADMARK, old_lead, 1)
        else:
            h = h.replace(LEADMARK, old_lead, 1)
            h = h.replace(anchor, anchor + '\n    ' + card(a, lang), 1)
    wr(p, h)
    return p


def main():
    if len(sys.argv) < 3:
        raise SystemExit('использование: build_news.py <repo> <slug> [--lead]')
    repo, slug = sys.argv[1], sys.argv[2]
    lead = '--lead' in sys.argv
    a = json.load(io.open(os.path.join(repo, '.seo/news/articles', slug + '.json'), encoding='utf-8'))
    a['slug'] = slug
    if a['cat'] not in RUBRICS:
        raise SystemExit('НЕ СОБРАЛОСЬ: неизвестная рубрика %s' % a['cat'])
    done = []
    for lang, sub in (('ru', 'news'), ('en', 'en/news')):
        out = os.path.join(repo, sub, slug + '.html')
        wr(out, render_page(repo, a, lang))
        done.append(out)
        done.append(put_into_feed(repo, a, lang, lead))
    print('Собрано:')
    for d in done:
        print('  ', d)
    print('Дальше: build_a.py, build_b.py, build_d.py, потом публикация')


if __name__ == '__main__':
    main()
