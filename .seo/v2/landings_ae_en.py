# -*- coding: utf-8 -*-
# makebiztechnologies.com landing pages, wave 1, EN (23.10.2026). Included from build_en_ae.py via exec() before the chrome block
# Prices only from /en/pricing. HubSpot: hubspot.com/pricing/sales on 23.10.2026
LA_DATE = 'October 23, 2026'

def la_tbl(head, rows, note=''):
    th = ''.join('<th>' + esc(h) + '</th>' for h in head)
    tr = ''
    for r in rows:
        tr += '<tr><td><b>' + r[0] + '</b></td><td class="pt-p">' + r[1] + '</td>' + ''.join('<td>' + c + '</td>' for c in r[2:]) + '</tr>'
    n = ('<p class="note">' + note + '</p>') if note else ''
    return '<div class="ptw gl"><table class="ptab"><thead><tr>' + th + '</tr></thead><tbody>' + tr + '</tbody></table></div>' + n

def la_mid(h3, text, btn):
    return ('<section class="sec dark"><div class="wrap"><div class="cross"><div><h3>' + esc(h3) + '</h3><p>' + esc(text)
            + '</p></div><a class="btn" href="#form">' + esc(btn) + '</a></div></div></section>')

def LA(path, text): return '<a href="' + U(path) + '">' + text + '</a>'

LA_PRICES = [
    ('Standard CRM setup', 'from AED 10,000', 'up to 20 users, launch from 14 days'),
    ('Work beyond the standard', 'AED 200 per hour', 'estimate in AED fixed before start'),
    ('WhatsApp or another messenger', 'AED 500', 'provider subscription separate'),
    ('Accounting integration', 'from AED 10,000', 'Zoho Books, QuickBooks, Odoo'),
    ('BI analytics', 'from AED 1,000', 'after the list of metrics'),
    ('Support after launch', 'from AED 1,250', 'a month, 5-hour package'),
    ('Bitrix24 license', 'from AED 180', 'a month, cloud Basic billed annually, bitrix24.ae price'),
]
def la_prices(keys=None, extra=None):
    rows = [r for r in LA_PRICES if keys is None or r[0] in keys]
    if extra: rows = extra + rows
    return la_tbl(['Work', 'Price', 'Terms'], rows, 'Prices as of ' + LA_DATE + ', excluding VAT. All prices on the ' + LA('/ceny', 'pricing page'))

def la_page(d):
    b = hero(d['eyebrow'], d['h1'], d['lead'], d['answer'], ('#form', d['cta']), ('#price', 'Pricing'), d['vis'], d['chips'], d['alt'])
    b += d['sections'][0]
    b += section(d['table_title'], d.get('table_sub', ''), d['table'], id_='price', tone='tint')
    b += la_mid(*d['mid'])
    for s in d['sections'][1:]: b += s
    if d.get('cases'): b += section('Cases', 'Real MakeBiz projects', case_cards(d['cases']), tone='tint')
    b += contract_block() + faq(d['faq']) + form_block(d['slug'], d['form'][0], d['form'][1]) + crosslink('ai')
    page(d['path'], d['slug'], d['title'], d['desc'], 'bitrix', b,
         [service_ld(d['svc'][0], d['svc'][1], en_path(d['path']), d['svc'][2])],
         [('/', 'Home'), ('/bitrix', 'Bitrix24'), (d['path'], d['crumb'])], d['faq'])

