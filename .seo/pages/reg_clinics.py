#!/usr/bin/env python3
"""Регистрация страницы-решения bitrix-clinics (Битрикс24 для клиник и салонов красоты в Дубае) во всех местах конвейера.
Идемпотентно: повторный запуск ничего не меняет. Запуск из корня сайта: python3 .seo/pages/reg_clinics.py"""
import io, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(ROOT)
MARK = 'bitrix-clinics'
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


# 1. Словарь PAGES
RU = ('Битрикс24 для клиник и салонов красоты в Дубае',
      'CRM для клиники и салона в Дубае: онлайн-запись к врачам и мастерам, напоминания в WhatsApp, '
      'согласия клиентов, медданные по закону ОАЭ. Настройка от 10 000 AED.',
      'Битрикс24 для клиник и салонов красоты', 'CRM для клиник и салонов')
EN = ('Bitrix24 for clinics and beauty salons in Dubai',
      'CRM for clinics and salons in Dubai: online booking with doctors and stylists, WhatsApp reminders, '
      'client consents, health data under UAE law. Setup from AED 10,000.',
      'Bitrix24 for clinics and beauty salons', 'Clinic and salon CRM')
for t in RU + EN:
    assert not any(d in t for d in DASHES)
assert len(RU[0]) + len(' | MakeBiz Group') <= 70 and len(EN[0]) + len(' | MakeBiz Group') <= 70
assert len(RU[1]) <= 170 and len(EN[1]) <= 170, (len(RU[1]), len(EN[1]))
PAGE = (" 'clinics': {\n  'slug': 'bitrix-clinics',\n  'ru': (%r,\n         %r,\n         %r, %r),\n"
        "  'en': (%r,\n         %r,\n         %r, %r),\n  'offer': True},\n}\n\ndef build(key, lang):") % (RU + EN)
patch('.seo/pages/build_solutions.py', [("}\n\ndef build(key, lang):", PAGE)])

# 2. Частые вопросы RU и EN
FAQ_RU = [
 ('Можно ли хранить данные пациентов в облачном Битрикс24?',
  'Медицинские данные в карточках облачного Битрикс24 не ведём. По статье 13 Федерального закона № 2 от 2019 года медицинскую информацию и данные, '
  'связанные с медицинскими услугами в ОАЭ, нельзя хранить и обрабатывать за пределами страны, кроме случаев, которые орган '
  'здравоохранения определяет по согласованию с министерством, а облачные порталы bitrix24.ae, по данным Bitrix24, размещены '
  'во Франкфурте. Поэтому диагнозы, анализы и фото остаются в медицинской системе клиники. Закон не делит данные на '
  'административные и медицинские, так что можно ли вести в облаке хотя бы запись и оплаты, решает юрист клиники. Если нельзя '
  'или медицинская часть нужна в CRM, ставим коробочный Битрикс24 на сервер в ОАЭ.'),
 ('Как Битрикс24 помогает справиться с неявками?',
  'Онлайн-запись Битрикс24 отправляет клиенту в WhatsApp сообщение о записи, просьбу подтвердить визит по ссылке (по умолчанию '
  'за день), напоминание в день визита и сообщение, если клиент опаздывает. Неподтверждённые записи подсвечиваются, у '
  'администратора появляется дело, и освободившееся время можно отдать клиенту из листа ожидания. Для услуг с повторным '
  'циклом роботы напоминают о следующем визите тем, кто согласился на такие сообщения.'),
 ('Можно ли делать рассылки пациентам в WhatsApp?',
  'Можно тем, кто дал номер и согласился получать сообщения, а просьбу больше не писать нужно выполнять: так требуют правила '
  'WhatsApp. Клиники с лицензией DHA должны писать тексты по стандартам DHA для медицинской рекламы в соцсетях, где WhatsApp '
  'тоже считается соцсетью: без слов «лучший», «100%», «без побочных эффектов» и «мгновенный результат», а публикации с '
  'упоминанием клиники согласует медицинский директор. Рекламные SMS и рекламные сообщения в приложениях соцсетей '
  'постановление Кабмина № 56 от 2024 года (статья 1) относит к телемаркетингу наравне со звонками.'),
 ('Сколько стоит Битрикс24 для клиники или салона?',
  'Стандартная настройка CRM Битрикс24 от 10 000 AED, смету фиксируем в дирхамах после разбора, до начала работ. Онлайн-запись '
  'в облачном Битрикс24 входит в тариф Professional и выше, лицензия Битрикс24 и сообщения WhatsApp оплачиваются отдельно. '
  'Связку с медицинской системой оцениваем после разбора, а после запуска сопровождаем по пакетам поддержки от 1 250 AED '
  'в месяц.'),
]
FAQ_EN = [
 ('Can patient data be stored in the Bitrix24 cloud?',
  'We do not keep health data in cloud Bitrix24 records. Under Article 13 of UAE Federal Law No. 2 of 2019, health information and data '
  'related to health services provided in the UAE may not be stored or processed outside the country except in cases set by '
  'the health authority in coordination with the ministry, and according to Bitrix24, bitrix24.ae cloud accounts are hosted in '
  'Frankfurt. So diagnoses, test results and photos stay in the clinic\'s medical system. The law does not split data into '
  'admin and clinical, so whether even bookings and payments can be kept in the cloud is for the clinic\'s lawyer to decide. If '
  'not, or if the clinical side is needed in the CRM, we install on-premise Bitrix24 on a server in the UAE.'),
 ('How does Bitrix24 help with no-shows?',
  'Bitrix24 Booking sends the client WhatsApp messages: the booking details, a request to confirm the visit via a link (one day '
  'ahead by default), a reminder on the day and a message if the client is running late. Unconfirmed bookings are highlighted, '
  'the receptionist gets an activity, and a freed slot can go to a client on the waitlist. For services with a repeat cycle, '
  'automation rules remind clients about the next visit if they agreed to such messages.'),
 ('Can we send WhatsApp broadcasts to patients?',
  'Yes, to people who gave you their number and agreed to receive messages, and a request to stop must be honoured: that is what '
  'WhatsApp rules require. DHA-licensed clinics must write the texts under the DHA standards for medical advertising on social '
  'media, where WhatsApp counts as social media too: no "the best", "100%", "no side effects" or "immediate results", and posts '
  'that name the clinic are approved by the medical director. Cabinet Resolution No. 56 of 2024 (Article 1) treats marketing '
  'text messages and marketing messages through social media apps as telemarketing, just like calls.'),
 ('How much does Bitrix24 cost for a clinic or salon?',
  'Standard Bitrix24 CRM setup starts from AED 10,000, and the quote is fixed in dirhams after the review, before the work '
  'starts. In the Bitrix24 cloud, Booking is part of the Professional plan and above; the Bitrix24 licence and WhatsApp messages '
  'are paid separately. Integration with the medical system is quoted after the review, and after launch the system is '
  'maintained under support packages from AED 1,250 a month.'),
]
for q, a in FAQ_RU + FAQ_EN:
    assert not any(d in q + a for d in DASHES)
