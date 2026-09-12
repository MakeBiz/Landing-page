# Часть D: robots.txt, llms.txt, sitemap.xml
import time
import sys, os, re, json, subprocess, datetime, html as H
sys.path.insert(0, os.path.dirname(__file__))
from seo_lib import *
ROOT = sys.argv[1]; TODAY = sys.argv[2]; os.chdir(ROOT)

ROBOTS = '''# Сайт открыт для поисковиков и AI-ассистентов целиком.
# Служебные страницы закрыты тегом robots noindex внутри самих страниц:
# запрет в этом файле мешает поисковику зайти на страницу и прочитать этот тег.
User-agent: *
Allow: /
Disallow: /api/

# Яндекс: рекламные метки не создают дубли страниц
User-agent: Yandex
Allow: /
Disallow: /api/
Clean-param: utm_source&utm_medium&utm_campaign&utm_content&utm_term&yclid&ymclid&gclid&gbraid&wbraid&fbclid&ttclid&msclkid&_openstat&from

# AI-поиск и ассистенты (ChatGPT, Perplexity, Claude, Gemini, Apple, Яндекс Нейро): доступ открыт
User-agent: OAI-SearchBot
User-agent: ChatGPT-User
User-agent: GPTBot
User-agent: PerplexityBot
User-agent: Perplexity-User
User-agent: ClaudeBot
User-agent: Claude-User
User-agent: Claude-SearchBot
User-agent: Google-Extended
User-agent: Applebot-Extended
User-agent: YandexAdditional
User-agent: YandexAdditionalBot
Allow: /
Disallow: /api/

Sitemap: https://makebiztechnologies.com/sitemap.xml
'''
wr('robots.txt', ROBOTS)

def cases(lang):
    out = subprocess.check_output(['node', '-e', "const vm=require('vm');const c={window:{}};vm.createContext(c);vm.runInContext(require('fs').readFileSync(process.argv[1],'utf8'),c);console.log(JSON.stringify(c.window.MB_CASES))",
                                   ('en/' if lang == 'en' else '') + 'keysy/cases-data.js']).decode()
    return json.loads(out)
plain = lambda x: re.sub(r'\s+', ' ', H.unescape(re.sub(r'<[^>]+>', '', x or ''))).strip()
def cut(t, n=230):
    return t if len(t) <= n else t[:n].rsplit(' ', 1)[0].rstrip(',;:') + '…'
def title_of(f): return H.unescape(re.search(r'<title>(.*?)</title>', rd(f), re.S).group(1)).strip()
def desc_of(f): return get_meta(rd(f), 'description') or ''
def h1_of(f): return plain(re.search(r'<h1[^>]*>(.*?)</h1>', rd(f), re.S).group(1))

news_en = sorted([f for f in os.listdir('en/news') if f.endswith('.html')])
news_ru = sorted([f for f in os.listdir('news') if f.endswith('.html')])

L = []
L.append('# MakeBiz Group\n')
L.append('> MakeBiz Group (legal entity MakeBiz Technologies FZE LLC) is an IT company in the UAE. We implement AI agents, Bitrix24 CRM, Vector AI speech analytics for sales calls, IntDoc document AI for procurement, BI analytics and IT infrastructure for businesses in Dubai, the UAE and Russian-speaking markets. The website is available in Russian (prices in AED) and English.\n')
L.append('Key facts:\n')
L.append('- Legal entity: MakeBiz Technologies FZE LLC, a free zone company of Ajman NuVentures Centre (UAE), registration number 2624215090888')
L.append('- Experience: 8 years in IT and AI, 150+ implementation projects, 24/7 support and maintenance')
L.append('- Contacts: Telegram @Anton_MakeBiz (https://t.me/Anton_MakeBiz), WhatsApp +971 50 262 0927, email info@makebiztechnologies.com')
L.append('- Meetings: online over Zoom or in person in Dubai; languages: Russian and English')
L.append('- All prices are in UAE dirhams (AED)\n')
L.append('## Services\n')
L.append('- [Bitrix24 implementation in Dubai and the UAE](%s/en/bitrix): CRM, sales pipelines, telephony, automation, BI and integrations. Standard CRM setup from AED 10,000; support packages of 5, 10 or 20 hours a month for AED 1,250, 2,300 or 4,200' % BASE)
L.append('- [AI agents for business](%s/en/ai-agents): a team of AI employees with roles, shared memory and CRM access that works in Telegram and runs sales, documents, calls and reports. Deployed on the client\'s server. From AED 6,000' % BASE)
L.append('- [AI agents cost calculator](%s/en/calculator-agents): 77 agents in 9 areas; implementation plans Start AED 6,000, Business AED 11,000, Holding AED 25,000 (one-off); maintenance 10%% of the implementation price per month' % BASE)
L.append('- [Vector: AI speech analytics for sales calls](%s/en/vector): analyses 100%% of calls and all 10 conversation stages, shows where clients are lost. Plans: Start AED 1,000 a month (5,000 minutes), Team AED 1,700 a month (10,000 minutes), Scale from AED 4,000 a month (from 30,000 minutes); prepayment discounts up to 20%%' % BASE)
L.append('- [IntDoc: AI supplier comparison from documents](%s/en/intdoc): extracts prices, lead times and availability from quotes, invoices, price lists and scans, compares suppliers in one table and justifies the choice' % BASE)
L.append('- [Servers and VPS](%s/en/vps): comparison of 7 hosting providers (Truehost Cloud, VPS.org, DataPacket, Hostman, UltaHost, IShosting, AEserver); MakeBiz deploys and maintains the chosen server\n' % BASE)
L.append('## Case studies\n')
for c in cases('en'):
    L.append('- [%s](%s/en/keysy/%s): %s' % (plain(c['title']), BASE, c['slug'], cut(plain(c['lead']))))