# ---------------------------------------------------------------- 1. Bitrix24 vs HubSpot
la_page(dict(path='/bitrix-vs-hubspot', slug='bitrix-vs-hubspot', crumb='Bitrix24 vs HubSpot',
    title='Bitrix24 vs HubSpot for a UAE company | MakeBiz',
    desc='Bitrix24 vs HubSpot in the UAE: pricing model, scope, WhatsApp, VAT. Bitrix24 Standard for 50 users is AED 364 a month vs paying for every seat.',
    eyebrow='CRM comparison · UAE', h1='Bitrix24 vs <span>HubSpot</span>',
    lead='Both are good systems. The difference is the pricing model, what is included and how many extra tools you end up buying around the CRM',
    answer='The main difference for a UAE company: Bitrix24 is priced per company (Standard for up to 50 users is AED 364 a month billed annually, bitrix24.ae price), while HubSpot Sales Hub is priced per seat (Professional from $90 per seat a month plus a required $1,500 onboarding, hubspot.com prices as of ' + LA_DATE + '). The bigger the team, the bigger the gap. MakeBiz Technologies implements Bitrix24, setup from AED 10,000.',
    cta='Compare on your numbers', vis=V_BOARD,
    chips=[('AED 364', 'Standard, 50 users, a month'), ('$90+', 'HubSpot Pro per seat'), ('$1,500', 'HubSpot Pro onboarding'), ('Partner', 'Bitrix24')],
    alt='Bitrix24 and HubSpot comparison',
    sections=[
        section('When to choose which', 'Honestly, each system has its strength', cards([
            ('Bitrix24 fits', 'A team of 10 or more, you need tasks, documents, telephony and chats in one system, a predictable company-wide price and an on-premise option'),
            ('HubSpot fits', 'Marketing and content come first, the sales team is small, you rely on English-language marketing integrations and per-seat pricing is not a concern'),
        ], 2)),
        section('Example for 25 sales reps', 'Illustrative figures from vendor price lists as of ' + LA_DATE + '. Rate 3.6725',
            '<div class="card"><p>Bitrix24 Standard covers up to 50 users: AED 364 a month billed annually, about AED 4,370 a year for the whole company. HubSpot Sales Hub Professional: from $90 per seat a month, for 25 seats that is from $2,250 a month, about AED 8,260, plus a one-time $1,500 onboarding. Our Bitrix24 setup starts at AED 10,000. We will run the exact comparison for your team on a call</p></div>'),
        section('How we move you off HubSpot', '', steps([
            ('Export', 'Companies, contacts, deals and history from HubSpot'),
            ('Field mapping', 'We map fields and stages and leave clutter behind'),
            ('Migration and check', 'We migrate and reconcile counts and amounts'),
            ('Training', 'We switch the team over and stay on support for the first weeks'),
        ]), tone='tint'),
        section('More on switching', '', '<div class="card"><p>The migration steps are on the ' + LA('/bitrix-migration', 'switching to Bitrix24') + ' page. For another popular CRM, see ' + LA('/bitrix-vs-zoho', 'Bitrix24 vs Zoho') + '. License prices in AED with the check date are on the ' + LA('/bitrix-licenses', 'Bitrix24 pricing') + ' page</p></div>'),
    ],
    table_title='Side by side', table_sub='Vendor data as of ' + LA_DATE + '. Features depend on the plan',
    table=la_tbl(['Point', 'Bitrix24', 'HubSpot Sales Hub'], [
        ('Pricing model', 'per company, plan by number of users', 'per seat'),
        ('Example price', 'Standard up to 50 users: AED 364 a month billed annually', 'Professional: from $90 per seat a month'),
        ('Required onboarding', 'none', '$1,500 (Professional), $3,500 (Enterprise)'),
        ('Tasks, documents, chats', 'in one system', 'focus on CRM and marketing'),
        ('On-premise version', 'yes, from AED 13,184 a year', 'no, cloud only'),
        ('WhatsApp', 'via connectors, our setup AED 500', 'via integrations'),
    ], 'Bitrix24: bitrix24.ae, HubSpot: hubspot.com/pricing/sales, checked ' + LA_DATE + '. USD/AED 3.6725'),
    mid=('We will calculate the total cost for your team', 'Tell us the number of users and the features you need, we compare both systems over three years in AED', 'Get the comparison'),
    cases=['cdek-b2b', 'unilin-crm', 'performia-crm'],
    faq=[
        ('Which is cheaper for a UAE company, Bitrix24 or HubSpot?', 'For a team of 10 or more it is usually Bitrix24: it is priced per company, while HubSpot charges per seat plus a required onboarding on Professional and Enterprise. For a small marketing team the gap is smaller.'),
        ('Can you move data from HubSpot to Bitrix24?', 'Yes: companies, contacts, deals and history. We estimate scope after the export, the work is AED 200 per hour.'),
        ('Does Bitrix24 support 5% VAT invoices?', 'Yes, products with tax and the invoice template are part of the standard setup. For accounting we connect your accounting system.'),
        ('Who helps with the license?', 'We are an official Bitrix24 partner in the UAE: we pick the plan and handle the purchase.'),
    ],
    form=('Let us compare Bitrix24 and HubSpot for you', 'Tell us your team size and what matters. We reply within a business day'),
    svc=('Bitrix24 implementation instead of HubSpot', 'Comparison and migration to Bitrix24 for UAE companies', 10000)))

