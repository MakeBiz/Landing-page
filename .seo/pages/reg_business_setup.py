#!/usr/bin/env python3
"""Регистрация страницы-решения bitrix-business-setup (Битрикс24 для компаний по регистрации бизнеса и консалтинга в ОАЭ)
во всех местах конвейера. Идемпотентно: повторный запуск ничего не меняет.
Запуск из корня сайта: python3 .seo/pages/reg_business_setup.py"""
import io, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(ROOT)
MARK = 'bitrix-business-setup'
DASHES = ('—', '–')


def patch(path, pairs):
    s = io.open(path, encoding='utf-8').read()
    if MARK in s:
        print('%-32s уже есть' % path)
        return
    for old, new in pairs:
        assert s.count(old) == 1, (path, old[:60])
        assert old not in new or new.count(old) == 1
        assert not any(d in new for d in DASHES), (path, new[:60])
        s = s.replace(old, new, 1)
    io.open(path, 'w', encoding='utf-8').write(s)
    print('%-32s добавлено' % path)


def qa_block(key, items):
    return '%r: [\n' % key + ''.join(' (%r,\n  %r),\n' % (q, a) for q, a in items) + '],\n'


# 0. Тег счётчика в шаблоне головы. С 21 окт 2026 (коммит 654d7c1) он стоит прямо в HTML всех страниц решений,
#    а build_solutions.py о нём не знал и при пересборке снял бы его со всех страниц решений
PX_OLD = "'<!--mb-attr--><script src=\"/mb-attr.js\"></script><!--/mb-attr-->',"
PX_NEW = ("'<!--mb-attr--><script defer src=\"https://makebiz-makebiz-platform-3628.twc1.net/px/t.js\" data-site=\"makebiz-com\" "
          "data-endpoint=\"https://makebiz-makebiz-platform-3628.twc1.net/px\"></script>\\n<script src=\"/mb-attr.js\"></script><!--/mb-attr-->',")
s = io.open('.seo/pages/build_solutions.py', encoding='utf-8').read()
if 'twc1.net/px/t.js' in s:
    print('%-32s тег счётчика уже есть' % '.seo/pages/build_solutions.py')
else:
    assert s.count(PX_OLD) == 1
    io.open('.seo/pages/build_solutions.py', 'w', encoding='utf-8').write(s.replace(PX_OLD, PX_NEW, 1))
    print('%-32s тег счётчика добавлен в шаблон' % '.seo/pages/build_solutions.py')

# 0б. Статус официального партнёра (коммит d9fca66) был вписан прямо в llms.txt, а build_d.py пересобрал бы старый текст:
#     переносим те же две строки в сборщик, чтобы llms.txt после сборки совпал с опубликованным
s = io.open('.seo/build_d.py', encoding='utf-8').read()
if 'an official Bitrix24 partner in Dubai' in s:
    print('%-32s строки партнёра уже есть' % '.seo/build_d.py')
else:
    for old, new in [
        ('is an IT company in the UAE. We implement AI agents',
         'is an IT company in the UAE and an official Bitrix24 partner in Dubai. We implement AI agents'),
        ('- [Bitrix24 implementation in Dubai and the UAE](%s/en/bitrix): CRM, sales pipelines',
         '- [Bitrix24 implementation partner in Dubai and the UAE](%s/en/bitrix): official Bitrix24 partner and integrator; '
         'CRM, sales pipelines')]:
        assert s.count(old) == 1, old
        s = s.replace(old, new, 1)
    io.open('.seo/build_d.py', 'w', encoding='utf-8').write(s)
    print('%-32s строки партнёра перенесены в сборщик' % '.seo/build_d.py')

# 1. Словарь PAGES
RU = ('Битрикс24 для компаний по регистрации бизнеса в ОАЭ',
      'CRM для компаний по регистрации бизнеса в ОАЭ: долгий цикл продаж, документы клиентов, сроки лицензий и виз, '
      'бенефициары и проверка клиентов. Настройка от 10 000 AED.',
      'Битрикс24 для компаний по регистрации бизнеса и консалтинговых фирм', 'CRM для компаний по регистрации бизнеса')
EN = ('Bitrix24 for business setup firms in the UAE',
      'CRM for business setup and consulting firms in the UAE: long sales cycles, client documents, licence and visa '
      'deadlines, beneficial owners and KYC. Setup from AED 10,000.',
      'Bitrix24 for business setup and consulting firms', 'Business setup CRM')
for t in RU + EN:
    assert not any(d in t for d in DASHES)
