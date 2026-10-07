#!/usr/bin/env python3
"""Регистрация страницы-решения bitrix-migration (переезд на Битрикс24 с amoCRM, HubSpot и таблиц) во всех местах конвейера.
Идемпотентно: повторный запуск ничего не меняет. Запуск из корня сайта: python3 .seo/pages/reg_migration.py"""
import io, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(ROOT)
MARK = 'bitrix-migration'


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
PAGE = """ 'migration': {
  'slug': 'bitrix-migration',
  'ru': ('Переезд на Битрикс24 с amoCRM, HubSpot и таблиц в ОАЭ',
         'Переносим клиентов, сделки и историю из amoCRM (Kommo), HubSpot, Excel и Google Таблиц в Битрикс24 без остановки продаж: тестовый перенос, переключение в выходные.',
         'Переезд на Битрикс24 с другой CRM', 'Миграция CRM'),
  'en': ('Bitrix24 migration from Kommo and HubSpot in the UAE',
         'We move clients, deals and history from Kommo (amoCRM), HubSpot, Excel and Google Sheets to Bitrix24 without stopping sales: a test run first, then a weekend switch.',
         'Bitrix24 migration from another CRM', 'CRM migration'),
  'offer': False},
}

def build(key, lang):"""
patch('.seo/pages/build_solutions.py', [("}\n\ndef build(key, lang):", PAGE)])

# 2. Частые вопросы RU и EN
FAQ_RU = """'bitrix-migration.html': [
 ('Остановятся ли продажи на время переезда на Битрикс24?',
  'Порядок переезда строится так, чтобы продажи не останавливались. Пока мы настраиваем Битрикс24 и переносим архив, команда работает в старой системе. Переключение проходит в выходные: догружаем изменения последних дней, переключаем WhatsApp, телефонию, почту и формы, и в первый рабочий день менеджеры открывают Битрикс24 с теми же клиентами и сделками. Старую систему не отключаем, пока вы не подтвердите, что всё на месте.'),
 ('Что переносится из amoCRM и HubSpot, а что нет?',
  'Переносим контакты, компании, сделки с воронками и стадиями, задачи, заметки, файлы и пользовательские поля, сохраняем ответственных и даты создания. Автоматизация не переносится: Salesbot и цифровую воронку amoCRM, workflows и sequences HubSpot собираем заново роботами и бизнес-процессами Битрикс24. Отчёты тоже настраиваем заново.'),
 ('Сохранится ли номер WhatsApp и переписка с клиентами?',
  'Номер, подключённый через официальный WhatsApp Business Platform, по документации Meta переводится к новому провайдеру без перерыва в переписке: сохраняются отображаемое имя, рейтинг качества и лимит сообщений, а шаблоны становятся доступны после копирования. История переписки вместе с номером не переезжает. То, что старая CRM отдаёт через выгрузку или API, переносим в карточки клиентов, остальное остаётся в архиве.'),
 ('Сколько стоит переезд на Битрикс24?',
  'Зависит от объёма базы, числа источников и того, сколько истории переносим. Смету фиксируем в дирхамах после разбора, до начала работ. Стандартная настройка CRM Битрикс24 от 10 000 AED, сопровождение после запуска по пакетам поддержки от 1 250 AED в месяц.'),
],
}

FAQ_EN = {"""
FAQ_EN_NEW = """'en/bitrix-migration.html': [
 ('Will sales stop while we move to Bitrix24?',
  'The move is planned so that they do not. While we set up Bitrix24 and move the archive, the team keeps working in the old system. The switch happens over a weekend: we bring across the changes from the last few days, switch WhatsApp, telephony, email and forms, and on the next working day managers open Bitrix24 with the same clients and deals. The old system is not switched off until you confirm that everything is in place.'),
 ('What moves from Kommo and HubSpot, and what does not?',
  'Contacts, companies, deals with pipelines and stages, tasks, notes, files and custom fields move, and responsible persons and creation dates are kept. Automation does not migrate: Salesbot and the Digital Pipeline in Kommo, workflows and sequences in HubSpot are rebuilt with Bitrix24 automation rules and workflows. Reports are set up again as well.'),
 ('Will we keep our WhatsApp number and chat history?',
  'According to Meta documentation, a number connected through the official WhatsApp Business Platform moves to a new provider with no break in messaging: it keeps its display name, quality rating and messaging limit, and templates become usable once they have been copied. Chat history does not move with the number. Whatever the old CRM gives through export or the API goes into client records; the rest stays in the archive.'),
 ('How much does a migration to Bitrix24 cost?',
  'It depends on the size of the database, the number of sources and how much history is moved. The quote is fixed in dirhams after the review, before the work starts. Standard Bitrix24 CRM setup starts from AED 10,000, and after launch the system is maintained under support packages from AED 1,250 a month.'),
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
ACC_TAIL = "through a separate one\\n' % BASE)"
LLMS = ("through a separate one' % BASE)\n"
        "L.append('- [Bitrix24 migration from Kommo and HubSpot in the UAE](%s/en/bitrix-migration): clients, deals and history move "
        "from Kommo (amoCRM), HubSpot, Excel and Google Sheets while the team keeps working in the old system, with the switch over a "
        "weekend; contacts, companies, deals with pipelines, notes, tasks and files are migrated, automation is rebuilt with Bitrix24 "
        "automation rules; Bitrix24 REST import methods do not trigger automation rules and keep creation dates; a WhatsApp Business "
        "Platform number keeps its display name and quality rating when moved to another provider, but chat history is not migrated; "
        "bitrix24.ae cloud accounts are hosted on AWS in Frankfurt, and the on-premise edition can run on a server in the UAE\\n' % BASE)")
patch('.seo/build_d.py', [
    (ACC_TAIL, LLMS),
    ("('bitrix-accounting.html', '/bitrix-accounting'), ",
     "('bitrix-accounting.html', '/bitrix-accounting'), ('bitrix-migration.html', '/bitrix-migration'), "),
    ("('bitrix-accounting', '0.8'), ", "('bitrix-accounting', '0.8'), ('bitrix-migration', '0.8'), "),
])

# 4. Карточка в блоке «Решения для ОАЭ» на /bitrix и /en/bitrix
patch('.seo/uae/link_solutions.py', [
    ("оплаты и долги клиентов в CRM', '/bitrix-accounting')]),\n 'en':",
     "оплаты и долги клиентов в CRM', '/bitrix-accounting'),\n   ('Переезд', 'Переезд с другой CRM', 'amoCRM, HubSpot и таблицы: "
     "клиенты, сделки и история переезжают без остановки продаж', '/bitrix-migration')]),\n 'en':"),
    ("payments and client balances in the CRM', '/bitrix-accounting')]),\n}",
     "payments and client balances in the CRM', '/bitrix-accounting'),\n   ('Migration', 'Moving from another CRM', 'Kommo, HubSpot "
     "and spreadsheets: clients, deals and history move without stopping sales', '/bitrix-migration')]),\n}"),
])
