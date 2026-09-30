#!/usr/bin/env python3
"""Регистрация страницы-решения bitrix-accounting (интеграция Битрикс24 с учётной системой) во всех местах конвейера.
Идемпотентно: повторный запуск ничего не меняет. Запуск из корня сайта: python3 .seo/pages/reg_accounting.py"""
import io, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(ROOT)
MARK = 'bitrix-accounting'


def patch(path, pairs):
    s = io.open(path, encoding='utf-8').read()
    if MARK in s:
        print('%-32s уже есть' % path)
        return
    for old, new in pairs:
        assert s.count(old) == 1, (path, old[:60])
        assert old not in new or new.count(old) == 1
        s = s.replace(old, new, 1)
    io.open(path, 'w', encoding='utf-8').write(s)
    print('%-32s добавлено' % path)


# 1. Словарь PAGES
PAGE = """ 'accounting': {
  'slug': 'bitrix-accounting',
  'ru': ('Интеграция Битрикс24 с учётной системой в ОАЭ',
         'Связываем Битрикс24 с Zoho Books, QuickBooks, Odoo или 1С: счёт из сделки без перенабора, оплаты и долги клиентов в CRM, чистые реквизиты для e-invoicing в ОАЭ.',
         'Интеграция Битрикс24 с учётной системой', 'Интеграция CRM и учётной системы'),
  'en': ('Bitrix24 accounting integration in the UAE',
         'We connect Bitrix24 to Zoho Books, QuickBooks, Odoo or 1C: invoices from deals without retyping, payments and client balances in the CRM, clean data for UAE e-invoicing.',
         'Bitrix24 accounting integration', 'CRM and accounting integration'),
  'offer': False},
}

def build(key, lang):"""
patch('.seo/pages/build_solutions.py', [("}\n\ndef build(key, lang):", PAGE)])

# 2. Частые вопросы RU и EN
FAQ_RU = """'bitrix-accounting.html': [
 ('Можно ли выставлять счета прямо в Битрикс24, без учётной системы?',
  'Можно: в Битрикс24 есть счета и шаблоны с TRN и VAT. Но если бухгалтерия ведётся в Zoho Books, QuickBooks, Odoo или 1С, налоговый счёт лучше выставлять там, а в сделку возвращать номер, ссылку и статус оплаты. Так нумерация счетов одна, декларация VAT сходится с продажами, а с 2027 года электронный счёт уходит через провайдера прямо из учётной системы.'),
 ('Что передаётся между Битрикс24 и учётной системой?',
  'Из Битрикс24 в учёт уходят клиенты с реквизитами и сделки, из которых создаются счета. Из учёта в Битрикс24 приходят товары и цены, оплаты и статусы счетов, долги и кредитные лимиты клиентов, а если склад ведётся в учёте, то и остатки.'),
 ('Хватит ли готового приложения из Маркета Битрикс24?',
  'Для простых задач хватит. Например, приложение QuickBooks из Маркета синхронизирует клиентов и статусы счетов, но не переносит товары. Если нужен счёт прямо из сделки, валюты, частичные оплаты или проверка дублей по TRN, делаем интеграцию по API.'),
 ('Сколько стоит интеграция с учётной системой?',
  'Зависит от системы, объёма данных и того, что передаётся в обе стороны. Смету фиксируем в дирхамах после разбора, до начала работ. Настройка CRM Битрикс24 от 10 000 AED, а сопровождать обмен можно в пакете поддержки от 1 250 AED в месяц.'),
],
}

FAQ_EN = {"""
FAQ_EN_NEW = """'en/bitrix-accounting.html': [
 ('Can invoices be issued directly in Bitrix24 without an accounting system?',
  'Yes, Bitrix24 has invoices and templates with TRN and VAT. But if the books are kept in Zoho Books, QuickBooks, Odoo or 1C, the tax invoice is better issued there, with the number, a link and the payment status returned to the deal. That keeps one invoice numbering, the VAT return matches sales, and from 2027 the e-invoice goes through the provider straight from the accounting system.'),
 ('What is exchanged between Bitrix24 and the accounting system?',
  'Clients with their company details and the deals that become invoices go from Bitrix24 to accounting. Products and prices, payments and invoice statuses, client balances and credit limits, and stock if it is kept in accounting come back to Bitrix24.'),
 ('Is a ready-made app from the Bitrix24 Market enough?',
  'For simple needs, yes. For example, the QuickBooks app in the Market syncs clients and invoice statuses but not products. If you need an invoice straight from the deal, currencies, partial payments or duplicate checks by TRN, we build the integration on the API.'),
 ('How much does an accounting integration cost?',
  'It depends on the system, the data volume and what goes in each direction. The quote is fixed in dirhams after the review, before the work starts. Bitrix24 CRM setup starts from AED 10,000, and the sync can be maintained under a support package from AED 1,250 a month.'),
],
}
"""
s = io.open('.seo/faq_data.py', encoding='utf-8').read()
if MARK in s:
    print('%-32s уже есть' % '.seo/faq_data.py')
else:
    assert s.count("],\n}\n\nFAQ_EN = {") == 1
    s = s.replace("],\n}\n\nFAQ_EN = {", "],\n" + FAQ_RU, 1)
    assert s.rstrip().endswith('],\n}'), s[-80:]
    s = s.rstrip()[:-1] + FAQ_EN_NEW
    io.open('.seo/faq_data.py', 'w', encoding='utf-8').write(s)
    print('%-32s добавлено' % '.seo/faq_data.py')

# 3. llms.txt, русский список, sitemap
DIST_TAIL = "IntDoc compares supplier quotes\\n' % BASE)"
LLMS = ("IntDoc compares supplier quotes' % BASE)\n"
        "L.append('- [Bitrix24 accounting integration in the UAE](%s/en/bitrix-accounting): Zoho Books, QuickBooks Online, Odoo and 1C "
        "connected to Bitrix24 with one master system per data set: clients with TRN and deals go from the CRM to accounting, "
        "products, prices, payments, receivables and stock come back to the CRM; a UAE electronic tax invoice has 51 mandatory fields "
        "and companies with revenue of AED 50M+ must appoint an e-invoicing provider by 30 October 2026; Zoho is an accredited "
        "provider itself, QuickBooks, Odoo and 1C connect through a separate one\\n' % BASE)")
patch('.seo/build_d.py', [
    (DIST_TAIL, LLMS),
    ("('bitrix-distribution.html', '/bitrix-distribution'), ",
     "('bitrix-distribution.html', '/bitrix-distribution'), ('bitrix-accounting.html', '/bitrix-accounting'), "),
    ("('bitrix-distribution', '0.8'), ", "('bitrix-distribution', '0.8'), ('bitrix-accounting', '0.8'), "),
])

# 4. Карточка в блоке «Решения для ОАЭ» на /bitrix и /en/bitrix
patch('.seo/uae/link_solutions.py', [
    ("закупка через IntDoc', '/bitrix-distribution')]),\n 'en':",
     "закупка через IntDoc', '/bitrix-distribution'),\n   ('Учёт', 'Интеграция с учётом', 'Zoho Books, QuickBooks, Odoo и 1С: "
     "счёт из сделки, оплаты и долги клиентов в CRM', '/bitrix-accounting')]),\n 'en':"),
    ("sourcing with IntDoc', '/bitrix-distribution')]),\n}",
     "sourcing with IntDoc', '/bitrix-distribution'),\n   ('Accounting', 'Accounting integration', 'Zoho Books, QuickBooks, Odoo "
     "and 1C: invoices from deals, payments and client balances in the CRM', '/bitrix-accounting')]),\n}"),
])