# ---------------------------------------------------------------- 2. Audit
la_page(dict(path='/bitrix-audit', slug='bitrix-audit', crumb='Bitrix24 audit',
    title='Bitrix24 portal audit in Dubai and the UAE | MakeBiz',
    desc='Bitrix24 audit: permissions, pipelines, automation, WhatsApp, reports. First review free, work AED 200 per hour, fixes in a support package from AED 1,250.',
    eyebrow='Bitrix24 · portal audit', h1='Bitrix24 <span>portal audit</span>',
    lead='We find out why the CRM does not work as intended: where leads get lost, who sees what they should not and which reports are wrong',
    answer='MakeBiz Technologies, an official Bitrix24 partner in the UAE, audits live portals: permissions, pipelines and fields, automation rules, WhatsApp and telephony, reports. The first 30-60 minute review is free, an in-depth audit is AED 200 per hour, and fixes can run inside a support package from AED 1,250 a month. Prices as of ' + LA_DATE + '.',
    cta='Book a review', vis=V_TICKETS,
    chips=[('Free', 'first review'), ('AED 200/h', 'in-depth audit'), ('from AED 1,250', 'fixes in a package'), ('Partner', 'Bitrix24')],
    alt='Bitrix24 portal audit',
    sections=[
        section('What we check', '', cards([
            ('Permissions', 'Who sees the client base, who can export or delete. More in our news on ' + LA('/news/prava-dostupa-v-crm-kto-chto-vidit', 'CRM access rights')),
            ('Pipelines and fields', 'Do the stages match the real customer path, are there dead fields'),
            ('Lead sources', 'WhatsApp, website, calls: do they all land in the CRM with a source'),
            ('Automation', 'What fires, what broke long ago or runs twice'),
            ('Invoices and VAT', 'Templates, products, tax, the link to accounting'),
            ('Reports', 'Do reports count what management thinks they count'),
        ], 3)),
        section('How the audit works', '', steps([
            ('Free review', '30-60 minutes on a video call, we spot the main issues'),
            ('Access and checks', 'A separate user account, we review settings and data'),
            ('Report', 'Issues by priority, what to fix and how many hours'),
            ('Fixes', 'On your own or with us, by the hour or in a support package'),
        ])),
        section('Signs it is time for an audit', '', cards([
            ('Reps work outside the CRM', 'Deals live in spreadsheets and personal WhatsApp'),
            ('Management does not trust reports', 'CRM numbers do not match accounting'),
            ('Your admin has left', 'Nobody knows how or why the automation was set up'),
            ('Before the team grows', 'New hires will inherit today’s mistakes'),
        ], 2), tone='tint'),
    ],
    table_title='What the audit costs', table_sub='You pay for hours, not a template',
    table=la_tbl(['Format', 'Price', 'Terms'], [
        ('First portal review', 'free', '30-60 minutes on a video call'),
        ('In-depth audit', 'AED 200 per hour', 'scope named after the review'),
        ('Fixes in a support package', 'from AED 1,250', 'a month, 5 hours; 10 hours AED 2,300, 20 hours AED 4,200'),
        ('Hour beyond the package', 'AED 250', 'as used'),
    ], 'Prices as of ' + LA_DATE + ', excluding VAT. Packages in detail on the ' + LA('/bitrix-support', 'support page')),
    mid=('We will find where your portal loses leads', 'Free 30-60 minute review, no data access needed at the first step', 'Book a review'),
    cases=['cdek-b2b', 'unilin-crm', 'performia-crm'],
    faq=[
        ('How much does a Bitrix24 audit cost?', 'The first review is free. An in-depth audit is AED 200 per hour, scope named after the review. Fixes can run inside a support package from AED 1,250 a month.'),
        ('Do you need access to the portal?', 'Not for the first review, screen sharing is enough. For the in-depth audit we use a separate account and remove access afterwards.'),
        ('Can you audit a portal set up by another partner?', 'Yes, that is common. We do not rebuild from scratch, we fix what gets in the way.'),
        ('What do we get?', 'A prioritised list of issues, how to fix each one, and an estimate in hours and AED.'),
    ],
    form=('Book a portal review', 'Tell us what is not working. We reply within a business day'),
    svc=('Bitrix24 audit', 'Audit of a live Bitrix24 portal for UAE companies', None)))