s = io.open('.seo/faq_data.py', encoding='utf-8').read()
if MARK in s:
    print('%-32s уже есть' % '.seo/faq_data.py')
else:
    assert s.count("],\n}\n\nFAQ_EN = {") == 1
    s = s.replace("],\n}\n\nFAQ_EN = {", "],\n" + qa_block('bitrix-clinics.html', FAQ_RU) + "}\n\nFAQ_EN = {", 1)
    assert s.rstrip().endswith('],\n}'), s[-80:]
    s = s.rstrip()[:-1] + qa_block('en/bitrix-clinics.html', FAQ_EN) + '}\n'
    io.open('.seo/faq_data.py', 'w', encoding='utf-8').write(s)
    print('%-32s добавлено' % '.seo/faq_data.py')

# 3. llms.txt, русский список, sitemap
MIG_TAIL = "on a server in the UAE\\n' % BASE)"
LINE = ("- [Bitrix24 for clinics and beauty salons in Dubai](%s/en/bitrix-clinics): Bitrix24 Booking for doctors, stylists, rooms "
        "and devices with WhatsApp messages for new bookings, confirmation requests, same-day reminders and late arrivals, online "
        "booking forms and a waitlist; clinical records stay in the medical system of the clinic, because UAE Federal Law No. 2 of "
        "2019 (Articles 13 and 20) bars storing health data outside the country except in cases set by the health authority and "
        "requires keeping it for at least 25 years, while bitrix24.ae cloud accounts are hosted on AWS in Frankfurt and the "
        "on-premise edition can run on a server in the UAE; consents for WhatsApp messages, marketing calls (9am to 6pm under "
        "Article 5 of Cabinet Resolution No. 56 of 2024) and patient photos in ads (DHA standards for medical advertising on social "
        "media, circular of 17 August 2026) are kept in the client record")
assert "'" not in LINE and '%' not in LINE.replace('%s', '') and not any(d in LINE for d in DASHES)
LLMS = "on a server in the UAE' % BASE)\nL.append('" + LINE + "\\n' % BASE)"
patch('.seo/build_d.py', [
    (MIG_TAIL, LLMS),
    ("('bitrix-migration.html', '/bitrix-migration'), ",
     "('bitrix-migration.html', '/bitrix-migration'), ('bitrix-clinics.html', '/bitrix-clinics'), "),
    ("('bitrix-migration', '0.8'), ", "('bitrix-migration', '0.8'), ('bitrix-clinics', '0.8'), "),
])

# 4. Карточка в блоке «Решения для ОАЭ» на /bitrix и /en/bitrix (девятая: сетка 3+3+3)
patch('.seo/uae/link_solutions.py', [
    ("без остановки продаж', '/bitrix-migration')]),\n 'en':",
     "без остановки продаж', '/bitrix-migration'),\n   ('Медицина и красота', 'Клиники и салоны', 'Онлайн-запись, напоминания "
     "в WhatsApp, согласия клиентов и медданные по закону ОАЭ', '/bitrix-clinics')]),\n 'en':"),
    ("without stopping sales', '/bitrix-migration')]),\n}",
     "without stopping sales', '/bitrix-migration'),\n   ('Health and beauty', 'Clinics and salons', 'Online booking, WhatsApp "
     "reminders, client consents and health data under UAE law', '/bitrix-clinics')]),\n}"),
])