assert len(RU[0]) + len(' | MakeBiz Group') <= 70 and len(EN[0]) + len(' | MakeBiz Group') <= 70, (len(RU[0]), len(EN[0]))
assert len(RU[1]) <= 170 and len(EN[1]) <= 170, (len(RU[1]), len(EN[1]))
PAGE = (" 'business-setup': {\n  'slug': 'bitrix-business-setup',\n  'ru': (%r,\n         %r,\n         %r, %r),\n"
        "  'en': (%r,\n         %r,\n         %r, %r),\n  'offer': True},\n}\n\ndef build(key, lang):") % (RU + EN)
patch('.seo/pages/build_solutions.py', [("}\n\ndef build(key, lang):", PAGE)])

# 2. Частые вопросы RU и EN
FAQ_RU = [
 ('Можно ли вести проверку клиентов (KYC) в Битрикс24?',
  'В Битрикс24 можно вести всю историю проверки, но клиентов по санкционным спискам он не проверяет, это делают отдельно. '
  'В карточке клиента хранятся анкета, копии документов, данные бенефициаров, уровень риска, кто и когда проверял и дата '
  'следующей проверки, а сделку нельзя передать в оформление, пока проверка не отмечена пройденной. Компании, которые выступают агентом '
  'при создании юрлиц или предоставляют юридический адрес, по статье 3 постановления Кабинета министров № 134 от 2025 года '
  'относятся к DNFBP и хранят документы проверки не меньше 5 лет после окончания отношений с клиентом (статья 25). Сообщения '
  'о подозрительных операциях в CRM не ведём.'),
 ('Как не пропустить продление лицензий и виз клиентов?',
  'Даты окончания лицензии, иммиграционной карты, виз, Emirates ID и аренды офиса заводим в смарт-процесс «Продления», связанный с компанией клиента и '
  'её людьми. Заранее, например за 60 и за 30 дней, робот ставит консультанту задачу на продление и отправляет '
  'клиенту напоминание в WhatsApp, если клиент согласился на такие сообщения. Для новой компании CRM считает и срок '
  'подачи заявки на регистрацию по корпоративному налогу: 3 месяца с даты создания по решению FTA № 3 от 2024 года, за опоздание штраф '
  '10 000 AED.'),
 ('Как собирать документы клиентов без переписки в WhatsApp и почте?',
  'Клиент загружает паспорт, фото и другие документы через CRM-форму с полями для файлов, и они сразу попадают в карточку. '
  'Нужные поля делаем обязательными на стадии, поэтому без документов сделку не передать в оформление. Поля с паспортными '
  'данными видят только выбранные сотрудники и отделы. Облачные порталы bitrix24.ae, по данным Bitrix24, размещены во '
  'Франкфурте, а если документы нужно хранить в ОАЭ, ставим коробочный Битрикс24 на ваш сервер в ОАЭ.'),
 ('Сколько стоит Битрикс24 для компании по регистрации бизнеса?',
  'Стандартная настройка CRM Битрикс24 от 10 000 AED, смету фиксируем в дирхамах после разбора, до начала работ. Лицензия '
  'Битрикс24 и платные сторонние сервисы, например отправка сообщений WhatsApp, оплачиваются отдельно, как и перенос данных из старых систем и сложные интеграции. После запуска сопровождаем '
  'по пакетам поддержки от 1 250 AED в месяц.'),
]
FAQ_EN = [
 ('Can client due diligence (KYC) be run in Bitrix24?',
  'Bitrix24 can hold the whole history of the check, but it does not screen clients against sanctions lists; that is done '
  'separately. The client record holds the questionnaire, document copies, beneficial owner data, the risk level, who checked '
  'the client and when, and the date of the next review, and the deal cannot be handed over for formation until the check is marked as '
  'passed. Firms that act as an agent in setting up legal persons or provide a registered office count as DNFBPs under '
  'Article 3 of Cabinet Resolution No. 134 of 2025 and keep due diligence records for at least 5 years after the '
  'relationship ends (Article 25). We do not keep suspicious transaction reports in the CRM.'),
 ('How do we avoid missing client licence and visa renewals?',
  'Expiry dates for the licence, establishment card, visas, Emirates IDs and office lease go into a Renewals smart process linked to the '
  'client company and its people. Ahead of time, for example 60 and 30 days before, an automation rule gives '
  'the consultant a renewal task and sends the client a WhatsApp reminder if they have agreed to such messages. For a new '
  'company the CRM also tracks the deadline to apply for corporate tax registration: 3 months from incorporation under FTA Decision '
  'No. 3 of 2024, with an AED 10,000 penalty for late registration.'),
 ('How can we collect client documents without WhatsApp and email threads?',
  'The client uploads their passport, photo and other documents through a CRM form with file fields, and the files land in '
  'the record straight away. The key fields are required by stage, so a deal cannot be handed over for formation without '
  'the documents. Fields with passport data are visible only to selected employees and departments. According to Bitrix24, '
  'bitrix24.ae cloud accounts are hosted in Frankfurt; if documents must stay in the UAE, we install on-premise Bitrix24 on '
  'your server in the UAE.'),
 ('How much does Bitrix24 cost for a business setup firm?',
  'Standard Bitrix24 CRM setup starts from AED 10,000, and the quote is fixed in dirhams after the review, before the work '
  'starts. The Bitrix24 licence and paid third-party services such as WhatsApp messaging are paid separately, as are data migration from old systems and complex integrations. After '
  'launch the system is maintained under support packages from AED 1,250 a month.'),
]
for q, a in FAQ_RU + FAQ_EN:
    assert not any(d in q + a for d in DASHES)