# ---------------------------------------------------------------- 3. Training
la_page(dict(path='/bitrix-training', slug='bitrix-training', crumb='Training',
    title='Bitrix24 team training in Dubai, EN and RU | MakeBiz',
    desc='Corporate Bitrix24 training on your own portal, in English or Russian: sales reps, managers, admin. AED 200 per hour or inside a support package.',
    eyebrow='Bitrix24 · training', h1='Bitrix24 <span>team training</span>',
    lead='We train on your portal and your deals, in English or Russian, with separate sessions for reps, managers and the admin',
    answer='MakeBiz Technologies trains UAE teams to work in Bitrix24 online or in Dubai: deals, WhatsApp and tasks for reps, reports and control for managers, permissions and automation for the admin. Training is AED 200 per hour or part of a support package from AED 1,250 a month, and intro training is included in the standard setup from AED 10,000.',
    cta='Order training', vis=V_TICKETS,
    chips=[('AED 200/h', 'training'), ('EN and RU', 'languages'), ('3 roles', 'rep, manager, admin'), ('Partner', 'Bitrix24')],
    alt='Bitrix24 team training',
    sections=[
        section('Who we train and on what', '', cards([
            ('Sales reps', 'Deals, tasks, WhatsApp and calls from the CRM, VAT invoices from the record'),
            ('Managers', 'Pipeline, reports, targets, running a weekly meeting from the CRM'),
            ('Admin', 'Users and permissions, fields, stages, automation'),
            ('New hires', 'A short onboarding course with recorded sessions'),
        ], 2)),
        section('How training works', '', steps([
            ('Review', 'We look at the portal and where the team slips'),
            ('Programme', 'Sessions by role and language'),
            ('Sessions', 'Online or in Dubai, on your portal'),
            ('Follow-up', 'Two weeks later we check the work and close gaps'),
        ])),
        section('Why mixed teams learn separately', '', '<div class="card"><p>Many Dubai teams work in several languages. Training everyone together means half the room listens to a translation. We split groups by role and language and give a CRM working guide in English and Russian. Role-based access is covered in our news on ' + LA('/news/prava-dostupa-v-crm-kto-chto-vidit', 'who sees what in the CRM') + '</p></div>', tone='tint'),
    ],
    table_title='What training costs', table_sub='You pay for hours',
    table=la_tbl(['Format', 'Price', 'Terms'], [
        ('Intro training at launch', 'included', 'in the standard setup from AED 10,000'),
        ('Corporate training', 'AED 200 per hour', 'programme by role, EN or RU'),
        ('Training in a support package', 'from AED 1,250', 'a month, 5 hours for training and improvements'),
    ], 'Prices as of ' + LA_DATE + ', excluding VAT'),
    mid=('We will build a programme for your team', 'Team size, roles and languages, and we propose a programme and count the hours', 'Get a programme'),
    cases=['performia-crm', 'unilin-crm', 'cdek-b2b'],
    faq=[
        ('How much does Bitrix24 training cost in the UAE?', 'Corporate training is AED 200 per hour or part of a support package from AED 1,250 a month. Intro training is included in the standard setup.'),
        ('What language are sessions in?', 'English or Russian, groups are split by language.'),
        ('Can you train in our Dubai office?', 'Yes, we meet in Dubai or run sessions online.'),
        ('Will you train our admin?', 'Yes: permissions, fields, stages and automation. Complex changes stay with us in the support package.'),
    ],
    form=('We will train your team', 'Tell us the team size and languages. We reply within a business day'),
    svc=('Bitrix24 training', 'Corporate Bitrix24 training for UAE companies', None)))

