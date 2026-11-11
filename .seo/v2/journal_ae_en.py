# -*- coding: utf-8 -*-
# Журнал гайдов makebiztechnologies.com, EN (/en/journal, /en/journal/<slug>). Подключается из build_en_ae.py через exec() после landings_ae_en.py.
# Статьи и общие функции: journal_src.py, тексты в .seo/v2/journal/<slug>.json. Шапка, подвал, форма и счётчики идут из page()
from journal_src import JOURNAL, date_en, read_min, words, rubrics, jpath, plain

J_STYLE = ('<style>.jart{max-width:860px;margin:0 auto}.jart h3{font-size:19px;margin:22px 0 8px}.jart ul,.jart ol{margin:0 0 16px 22px;padding:0;color:var(--ink2);font-size:17px;line-height:1.6}'
           '.jart li{margin:6px 0}.jart .ptw{margin:18px 0 8px}.jart a{text-decoration:underline;text-underline-offset:3px}.jart p.note{font-size:14px}'
           '.jmeta{margin-top:10px;font-size:14px;color:var(--mut)}.jhub .card small{display:block;margin-top:10px;font-size:13px;color:var(--mut)}.jrub{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px}</style>')

def j_html(s, Uf):
    s = s.replace('<table>', '<div class="ptw gl"><table class="ptab">').replace('</table>', '</table></div>')
    s = re.sub(r'href="(/[^"#]*)(#[^"]*)?"', lambda m: 'href="' + Uf(m.group(1)) + (m.group(2) or '') + '"', s)
    s = re.sub(r'<a href="(https?://(?!makebiztechnologies\.com)[^"]+)"', r'<a href="\1" rel="noopener" target="_blank"', s)
    return s

def j_art(x, first):
    pad = ' style="padding-top:0"' if first else ''
    return f'<section class="sec"{pad}><div class="wrap"><article class="kart gl jart">{x}</article></div></section>'

def j_mid(t, x, btn):
    return ('<section class="sec dark"><div class="wrap"><div class="cross"><div><h3>' + esc(t) + '</h3><p>' + esc(x)
            + '</p></div><a class="btn" href="#form">' + esc(btn) + '</a></div></div></section>')

def j_related(items, lab_j, lab_n, more_t, more_href, title, Uf):
    li = ''
    for u, t in items:
        lab = lab_j if u.startswith('/journal/') else lab_n
        li += f'<a class="rel-a gl" href="{Uf(u)}"><small>{lab}</small><b>{esc(t)}</b><span>Read →</span></a>'
    return f'<section class="sec rel-sec"><div class="wrap"><h2>{title}</h2><div class="rel">{li}</div><p class="more"><a href="{Uf(more_href)}">{more_t}</a></p></div></section>'

def j_article_ld(a, L, canon, lang, rub):
    return {"@type": "Article", "@id": canon + "#article", "headline": plain(L.get('h1') or L['title']), "description": L['desc'],
            "datePublished": a['date'], "dateModified": a.get('modified', a['date']), "inLanguage": lang, "articleSection": rub,
            "wordCount": words(a, lang), "mainEntityOfPage": canon, "url": canon, "image": SITE + "/img/og.jpg",
            "author": {"@type": "Organization", "@id": SITE + "/#organization", "name": "MakeBiz Technologies", "url": SITE + "/"},
            "publisher": {"@type": "Organization", "@id": SITE + "/#organization", "name": "MakeBiz Technologies", "logo": {"@type": "ImageObject", "url": SITE + "/favicon.png"}}}

for a in JOURNAL:
    L = a['en']; p = jpath(a['slug']); rub = a['rubric_en']
    parts = j_html(L['body'], U).split('<!--cta-->')
    b = (f'<section class="hero hero-small"><div class="wrap"><span class="eyebrow">Journal · {esc(rub)}</span><h1>{esc(L.get("h1") or L["title"])}</h1>'
         f'<p class="lead">{L["lead"]}</p><p class="answer">{j_html(L["answer"], U)}</p>'
         f'<p class="jmeta">MakeBiz Technologies · {date_en(a["date"])} · {read_min(a, "en")} min read</p></div></section>')
    b += J_STYLE + j_art(parts[0], True)
    if len(parts) > 1:
        b += j_mid(*L['mid']) + j_art(parts[1], False)
    b += faq([(q, j_html(x, U)) for q, x in L['faq']])
    b += j_related(L['related'], 'Journal', 'News', 'All journal articles →', '/journal', 'Read also', U)
    b += form_block('journal-' + a['slug'], L['cta'][0], L['cta'][1])
    page(p, 'journal-' + a['slug'], L['title'], L['desc'], 'journal', b,
         [j_article_ld(a, L, SITE + en_path(p), 'en', rub)],
         [('/', 'Home'), ('/journal', 'Journal'), (p, L.get('crumb') or L['title'])], L['faq'])

if JOURNAL:
    rb = rubrics('en')
    hb = (f'<section class="hero hero-small"><div class="wrap"><span class="eyebrow">MakeBiz Journal</span><h1>Journal: guides to <span>Bitrix24 and CRM in the UAE</span></h1>'
          f'<p class="lead">Short answers to the questions companies ask before a CRM project in Dubai and across the Emirates: choosing a partner, plans, WhatsApp, processes and data</p>'
          f'<p class="answer">The MakeBiz Technologies journal has {len(JOURNAL)} guide{"" if len(JOURNAL) == 1 else "s"} for UAE companies: each opens with a short answer, then a table, a worked example and prices in AED with the date they were checked. New articles come out twice a week, market updates are in the <a href="{U("/news")}">news</a>.</p>'
          f'<div class="jrub">' + ''.join(f'<a class="ktag" href="#r{i}">{esc(r)}</a>' for i, r in enumerate(rb)) + '</div></div></section>')
    for i, r in enumerate(rb):
        cs = ''.join(f'<a class="card" href="{U(jpath(x["slug"]))}"><h3>{esc(x["en"].get("h1") or x["en"]["title"])}</h3><p>{esc(x["en"]["desc"])}</p><small>{date_en(x["date"])} · {read_min(x, "en")} min</small></a>'
                     for x in JOURNAL if x['rubric_en'] == r)
        hb += section(esc(r), '', f'<div class="grid g3 jhub">{cs}</div>', id_=f'r{i}', tone='tint' if i % 2 else '')
    hb += J_STYLE + form_block('journal', 'Let us discuss your task', 'Tell us what you need set up or priced. We reply within a business day')
    page('/journal', 'journal', 'MakeBiz Journal: Bitrix24 and CRM guides for the UAE',
         'MakeBiz Technologies guides for UAE companies: choosing a Bitrix24 partner, plans, WhatsApp in CRM. An answer, a table and AED prices in every article.',
         'journal', hb,
         [{"@type": "CollectionPage", "@id": SITE + "/en/journal#collection", "url": SITE + "/en/journal", "name": "MakeBiz Journal", "inLanguage": "en",
           "mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": SITE + en_path(jpath(x['slug'])), "name": x['en']['title']} for i, x in enumerate(JOURNAL)]}}],
         [('/', 'Home'), ('/journal', 'Journal')])
