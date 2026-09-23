#!/usr/bin/env python3
"""Блок «Решения для ОАЭ» на /bitrix и /en/bitrix: ссылки на страницы-решения. Идемпотентно (маркер <!--mb-solutions-->)"""
import os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(ROOT)
ANCHOR = '  <a id="process"></a>'
CARD = ('<a href="%s" style="display:block;text-decoration:none;background:linear-gradient(180deg,rgba(255,255,255,.06),rgba(255,255,255,.02));'
        'border:1px solid rgba(255,255,255,.1);border-radius:20px;padding:24px 22px;color:#EAF1FF">'
        '<span style="font:700 12px Oxygen;letter-spacing:.14em;text-transform:uppercase;color:#16C15A">%s</span>'
        '<h3 style="font:700 19px/1.3 Oxygen;color:#fff;margin:12px 0 8px">%s</h3>'
        '<p style="font:300 14.5px/1.55 Oxygen;color:#93A4B8;margin:0 0 14px">%s</p>'
        '<span style="font:700 14px Oxygen;color:#4FE07F">%s</span></a>')
T = {
 'ru': ('Решения для ОАЭ', 'Битрикс24 под задачи бизнеса в Дубае', 'Подробнее →', '', [
   ('Недвижимость', 'Агентство недвижимости в Дубае', 'Property Finder, Bayut и Dubizzle в CRM, разрешения Trakheesi, формы RERA и комиссии в AED', '/bitrix-real-estate'),
   ('Мессенджеры', 'WhatsApp в Битрикс24', 'Один номер на команду через официальный API, диалоги в карточке клиента, контроль времени ответа', '/bitrix-whatsapp'),
   ('Налоги', 'VAT, дирхамы и e-invoicing', 'VAT 5%, TRN и валюты в CRM, подготовка к электронным счетам с 2027 года', '/bitrix-vat-einvoicing'),
   ('Звонки', 'Телефония в ОАЭ', 'Через лицензированного оператора du или e&: звонки из CRM, записи разговоров, задачи на пропущенные', '/bitrix-telephony'),
   ('Выбор CRM', 'Битрикс24 или Zoho CRM', 'Честное сравнение: цена за компанию или за пользователя, свой сервер, учёт в Zoho Books', '/bitrix-vs-zoho'),
   ('Дистрибуция', 'Дистрибуция и опт', 'Склады и резервы, прайсы в AED и USD, дилеры с лимитами и PDC, закупка через IntDoc', '/bitrix-distribution')]),
 'en': ('Solutions for the UAE', 'Bitrix24 for the way business runs in Dubai', 'Learn more →', '/en', [
   ('Real estate', 'Real estate agency in Dubai', 'Property Finder, Bayut and Dubizzle in the CRM, Trakheesi permits, RERA forms and commissions in AED', '/bitrix-real-estate'),
   ('Messaging', 'WhatsApp in Bitrix24', 'One number for the team through the official API, chats in the client record, response-time control', '/bitrix-whatsapp'),
   ('Tax', 'VAT, dirhams and e-invoicing', '5% VAT, TRN and currencies in the CRM, ready for electronic invoices from 2027', '/bitrix-vat-einvoicing'),
   ('Calls', 'Telephony in the UAE', 'Through a licensed du or e& line: calls from the CRM, call recordings, tasks for missed calls', '/bitrix-telephony'),
   ('Choosing a CRM', 'Bitrix24 or Zoho CRM', 'An honest comparison: per-company or per-user pricing, own server, Zoho Books accounting', '/bitrix-vs-zoho'),
   ('Distribution', 'Distribution and wholesale', 'Warehouses and reservations, AED and USD price lists, dealers with credit limits and PDCs, sourcing with IntDoc', '/bitrix-distribution')]),
}
for path, lang in (('bitrix.html', 'ru'), ('en/bitrix.html', 'en')):
    h = open(path, encoding='utf-8').read()
    if '<!--mb-solutions-->' in h:
        a = h.index('  <!--mb-solutions-->'); b = h.index('<!--/mb-solutions-->') + len('<!--/mb-solutions-->\n\n')
        h = h[:a] + h[b:]
    eyebrow, h2, more, pre, cards = T[lang]
    block = ('  <!--mb-solutions--><section style="max-width:1180px;margin:0 auto;padding:clamp(40px,5vw,80px) clamp(18px,4vw,40px);border-top:1px solid transparent">\n'
             '    <div style="max-width:56ch;margin-bottom:32px"><span style="font:700 12px Oxygen;letter-spacing:.16em;text-transform:uppercase;color:#16C15A">%s</span>'
             '<h2 style="font:700 clamp(26px,3.6vw,42px)/1.1 Oxygen;letter-spacing:-.02em;color:#fff;margin:14px 0 0">%s</h2></div>\n'
             '    <div data-caps="" style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px">%s</div>\n'
             '  </section><!--/mb-solutions-->\n\n') % (eyebrow, h2, ''.join(CARD % (pre + u, e, t, d, more) for e, t, d, u in cards))
    assert h.count(ANCHOR) == 1, path
    h = h.replace(ANCHOR, block + ANCHOR, 1)
    open(path, 'w', encoding='utf-8').write(h)
    print(path, 'блок добавлен')