# ---------------------------------------------------------------- 4. Car rental
la_page(dict(path='/bitrix-car-rental', slug='bitrix-car-rental', crumb='CRM for car rental',
    title='CRM for a car rental company in Dubai | MakeBiz',
    desc='CRM for car rental in Dubai on Bitrix24: leads from WhatsApp and the website, bookings, deposits, returns. Setup from AED 10,000, WhatsApp AED 500.',
    eyebrow='CRM · car rental', h1='CRM for <span>car rental</span>',
    lead='Leads from WhatsApp and the website, bookings by date, deposits, handover and return in one system instead of reps’ chats',
    answer='MakeBiz Technologies sets up CRM for car rental companies in Dubai on Bitrix24: leads from WhatsApp, the website and aggregators, bookings by date and car class, deposit and payment, handover and return with photos, repeat rentals. Standard setup from AED 10,000, WhatsApp connection AED 500, rental-specific work AED 200 per hour. Prices as of ' + LA_DATE + '.',
    cta='Discuss a rental CRM', vis=V_CHAT,
    chips=[('from AED 10,000', 'setup'), ('AED 500', 'WhatsApp'), ('AED 200/h', 'custom work'), ('Partner', 'Bitrix24')],
    alt='CRM for car rental',
    sections=[
        section('What we set up for rental', '', cards([
            ('One lead pipeline', 'WhatsApp, website, calls and aggregators with source and owner'),
            ('Bookings by date', 'Car class, dates, pick-up point, reminders to the client'),
            ('Deposit and payment', 'Payment stages, invoice with 5% VAT, deposit refund'),
            ('Handover and return', 'Checklist and photos in the record, fines and extra charges'),
            ('Repeat clients', 'Rental history and an offer for the next visit'),
            ('Reports', 'Utilisation, revenue by car class and lead source'),
        ], 3)),
        section('Where rental companies lose money', '', cards([
            ('Slow WhatsApp replies', 'The client messages three companies and books with whoever answers first'),
            ('Bookings in a chat', 'Two bookings for one car and an awkward call'),
            ('Deposits in a spreadsheet', 'Nobody sees what to refund and what to hold'),
            ('No repeat sales', 'The tourist left, the resident is forgotten'),
        ], 2), tone='tint'),
        section('Answer first on WhatsApp', '', '<div class="card"><p>If lead volume is high, an ' + LA('/ai-agents/rop', 'AI agent') + ' (from AED 5,000) can send the first reply and confirm dates, and the rep takes over a ready lead. How it works is in our news on ' + LA('/news/ai-agent-v-whatsapp-vhodyashchie-zayavki', 'an AI agent on WhatsApp') + '. Channel setup is on the ' + LA('/bitrix-messengers', 'WhatsApp in Bitrix24') + ' page</p></div>'),
    ],
    table_title='What a rental CRM costs', table_sub='Our work, the Bitrix24 license is separate',
    table=la_prices(['Standard CRM setup', 'Work beyond the standard', 'WhatsApp or another messenger', 'Support after launch', 'Bitrix24 license'],
        extra=[('Bookings, deposits, handover and return', 'AED 200 per hour', 'scope after the survey, estimate before start')]),
    mid=('We will show a rental pipeline in a demo', 'Fleet size and lead sources, we show how it looks in the CRM and give a price', 'Book a demo'),
    cases=['apartika-crm', 'cdek-b2b', 'performia-crm'],
    faq=[
        ('Does Bitrix24 work for car rental?', 'Yes. Leads, bookings, payments and returns are set up as a pipeline and separate processes with car and date fields.'),
        ('How much does a rental CRM cost in Dubai?', 'Standard setup from AED 10,000, WhatsApp AED 500, rental-specific work AED 200 per hour after a survey. The Bitrix24 license is separate, from AED 180 a month.'),
        ('Can deposits be tracked in the CRM?', 'Yes, as a separate stage and fields in the deal, with a refund reminder.'),
        ('Can you connect several WhatsApp numbers?', 'Yes, each number is connected to the CRM and the chat stays in the client record.'),
    ],
    form=('Let us discuss your rental CRM', 'Tell us your fleet size and where leads come from. We reply within a business day'),
    svc=('CRM for car rental', 'Bitrix24 implementation for car rental companies in the UAE', 10000)))