L.append('')
L.append('## Articles\n')
for f in news_en:
    p = 'en/news/' + f
    L.append('- [%s](%s/en/news/%s): %s' % (h1_of(p), BASE, f[:-5], desc_of(p)))
L.append('')
L.append('## Company\n')
L.append('- [Contacts](%s/en/contacts)' % BASE)
L.append('- [Partner programme](%s/en/partners): 20%% of the first client payment and 10%% for the following year for referrals' % BASE)
L.append('- [Privacy policy](%s/en/privacy)' % BASE)
L.append('- [Terms of use](%s/en/terms)\n' % BASE)
L.append('## Русская версия\n')
for f, u in [('index.html', '/'), ('bitrix.html', '/bitrix'), ('ai-agents.html', '/ai-agents'), ('calculator-agents.html', '/calculator-agents'), ('vector.html', '/vector'),
             ('intdoc.html', '/intdoc'), ('vps.html', '/vps'), ('keysy.html', '/keysy'), ('news.html', '/news'), ('partners.html', '/partners'), ('contacts.html', '/contacts')]:
    L.append('- [%s](%s%s): %s' % (title_of(f).split(' | ')[0], BASE, u, desc_of(f)))
for f in news_ru:
    p = 'news/' + f
    L.append('- [%s](%s/news/%s)' % (h1_of(p), BASE, f[:-5]))
wr('llms.txt', '\n'.join(L).rstrip() + '\n')

# ---------- sitemap ----------
def lastmod(paths):
    # было по git-истории: в папке STAGE репозитория нет, берём время файла
    best = 0
    for p in paths:
        if p and os.path.exists(p):
            best = max(best, os.path.getmtime(p))
    if not best:
        return TODAY
    return time.strftime('%Y-%m-%d', time.localtime(best))
pages = []   # (ru_url, en_url or None, priority, changefreq, files)
pairs = [('/', '/en', 'index.html', 'en/index.html', '1.0', 'weekly')]
for k, pr in [('bitrix', '0.9'), ('bitrix-support', '0.8'), ('ai-agents', '0.9'), ('vector', '0.9'), ('intdoc', '0.8'),
              ('vps', '0.6'), ('company', '0.7'), ('keysy', '0.7'), ('news', '0.7'),
              ('partners', '0.6'), ('contacts', '0.7'), ('privacy', '0.2'), ('terms', '0.2')]:
    pairs.append(('/' + k, '/en/' + k, k + '.html', 'en/' + k + '.html', pr, 'weekly' if k == 'news' else 'monthly'))
pairs.append(('/calculator-agents', '/en/calculator-agents', 'calculator-agents.html', 'en/calculator-agents.html', '0.8', 'monthly'))
for c in cases('ru'):
    s = c['slug']; pairs.append(('/keysy/' + s, '/en/keysy/' + s, 'keysy/%s.html' % s, 'en/keysy/%s.html' % s, '0.6', 'monthly'))
for f in news_ru:
    s = f[:-5]; en = 'en/news/' + f
    pairs.append(('/news/' + s, '/en/news/' + s if os.path.exists(en) else None, 'news/' + f, en if os.path.exists(en) else None, '0.6', 'monthly'))
X = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
n = 0
for ru, en, fr, fe, pr, cf in pairs:
    for loc, f in [(ru, fr), (en, fe)]:
        if not loc: continue
        assert os.path.exists(f), f
        X.append('  <url>')
        X.append('    <loc>%s%s</loc>' % (BASE, loc))
        if en:
            X.append('    <xhtml:link rel="alternate" hreflang="ru" href="%s%s"/>' % (BASE, ru))
            X.append('    <xhtml:link rel="alternate" hreflang="en" href="%s%s"/>' % (BASE, en))
            X.append('    <xhtml:link rel="alternate" hreflang="x-default" href="%s%s"/>' % (BASE, ru))
        X.append('    <lastmod>%s</lastmod>' % lastmod([f]))
        X.append('    <changefreq>%s</changefreq>' % cf)
        X.append('    <priority>%s</priority>' % (pr if loc == ru else str(round(float(pr) - 0.1, 1))))
        X.append('  </url>'); n += 1
X.append('</urlset>')
wr('sitemap.xml', '\n'.join(X) + '\n')
print('robots.txt, llms.txt (%d lines), sitemap.xml (%d urls)' % (len(L), n))
