# SSR-блоки: текст отрендеренной страницы в исходном HTML (для Яндекса и AI-ботов без JS)
import re, html as H

NAV = {
 'ru': [('/', 'Главная'), ('/bitrix', 'Внедрение Битрикс24'), ('/ai-agents', 'AI-агенты'), ('/calculator-agents', 'Калькулятор AI-агентов'),
        ('/vector', 'Vector: речевая аналитика'), ('/intdoc', 'IntDoc: документы и закупки'), ('/vps', 'Серверы'), ('/keysy', 'Кейсы'),
        ('/news', 'Новости'), ('/partners', 'Партнёрам'), ('/contacts', 'Контакты'), ('/en', 'English')],
 'en': [('/en', 'Home'), ('/en/bitrix', 'Bitrix24 implementation'), ('/en/ai-agents', 'AI agents'), ('/en/calculator-agents', 'AI agents cost calculator'), ('/en/vector', 'Vector: speech analytics'),
        ('/en/intdoc', 'IntDoc: documents and procurement'), ('/en/vps', 'Servers'), ('/en/keysy', 'Case studies'), ('/en/news', 'News'),
        ('/en/partners', 'Partners'), ('/en/contacts', 'Contacts'), ('/', 'Русская версия')],
}
FOOT = {
 'ru': 'MakeBiz Group, IT-компания в ОАЭ: внедряем AI, CRM Битрикс24 и BI-аналитику. MakeBiz Technologies FZE LLC, компания свободной экономической зоны Ajman NuVentures Centre, регистрационный номер 2624215090888. Связь: <a href="https://t.me/Anton_MakeBiz">Telegram @Anton_MakeBiz</a>, <a href="https://wa.me/971502620927">WhatsApp +971 50 262 0927</a>, <a href="mailto:info@makebiztechnologies.com">info@makebiztechnologies.com</a>.',
 'en': 'MakeBiz Group, an IT company in the UAE: we implement AI, Bitrix24 CRM and BI analytics. MakeBiz Technologies FZE LLC, a free zone company of Ajman NuVentures Centre, registration number 2624215090888. Contact: <a href="https://t.me/Anton_MakeBiz">Telegram @Anton_MakeBiz</a>, <a href="https://wa.me/971502620927">WhatsApp +971 50 262 0927</a>, <a href="mailto:info@makebiztechnologies.com">info@makebiztechnologies.com</a>.',
}
UI = re.compile(r'^(Подробнее|Обсудить проект|Записаться на демонстрацию|Рассчитать.*|Выбрать.*|Оставить заявку|Написать в Telegram|Отправить|Learn more|Discuss (a|the) project|Book a demo|Calculate.*|Choose.*|Leave a request|Write (to us )?(on|in) Telegram|Send|Все кейсы|All cases|Наши продукты|Our products)\s*[→›»]*$', re.I)
FOOT_START = re.compile(r'^(IT-компания в ОАЭ\. Внедряем|UAE IT company\.|An IT company in the UAE\.|IT company in the UAE\.)')

def esc(t): return H.escape(t, quote=False)

def is_caps(t):
    letters = re.sub(r'[^A-Za-zА-Яа-яЁё]', '', t)
    return len(letters) >= 3 and letters == letters.upper() and len(t) < 60

def build(blocks, lang, fixes=None):
    out, labels, ul = [], [], []
    seen = set()
    def flush_labels():
        nonlocal labels
        if len(labels) >= 2 and sum(len(x) for x in labels) < 220: out.append('<p>' + esc(' · '.join(labels)) + '</p>')
        labels = []
    def flush_ul():
        nonlocal ul
        if ul: out.append('<ul>' + ''.join('<li>' + esc(x) + '</li>' for x in ul) + '</ul>')
        ul = []
    for b in blocks:
        t = b['t'].strip()
        if fixes:
            for a, c in fixes: t = re.sub(a, c, t)
        if b['tag'] == 'A':
            if b.get('inHeader') or b.get('inFooter'): continue
            href = b.get('href') or ''
            txt = re.sub(r'\s*[→›»]+\s*$', '', t)
            if href.startswith('/') and txt and not UI.match(t) and ('A' + txt) not in seen:
                seen.add('A' + txt); flush_labels(); flush_ul(); out.append('<p><a href="%s">%s</a></p>' % (H.escape(href), esc(txt)))
            elif href.startswith('/') and txt and ('A' + txt) not in seen and txt in ('Все кейсы', 'All cases'):
                seen.add('A' + txt); out.append('<p><a href="%s">%s</a></p>' % (H.escape(href), esc(txt)))
            continue
        if b['tag'] in ('H4',) and t in ('Продукты', 'Разделы', 'Правовое', 'Products', 'Sections', 'Legal'): break
        if b['tag'] in ('T', 'P') and FOOT_START.match(t): break
        if not t or t in seen: continue
        seen.add(t)
        if b['tag'] in ('H1', 'H2', 'H3', 'H4'):
            flush_labels(); flush_ul()
            lvl = {'H1': 'h1', 'H2': 'h2', 'H3': 'h3', 'H4': 'h3'}[b['tag']]
            out.append('<%s>%s</%s>' % (lvl, esc(t), lvl)); continue
        if b['tag'] == 'LI':
            flush_labels(); ul.append(t); continue
        # P / T
        if '→' in t or UI.match(t) or is_caps(t): continue
        words = len(t.split())
        if words <= 4 and not re.search(r'[.!?]$', t):
            flush_ul(); labels.append(t); continue
        flush_labels(); flush_ul()
        out.append('<p>' + esc(t) + '</p>')
    flush_labels(); flush_ul()
    nav = '<nav>' + ' '.join('<a href="%s">%s</a>' % (u, esc(n)) for u, n in NAV[lang]) + '</nav>'
    return '\n'.join(out) + '\n' + nav + '\n<p>' + FOOT[lang] + '</p>'

def words(htmlfrag): return len(re.findall(r'\w+', re.sub(r'<[^>]+>', ' ', htmlfrag)))