# ---------------------------------------------------------------- 5. Logistics
la_page(dict(path='/bitrix-logistics', slug='bitrix-logistics', crumb='CRM for logistics',
    title='CRM for a logistics company in the UAE | MakeBiz',
    desc='CRM for logistics and freight forwarding in the UAE on Bitrix24: rate requests, quotes, shipments, B2B clients, accounting link. Setup from AED 10,000.',
    eyebrow='CRM · logistics', h1='CRM for a <span>logistics company</span>',
    lead='Rate requests, quotes, shipments and corporate clients in one system instead of email threads and spreadsheets',
    answer='MakeBiz Technologies implements CRM for logistics and freight forwarding companies in the UAE on Bitrix24: rate requests from email and WhatsApp, quotes from a template, shipments by stage, contracts with B2B clients and a link to your accounting system. Standard setup from AED 10,000, integration with Zoho Books, QuickBooks or Odoo from AED 10,000. Our cases include CDEK: corporate B2B on Bitrix24.',
    cta='Discuss a logistics CRM', vis=V_SYNC,
    chips=[('from AED 10,000', 'setup'), ('from AED 10,000', 'accounting link'), ('B2B', 'CDEK case'), ('Partner', 'Bitrix24')],
    alt='CRM for a logistics company',
    sections=[
        section('What we set up for logistics', '', cards([
            ('Rate requests', 'Emails and messages become a request with route and cargo'),
            ('Quotes from a template', 'Rate, terms and timing from the record, in English and Russian'),
            ('Shipments by stage', 'A separate shipment process with statuses and owners'),
            ('Corporate clients', 'Contracts, several contacts, shipment history'),
            ('Accounting link', 'VAT invoices and payments, see ' + LA('/bitrix-integrations', 'accounting integrations')),
            ('Reports', 'Request to shipment conversion, margin by client'),
        ], 3)),
        section('Where logistics loses money', '', cards([
            ('Unanswered rate request', 'The client waits a day for a quote and goes to whoever replied in an hour'),
            ('Rates buried in email', 'Nobody knows what price the client got last time'),
            ('Shipment without an owner', 'The client hears about a delay before the rep does'),
            ('No view of margin', 'Revenue is there, profitable clients are not visible'),
        ], 2), tone='tint'),
        section('More', '', '<div class="card"><p>How to link sales and money is on the ' + LA('/bitrix-distribution', 'CRM for trading and distribution') + ' page. A single view of clients and margin comes from ' + LA('/bi-analitika', 'BI analytics') + ' from AED 300 a month. What calls reveal that never reaches the CRM is in our news on ' + LA('/news/chto-teryaetsya-mezhdu-zvonkom-i-kartochkoy-sdelki', 'calls and the CRM record') + '</p></div>'),
    ],
    table_title='What a logistics CRM costs', table_sub='Our work, the Bitrix24 license is separate',
    table=la_prices(['Standard CRM setup', 'Work beyond the standard', 'Accounting integration', 'BI analytics', 'Support after launch', 'Bitrix24 license']),
    mid=('We will map the path from request to shipment', 'Tell us how rate requests and shipments run today, we return a CRM map and an estimate in AED', 'Get a map'),
    cases=['cdek-b2b', 'unilin-crm', 'haval-vector'],
    faq=[
        ('Does Bitrix24 work for a logistics company?', 'Yes. Requests and quotes run in the sales pipeline, shipments in a separate process with their own statuses, and invoices and payments come from accounting.'),
        ('How much does a logistics CRM cost in the UAE?', 'Standard setup from AED 10,000, accounting integration from AED 10,000, BI from AED 300 a month. The exact estimate is fixed after a survey.'),
        ('Can rate requests come from email?', 'Yes, the mailbox is connected to the CRM and an email creates a request with an owner.'),
        ('Do you work with our TMS or WMS?', 'If the system has an API, we scope the data exchange in the survey at AED 200 per hour.'),
    ],
    form=('Let us discuss your logistics CRM', 'Tell us what you move and which accounting system you use. We reply within a business day'),
    svc=('CRM for logistics', 'Bitrix24 implementation for logistics and freight forwarding companies in the UAE', 10000)))

