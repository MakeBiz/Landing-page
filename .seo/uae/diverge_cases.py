#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Разводит карточки кейсов дубайского сайта с makebiz.life.

Данные кейсов совпадали с российским сайтом на 100%, а карточки (заголовок,
лид, «было», «стало», строка софта) показываются внизу /bitrix, /ai-agents,
/partners и на /keysy. Именно они давали основной остаток совпадений после
правки самих страниц. Факты те же, формулировки разные.

Длинные тексты внутри кейсов (problem, solution, result) пока не трогаем:
они видны только на самих страницах кейсов.

    python3 .seo/uae/diverge_cases.py .
"""
import io, os, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
os.chdir(ROOT)

RU = 'keysy/cases-data.js'
EN = 'en/keysy/cases-data.js'

PAIRS_RU = [
    ('Апартика: аренда недвижимости <b>по всей России в одной CRM</b>',
     'Апартика: тысяча объектов аренды <b>в одной CRM</b>'),
    ('Собрали аренду квартир, апартаментов, дач и домов в единую систему: больше тысячи объектов по всей стране, автопостинг объявлений на Avito, Циан и другие площадки, AI-агент квалифицирует заявки и помогает с бронированием, а речевая аналитика Vector следит за вежливостью и эмпатией в звонках.',
     'Аренда квартир, апартаментов, дач и домов ведётся в одной системе: больше тысячи объектов, объявления уходят на Avito, Циан и другие площадки сами, AI-агент разбирает заявки и помогает с бронью, а Vector слушает звонки и следит за вежливостью.'),
    ('объявления, площадки и заявки вели вручную и порознь', 'объявления и заявки жили в разных местах и вручную'),
    ('постинг, заявки, брони и аналитика в одной CRM', 'публикация, заявки, брони и цифры в одной системе'),
    ('CRM + автопостинг на площадки + AI-агент + <b>Vector</b> и BI по всем объектам.',
     'CRM, автопостинг объявлений, AI-агент, <b>Vector</b> и BI по всем объектам.'),

    ('Unilin: Битрикс24 для разъездных менеджеров <b>и аналитика по рынку</b>',
     'Unilin: коробочный Битрикс24 в полях <b>и аналитика по рынку</b>'),
    ('Третий год развиваем и поддерживаем Unilin: коробочный Битрикс24 на их сервере, глубоко доработанный под региональные продажи, работа разъездных менеджеров с мобильного, интеграции с 1С и ERP и BI-аналитика по рынку, торговым точкам, продуктам и компании.',
     'Третий год ведём Unilin: коробка Битрикс24 на их сервере, доработанная под региональные продажи, работа менеджеров в полях с телефона, связка с 1С и ERP и BI по рынку, торговым точкам, продуктам и компании.'),
    ('разъездные менеджеры и регионы вне единой системы', 'полевые менеджеры и регионы вне общей системы'),
    ('весь регион в CRM с телефона и аналитика по всем срезам', 'регион ведётся с телефона, аналитика по четырём срезам'),
    ('Коробочный Битрикс24, мобильные разъездные менеджеры, 1С и ERP, <b>BI по 4 срезам</b>.',
     'Коробка Битрикс24, работа в полях с телефона, 1С и ERP, <b>BI по 4 срезам</b>.'),

    ('СДЭК: корпоративный B2B на Битрикс24 <b>с агентами и аналитикой</b>',
     'СДЭК: B2B-направление на Битрикс24 <b>с агентами и дашбордами</b>'),
    ('Второй год развиваем корпоративное направление СДЭК в России и Казахстане: коробочный Битрикс24 под ключ, интеграции с внутренними системами, AI-агенты и BI-дашборды по корпоративным клиентам.',
     'Второй год ведём корпоративное направление СДЭК в России и Казахстане: коробка Битрикс24 под ключ, связка с внутренними системами, AI-агенты и BI-дашборды по корпоративным клиентам.'),
    ('корпоративные клиенты в разных системах и вручную', 'корпоративных клиентов вели в разных системах руками'),
    ('ведение, поддержка и аналитика в одном контуре', 'ведение, поддержка и цифры в одном контуре'),
    ('Коробочный Битрикс24, интеграции, <b>5 AI-агентов</b> и BI-дашборды.',
     'Коробка Битрикс24, интеграции, <b>пять AI-агентов</b> и BI-дашборды.'),

    ('HAVAL: речевая аналитика Vector <b>для сети автосалонов</b>',
     'HAVAL: Vector слушает <b>всю сеть автосалонов</b>'),
    ('Слушаем звонки автосалонов по всей России: Vector проверяет более 300 000 минут разговоров в месяц по 40+ критериям, при падении качества ниже 70% подключает старшего менеджера, а результат сводит в BI-дашборды.',
     'Звонки автосалонов по всей России разбирает Vector: больше 300 000 минут в месяц, 40+ критериев на разговор, падение ниже 70% поднимает старшего менеджера, итог складывается в BI-дашборды.'),
    ('сотни тысяч минут звонков никто не мог проверить', 'сотни тысяч минут разговоров проверить было нечем'),
    ('40+ критериев на каждом звонке и эскалация при риске', 'каждый звонок по 40+ критериям, слабый уходит наверх'),
    ('Vector + агенты + BI: <b>40+ критериев</b>, авто-эскалация ниже 70%, дашборды.',
     'Vector, агенты и BI: <b>40+ критериев</b>, автоэскалация ниже 70%, дашборды.'),

    ('Перформия: продажи, обучение, финансы и <b>сквозная аналитика</b>',
     'Перформия: путь от заявки до выпуска группы <b>в одной системе</b>'),
    ('Собрали весь цикл компании в одну систему: две линии продаж, выпуск учебных групп по всем программам, аккаунтинг и финансовый блок с рассрочками, задолженностями и ЭДО, плюс BI-дашборд со сквозной аналитикой по продажам, лидам, продуктам и поведению клиентов.',
     'Весь цикл компании собран в одну систему: две линии продаж, выпуск учебных групп по всем программам, аккаунтинг и финансы с рассрочками, задолженностями и ЭДО, а сверху BI-дашборд по продажам, лидам, продуктам и поведению клиентов.'),
    ('продажи, курсы и финансы жили порознь', 'продажи, курсы и деньги считали порознь'),
    ('весь цикл и сквозная аналитика в одном окне', 'цикл целиком и сквозная аналитика в одном окне'),
    ('Продажи, выпуск групп, финансы, ЭДО и <b>сквозная аналитика</b> в одном контуре.',
     'Продажи, выпуск групп, финансы, ЭДО и <b>сквозная аналитика</b> в одной системе.'),
]

PAIRS_EN = [
    ('Apartico: property rental <b>across Russia in one CRM</b>', 'Apartico: a thousand rental objects <b>in one CRM</b>'),
    ('We brought rental of apartments, serviced apartments, dachas and houses into one system: over a thousand objects across the country, auto posting of listings to Avito, Cian and other portals, an AI agent that qualifies enquiries and helps with booking, and Vector speech analytics that watches politeness and empathy on calls.',
     'Rental of apartments, serviced apartments, dachas and houses now runs in one system: over a thousand objects, listings posted to Avito, Cian and other portals on their own, an AI agent sorting enquiries and helping with bookings, and Vector listening in on calls for politeness.'),
    ('listings, portals and enquiries handled by hand and apart', 'listings and enquiries lived in different places, by hand'),
    ('posting, enquiries, bookings and analytics in one CRM', 'posting, enquiries, bookings and numbers in one system'),
    ('CRM + auto posting to portals + AI agent + <b>Vector</b> and BI across all objects.',
     'CRM, auto posting of listings, an AI agent, <b>Vector</b> and BI across all objects.'),

    ('Unilin: Bitrix24 for field managers <b>and market analytics</b>', 'Unilin: on-premise Bitrix24 in the field <b>and market analytics</b>'),
    ('For a third year we develop and support Unilin: an on-premise Bitrix24 on their server, deeply customized for regional sales, field managers working from mobile, integrations with 1C and ERP, and BI analytics on the market, retail points, products and the company.',
     'Third year on Unilin: an on-premise Bitrix24 on their own server, reworked for regional sales, managers working from a phone in the field, wired into 1C and ERP, with BI on the market, retail points, products and the company.'),
    ('field managers and regions outside a single system', 'field teams and regions outside any shared system'),
    ('the whole region in CRM from a phone, analytics on every cut', 'a region run from a phone, analytics across four cuts'),
    ('On-premise Bitrix24, mobile field managers, 1C and ERP, <b>BI across 4 cuts</b>.',
     'On-premise Bitrix24, field work from a phone, 1C and ERP, <b>BI across 4 cuts</b>.'),

    ('CDEK: corporate B2B on Bitrix24 <b>with agents and analytics</b>', 'CDEK: the B2B arm on Bitrix24 <b>with agents and dashboards</b>'),
    ('For a second year we develop CDEK corporate direction in Russia and Kazakhstan: an on-premise Bitrix24 built to fit, integrations with internal systems, AI agents and BI dashboards for corporate clients.',
     'Second year on the CDEK corporate arm in Russia and Kazakhstan: an on-premise Bitrix24 built to fit, wired into their internal systems, AI agents and BI dashboards for corporate clients.'),
    ('corporate clients spread across systems and handled by hand', 'corporate clients spread over systems and worked by hand'),
    ('management, support and analytics in one loop', 'management, support and numbers in one loop'),
    ('On-premise Bitrix24, integrations, <b>5 AI agents</b> and BI dashboards.',
     'On-premise Bitrix24, integrations, <b>five AI agents</b> and BI dashboards.'),

    ('HAVAL: Vector speech analytics <b>for a dealer network</b>', 'HAVAL: Vector listens to <b>the whole dealer network</b>'),
    ('We analyze dealership sales calls across Russia: Vector checks over 300,000 minutes of conversation a month against 40+ criteria, escalates to a senior manager when quality drops below 70%, and rolls everything up into BI dashboards.',
     'Dealership sales calls across Russia go through Vector: over 300,000 minutes a month, 40+ criteria per conversation, anything under 70% pulled up to a senior manager, and the whole picture in BI dashboards.'),
    ('hundreds of thousands of call minutes went unchecked', 'hundreds of thousands of call minutes with nothing to check them'),
    ('40+ criteria on every call and escalation on risk', 'every call against 40+ criteria, the weak ones pushed up'),
    ('Vector + agents + BI: <b>40+ criteria</b>, auto escalation below 70%, dashboards.',
     'Vector, agents and BI: <b>40+ criteria</b>, auto escalation under 70%, dashboards.'),

    ('Performia: sales, training, finance and <b>end to end analytics</b>',
     'Performia: from enquiry to graduating a group <b>in one system</b>'),
    ('We brought the company entire cycle into one system: two sales lines, running training groups across all programs, account management and a finance block with installments, receivables and payables, plus electronic document flow and a BI dashboard with end to end analytics on sales, leads, products and customer behavior.',
     'The whole company cycle now sits in one system: two sales lines, training groups run across every program, account management and a finance block with installments, receivables and payables, electronic document flow, and a BI dashboard over sales, leads, products and customer behaviour.'),
    ('sales, courses and finance lived apart', 'sales, courses and money were counted apart'),
    ('the whole cycle and end to end analytics in one window', 'the entire cycle and end to end analytics in one window'),
    ('Sales, group delivery, finance, documents and <b>end to end analytics</b> in one loop.',
     'Sales, group delivery, finance, documents and <b>end to end analytics</b> in one system.'),
]


def patch(path, pairs):
    h = io.open(path, encoding='utf-8').read()
    before = h
    done = skipped = 0
    for old, new in pairs:
        assert old not in new, 'новая строка не должна содержать старую: %s' % old[:50]
        if old not in h:
            skipped += 1
            continue
        h = h.replace(old, new)
        done += 1
    if h != before:
        io.open(path, 'w', encoding='utf-8').write(h)
    print('%s: заменено %d, уже было %d' % (path, done, skipped))


def main():
    patch(RU, PAIRS_RU)
    patch(EN, PAIRS_EN)
    # те же строки вшиты в собранные страницы кейсов и в хаб: build_c1 их печёт из снимка,
    # а снимок снять нечем (на Маке нет Playwright), поэтому правим те же строки на месте
    import glob
    for f in sorted(glob.glob('keysy/*.html')) + ['keysy.html']:
        patch(f, PAIRS_RU)
    for f in sorted(glob.glob('en/keysy/*.html')) + ['en/keysy.html']:
        patch(f, PAIRS_EN)


if __name__ == '__main__':
    main()