s = io.open('.seo/faq_data.py', encoding='utf-8').read()
if MARK in s:
    print('%-32s уже есть' % '.seo/faq_data.py')
else:
    assert s.count("],\n}\n\nFAQ_EN = {") == 1
    s = s.replace("],\n}\n\nFAQ_EN = {", "],\n" + qa_block('bitrix-business-setup.html', FAQ_RU) + "}\n\nFAQ_EN = {", 1)
    assert s.rstrip().endswith('],\n}'), s[-80:]
    s = s.rstrip()[:-1] + qa_block('en/bitrix-business-setup.html', FAQ_EN) + '}\n'
    io.open('.seo/faq_data.py', 'w', encoding='utf-8').write(s)
    print('%-32s добавлено' % '.seo/faq_data.py')

# 3. llms.txt, русский список, sitemap
CLIN_TAIL = "in the client record\\n' % BASE)"
LINE = ("- [Bitrix24 for business setup firms in the UAE](%s/en/bitrix-business-setup): a sales pipeline for the "
        "long choice between the mainland and free zones with a time limit on every stage, proposals and contracts from DOCX "
        "templates, client documents uploaded through CRM forms into the record with fields required by stage, a formation "
        "smart process, renewal reminders for licences, establishment cards, visas and Emirates IDs, and recurring deals for "
        "bookkeeping and PRO services; due diligence history and beneficial owner data are kept in the client record, as "
        "corporate service providers count as DNFBPs under Cabinet Resolution No. 134 of 2025 (Article 3, records kept for "
        "at least 5 years under Article 25), beneficial owner changes are reported to the registrar within 15 days under "
        "Cabinet Resolution No. 109 of 2023 and a new company applies for corporate tax registration within 3 months of incorporation "
        "under FTA Decision No. 3 of 2024")
assert "'" not in LINE and '%' not in LINE.replace('%s', '') and not any(d in LINE for d in DASHES)
LLMS = "in the client record' % BASE)\nL.append('" + LINE + "\\n' % BASE)"
patch('.seo/build_d.py', [
    (CLIN_TAIL, LLMS),
    ("('bitrix-clinics.html', '/bitrix-clinics'), ",
     "('bitrix-clinics.html', '/bitrix-clinics'), ('bitrix-business-setup.html', '/bitrix-business-setup'), "),
    ("('bitrix-clinics', '0.8'), ", "('bitrix-clinics', '0.8'), ('bitrix-business-setup', '0.8'), "),
])

# 4. Карточка в блоке «Решения для ОАЭ» на /bitrix и /en/bitrix (десятая: последняя строка из одной карточки)
patch('.seo/uae/link_solutions.py', [
    ("медданные по закону ОАЭ', '/bitrix-clinics')]),\n 'en':",
     "медданные по закону ОАЭ', '/bitrix-clinics'),\n   ('Корпоративные услуги', 'Регистрация бизнеса и консалтинг', "
     "'Долгий цикл продаж, документы клиентов, сроки лицензий и виз, бенефициары и проверка клиентов', "
     "'/bitrix-business-setup')]),\n 'en':"),
    ("health data under UAE law', '/bitrix-clinics')]),\n}",
     "health data under UAE law', '/bitrix-clinics'),\n   ('Corporate services', 'Business setup and consulting', "
     "'Long sales cycles, client documents, licence and visa deadlines, beneficial owners and KYC', "
     "'/bitrix-business-setup')]),\n}"),
])