# ---------------------------------------------------------------- 6. Education
la_page(dict(path='/bitrix-education', slug='bitrix-education', crumb='CRM for education',
    title='CRM for a training centre or school in the UAE | MakeBiz',
    desc='CRM for training centres and schools in the UAE on Bitrix24: enquiries, trial lessons, payments, groups, WhatsApp. Setup from AED 10,000.',
    eyebrow='CRM · education', h1='CRM for a <span>training centre</span>',
    lead='Enquiries, trial lessons, payments and groups in one system: the admin sees whom to call back, the owner sees enrolment and money',
    answer='MakeBiz Technologies sets up CRM for training centres, courses and private schools in the UAE on Bitrix24: enquiries from WhatsApp and the website, booking a trial lesson, contract and instalment payments, groups and timetable, course renewals. Standard setup from AED 10,000, WhatsApp AED 500. Our cases include Performia: sales, training and finance in one system.',
    cta='Discuss a school CRM', vis=V_BOARD,
    chips=[('from AED 10,000', 'setup'), ('AED 500', 'WhatsApp'), ('Case', 'Performia'), ('Partner', 'Bitrix24')],
    alt='CRM for a training centre',
    sections=[
        section('What we set up for education', '', cards([
            ('Enrolment', 'Enquiries from WhatsApp, the website and social media with a source'),
            ('Trial lesson', 'Booking, reminder, attendance mark'),
            ('Contract and payment', 'Instalments, payment reminders, VAT invoice'),
            ('Groups', 'Group lists and timetable as a separate process'),
            ('Renewals', 'Automation reminds about the course end and offers the next one'),
            ('Reports', 'Enrolment by source, trial to contract conversion, revenue'),
        ], 3)),
        section('Where schools lose students', '', cards([
            ('Enquiry without a call', 'A parent left a number in the evening, by morning it is forgotten'),
            ('Trial without a next step', 'They came, liked it, nobody offered a contract'),
            ('Payments in a spreadsheet', 'Arrears show up only at month end'),
            ('No renewals', 'The course ended and the student moved to a competitor'),
        ], 2), tone='tint'),
        section('More', '', '<div class="card"><p>Evening and weekend replies to parents on WhatsApp can come from an ' + LA('/ai-agents/rop', 'AI agent') + ', and the admin gets ready bookings in the morning. Channel setup is on the ' + LA('/bitrix-messengers', 'WhatsApp in Bitrix24') + ' page. See how a training and finance project works in the ' + LA('/keysy/performia-crm', 'Performia case') + '</p></div>'),
    ],
    table_title='What a school CRM costs', table_sub='Our work, the Bitrix24 license is separate',
    table=la_prices(['Standard CRM setup', 'Work beyond the standard', 'WhatsApp or another messenger', 'BI analytics', 'Support after launch', 'Bitrix24 license'],
        extra=[('Groups, timetable, instalments', 'AED 200 per hour', 'scope after the survey, estimate before start')]),
    mid=('We will show an enrolment pipeline in a demo', 'Number of students and courses, we show how it looks and give a price', 'Book a demo'),
    cases=['performia-crm', 'apartika-crm', 'cdek-b2b'],
    faq=[
        ('Does Bitrix24 work for a training centre?', 'Yes. Enrolment runs in a pipeline, groups and timetable in a separate process, instalments with their own stages and reminders.'),
        ('How much does a school CRM cost in the UAE?', 'Standard setup from AED 10,000, WhatsApp AED 500, custom work AED 200 per hour after a survey. The Bitrix24 license is separate.'),
        ('Can payment reminders be automatic?', 'Yes, automation messages the parent or sets a task for the admin before the due date.'),
        ('Do you have an example project?', 'Yes, the Performia case: sales, training, finance and end-to-end analytics in one system.'),
    ],
    form=('Let us discuss your school CRM', 'Tell us how many courses you run and where students come from. We reply within a business day'),
    svc=('CRM for a training centre', 'Bitrix24 implementation for training centres and schools in the UAE', 10000)))

