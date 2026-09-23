#!/usr/bin/env python3
"""Регистрация страницы-решения bitrix-distribution (дистрибуция и опт в ОАЭ) во всех местах конвейера.
Идемпотентно: повторный запуск ничего не меняет. Запуск из корня сайта: python3 .seo/pages/reg_distribution.py"""
import io, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(ROOT)
MARK = 'bitrix-distribution'


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
PAGE = """ 'distribution': {
  'slug': 'bitrix-distribution',
  'ru': ('Битрикс24 для дистрибуции и оптовой торговли в ОАЭ',
         'CRM для дистрибьютора в ОАЭ: склады и резервы в сделке, цены для дилеров и опта, прайсы в AED и USD, кредитные лимиты и PDC, VAT и экспорт. Настройка от 10 000 AED.',
         'Битрикс24 для дистрибуции и оптовой торговли', 'CRM для дистрибуции и опта'),
  'en': ('Bitrix24 for distribution and wholesale in the UAE',
         'CRM for UAE distributors: stock and reservations, dealer and wholesale prices, AED and USD price lists, credit limits and PDCs, VAT and exports. Setup from AED 10,000.',
         'Bitrix24 for distribution and wholesale', 'Distribution CRM'),
  'offer': True},
}

def build(key, lang):"""
patch('.seo/pages/build_solutions.py', [("}\n\ndef build(key, lang):", PAGE)])

# 2. Частые вопросы RU и EN
FAQ_RU = """'bitrix-distribution.html': [
 ('Можно ли вести в Битрикс24 склад и остатки?',
  'Да. В Битрикс24 есть складской учёт: несколько складов, приход, перемещение и списание, резерв товара в сделке и списание со склада при закрытии сделки. Если склад уже ведётся в учётной системе, остатки передаём в Битрикс24 интеграцией.'),
 ('Как вести цены в дирхамах и долларах?',
  'Цена товара хранится в своей валюте и пересчитывается в валюту сделки по курсу из настроек CRM. Дирхам привязан к доллару по курсу 3,6725, поэтому этот курс задаётся один раз. В налоговом счёте в долларах итог и VAT указываются и в дирхамах, по курсу ЦБ ОАЭ на дату поставки.'),
 ('Можно ли дать дилерам свои цены и кредитные лимиты?',
  'Да. У каждого уровня клиентов свой тип цены в каталоге, и в сделку подставляется цена уровня клиента. Кредитный лимит и отсрочка хранятся в карточке дилера, заказ сверх лимита уходит на согласование руководителю.'),
 ('Сколько стоит CRM для дистрибьютора?',
  'Стандартная настройка Битрикс24 от 10 000 AED. Точная смета зависит от числа складов, типов цен и интеграций, фиксируем её в дирхамах до начала работ.'),
],
}

FAQ_EN = {"""
FAQ_EN_NEW = """'en/bitrix-distribution.html': [
 ('Can Bitrix24 handle warehouses and stock?',
  'Yes. Bitrix24 has inventory management: several warehouses, receipts, transfers and write-offs, product reservation in a deal and a stock write-off when the deal closes. If stock is already kept in an accounting system, we bring stock levels into Bitrix24 through an integration.'),
 ('How do prices in dirhams and dollars work?',
  'Each product price is stored in its own currency and converted into the deal currency at the rate set in the CRM. The dirham is pegged to the dollar at 3.6725, so that rate is set once. On a tax invoice in dollars the total and the VAT are also shown in dirhams at the UAE Central Bank rate on the date of supply.'),
 ('Can dealers have their own prices and credit limits?',
  "Yes. Each customer tier has its own price type in the catalog, and the deal picks up the price for the client's tier. The credit limit and payment terms sit in the dealer record, and an order over the limit goes to management for approval."),
 ('How much does a CRM for a distributor cost?',
  'Standard Bitrix24 setup starts from AED 10,000. The exact quote depends on the number of warehouses, price types and integrations and is fixed in dirhams before the work starts.'),
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
ZOHO_TAIL = "written by a Bitrix24 integrator\\n' % BASE)"
LLMS = ("written by a Bitrix24 integrator' % BASE)\n"
        "L.append('- [Bitrix24 for distribution and wholesale in the UAE](%s/en/bitrix-distribution): warehouses and stock "
        "reservation in deals, price types for retail, wholesale and dealer tiers, AED and USD price lists (the dirham is pegged "
        "at 3.6725 per US dollar), dealer credit limits and a post-dated cheque register, tax invoices in USD with VAT shown in AED, "
        "zero-rated exports outside the GCC, free zone stock; IntDoc compares supplier quotes\\n' % BASE)")
patch('.seo/build_d.py', [
    (ZOHO_TAIL, LLMS),
    ("('bitrix-vs-zoho.html', '/bitrix-vs-zoho'), ",
     "('bitrix-vs-zoho.html', '/bitrix-vs-zoho'), ('bitrix-distribution.html', '/bitrix-distribution'), "),
    ("('bitrix-vs-zoho', '0.7'), ", "('bitrix-vs-zoho', '0.7'), ('bitrix-distribution', '0.8'), "),
])

# 4. Карточка в блоке «Решения для ОАЭ» на /bitrix и /en/bitrix
patch('.seo/uae/link_solutions.py', [
    ("'/bitrix-vs-zoho')]),\n 'en':",
     "'/bitrix-vs-zoho'),\n   ('Дистрибуция', 'Дистрибуция и опт', 'Склады и резервы, прайсы в AED и USD, дилеры с лимитами и PDC, "
     "закупка через IntDoc', '/bitrix-distribution')]),\n 'en':"),
    ("Zoho Books accounting', '/bitrix-vs-zoho')]),\n}",
     "Zoho Books accounting', '/bitrix-vs-zoho'),\n   ('Distribution', 'Distribution and wholesale', 'Warehouses and "
     "reservations, AED and USD price lists, dealers with credit limits and PDCs, sourcing with IntDoc', '/bitrix-distribution')]),\n}"),
])