# ---------------------------------------------------------------- 7. Recruitment
la_page(dict(path='/bitrix-recruitment', slug='bitrix-recruitment', crumb='CRM for recruitment',
    title='CRM for a recruitment agency in the UAE | MakeBiz',
    desc='CRM for recruitment agencies in the UAE on Bitrix24: clients, jobs, candidates, selection stages, an AI agent for screening. Setup from AED 10,000.',
    eyebrow='CRM · recruitment', h1='CRM for a <span>recruitment agency</span>',
    lead='Clients, jobs and candidates are linked: recruiters see the selection stage, the owner sees filled positions and revenue',
    answer='MakeBiz Technologies sets up CRM for recruitment agencies and in-house HR teams in the UAE on Bitrix24: clients and contracts, jobs as a separate process, candidates by selection stage, interviews and offers, invoices to clients. Standard setup from AED 10,000, and an HR agent from AED 5,000 can run first-round screening. Prices as of ' + LA_DATE + '.',
    cta='Discuss an agency CRM', vis=V_AGENTS,
    chips=[('from AED 10,000', 'setup'), ('from AED 5,000', 'HR agent'), ('Jobs', 'and candidates'), ('Partner', 'Bitrix24')],
    alt='CRM for a recruitment agency',
    sections=[
        section('What we set up for recruitment', '', cards([
            ('Clients and contracts', 'Hiring companies, terms, contacts'),
            ('Jobs', 'A separate process with statuses from open to filled'),
            ('Candidates', 'Selection stages, CV, interviews, offer'),
            ('Job to candidate link', 'Every job shows all candidates and their stage'),
            ('Client invoices', 'A VAT invoice when a position is filled'),
            ('Reports', 'Time to fill, stage conversion, revenue by client'),
        ], 3)),
        section('Where an AI agent saves recruiter time', '', '<div class="card"><p>The ' + LA('/ai-agents/hr', 'HR agent') + ' runs a first interview in a Telegram bot, scores the answers and hands the recruiter a shortlist. Recruiters spend time on strong candidates, not on a first call to everyone. Why such projects sometimes stall and how to avoid it is in our news on ' + LA('/news/pochemu-vnedrenie-ai-agentov-buksuet', 'AI agent rollout mistakes') + '</p></div>'),
        section('Typical mistakes', '', cards([
            ('Candidates in email', 'CVs get lost, one candidate lands with two recruiters'),
            ('Jobs without a status', 'The client asks for an update and the recruiter digs through chats'),
            ('No history', 'A strong candidate from a past job is forgotten'),
            ('Open access', 'Everyone sees candidates’ personal data, more in our news on ' + LA('/news/prava-dostupa-v-crm-kto-chto-vidit', 'access rights')),
        ], 2), tone='tint'),
    ],
    table_title='What a recruitment CRM costs', table_sub='Our work, the Bitrix24 license is separate',
    table=la_prices(['Standard CRM setup', 'Work beyond the standard', 'Support after launch', 'Bitrix24 license'],
        extra=[('Jobs and candidates, links and stages', 'AED 200 per hour', 'scope after the survey'), ('HR agent for screening', 'from AED 5,000', 'maintenance 10% of the cost a month')]),
    mid=('We will show the HR agent on your jobs', 'A free 30-40 minute demo, then we price the CRM and the agent in AED', 'Book a demo'),
    cases=['performia-crm', 'cdek-b2b', 'unilin-crm'],
    faq=[
        ('Does Bitrix24 work for a recruitment agency?', 'Yes. Clients and deals live in the CRM, jobs and candidates in separate linked processes.'),
        ('How much does a recruitment CRM cost in the UAE?', 'Standard setup from AED 10,000, custom work AED 200 per hour, HR agent from AED 5,000. The Bitrix24 license is separate.'),
        ('How is candidate data protected?', 'Access is set by role: a recruiter sees their own candidates, the manager sees everyone.'),
        ('What does the HR agent do?', 'It runs a first interview in a Telegram bot, scores the answers and passes a shortlist to the recruiter.'),
    ],
    form=('Let us discuss your agency CRM', 'Tell us how many recruiters and jobs a month. We reply within a business day'),
    svc=('CRM for recruitment', 'Bitrix24 implementation for recruitment agencies in the UAE', 10000)))
