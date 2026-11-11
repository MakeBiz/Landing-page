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

# ================================================================ Wave 2 (11.11.2026), EN
# Prices only from /en/pricing on 11.11.2026; topics and sources as in the wave 2 block of landings_ae.py. British spelling in new text
LA_DATE2 = 'November 11, 2026'
_LA_UPD = (UPDATED, UPDATED_ISO)
UPDATED, UPDATED_ISO = LA_DATE2, '2026-11-11'

def la2_tbl(rows, extra_note=''):
    return la_tbl(['Work', 'Price', 'Terms'], rows, 'Prices as of ' + LA_DATE2 + ', excluding VAT' + extra_note + '. ' + LA('/ceny', 'All prices'))
LA2_SETUP = ('Standard CRM setup', 'from AED 10,000', 'up to 20 users, from 14 days')
def LA2_HOUR(what): return (what, 'AED 200 per hour', 'estimate before start')
LA2_WA = ('WhatsApp or another messenger', 'AED 500', 'provider subscription separate')
LA2_SUP = ('Support after launch', 'from AED 1,250', 'a month, 5 hours')
LA2_BI = ('BI analytics', 'from AED 300', 'a month; Standard AED 700, Pro AED 1,000')
LA2_LIC = ('Bitrix24 licence', 'from AED 180', 'a month, Basic for 5 users, billed annually')
def la2_card(text): return '<div class="card"><p>' + text + '</p></div>'

# ---------------------------------------------------------------- 8. AI-powered CRM
la_page(dict(path='/bitrix-ai-crm', slug='bitrix-ai-crm', crumb='AI-powered CRM',
    title='AI-powered CRM in Dubai: Bitrix24 with AI | MakeBiz',
    desc='AI-powered CRM on Bitrix24 for UAE companies: CoPilot transcribes calls and fills in fields, an AI agent replies on WhatsApp. One agent from AED 5,000.',
    eyebrow='CRM · artificial intelligence', h1='AI-powered CRM <span>for UAE business</span>',
    lead='What AI does inside Bitrix24, what agents add and what it costs',
    answer='An AI-powered CRM for a UAE company has two layers: the Bitrix24 assistant CoPilot transcribes calls, writes summaries and fills in deal fields, while MakeBiz AI agents reply to customers on WhatsApp and score calls. CRM setup from AED 10,000, one AI agent from AED 5,000, speech analytics from AED 1,000 a month. Prices as of ' + LA_DATE2 + '.',
    cta='Discuss an AI-powered CRM', vis=V_AGENTS,
    chips=[('from AED 5,000', 'one AI agent'), ('from AED 10,000', 'CRM setup'), ('AED 1,000/mo', 'speech analytics'), ('Partner', 'Bitrix24')],
    alt='AI-powered CRM on Bitrix24',
    sections=[
        section('What the Bitrix24 built-in AI does', 'Bitrix24 helpdesk, November 6, 2026', cards([
            ('Call transcript', 'Searchable text in the language of the call'),
            ('Call summary', 'The key points in the deal timeline'),
            ('Fields from the call', 'Empty fields are filled, filled ones only get a suggested change'),
            ('Script check', 'The call is scored against your sales script'),
            ('Follow-up activity', 'The next activity with a short call outcome'),
            ('Chat review', 'Chats in leads, deals, contacts and companies'),
        ], 3)),
        section('Where built-in AI is not enough', '', cards([
            ('CoPilot in the record', 'Helps with one call or chat, within plan limits'),
            ('An agent in the chat', 'The ' + LA('/ai-agents/rop', 'AI sales head') + ' replies on its own if the rep is silent for 15 minutes'),
            ('Every team call', LA('/ai-agents/zvonki', 'Speech analytics') + ' scores every call, rep by rep'),
            ('Agent or rule', 'The difference is in our news on ' + LA('/news/chem-ai-agent-otlichaetsya-ot-robota-v-crm', 'agents and rules')),
        ], 2)),
        section('Limits, plan and data', '', la2_card('Regular Bitrix24 plans have monthly AI limits, Vibe+ plans do not (Bitrix24 blog, August 17, 2026). Agents reach a cloud portal through the REST API, which per the Bitrix24 documentation now comes with Vibe+ plans, not Essentials. CoPilot runs on third-party models such as OpenAI; if data must stay with you, we deploy agents on your server, including in the UAE. Plan prices: ' + LA('/bitrix-licenses', 'Bitrix24 licences')), tone='tint'),
        section('Example: a sales team of 8', '', la2_card('An illustration, not a case. 8 reps, leads from WhatsApp and calls. CRM setup AED 10,000 plus the AI sales head on the Start package for AED 5,000, who answers in the evening and at weekends. Total AED 15,000 one-off, AED 500 a month maintenance and the licence. Speech analytics, if needed: AED 1,000 a month.')),
    ],
    table_title='What an AI-powered CRM costs', table_sub='Our work and the licence',
    table=la2_tbl([LA2_SETUP, LA2_HOUR('CoPilot setup: fields, script, rights'), ('AI agent, Start package', 'AED 5,000', 'one-off, maintenance 10% a month'), ('Speech analytics', 'from AED 1,000', 'a month for 5,000 minutes'), LA2_WA, LA2_LIC]),
    mid=('We will show AI on your calls and chats', 'A free 30-40 minute demo with prices', 'Book a demo'),
    cases=['haval-vector', 'cdek-b2b', 'apartika-crm'],
    faq=[
        ('Does Bitrix24 have built-in AI?', 'Yes, CoPilot: in the CRM it transcribes and summarises calls, fills in fields and scores calls. Usage depends on the plan.'),
        ('How much does an AI-powered CRM cost in the UAE?', 'CRM setup from AED 10,000, an AI agent from AED 5,000 plus 10% a month, speech analytics from AED 1,000 a month, licence separate.'),
        ('How is an AI agent different from CoPilot?', 'CoPilot helps an employee in the record. An agent works on its own: replies, leads the dialogue to a booking and sets a task for the rep.'),
        ('Which languages does the AI work in?', 'CoPilot uses the language of the call, our agents reply in English and Russian.'),
    ],
    form=('Let us show you an AI-powered CRM', 'Tell us your team size. We reply within a business day'),
    svc=('AI-powered CRM', 'Bitrix24 implementation with CoPilot and AI agents for UAE companies', 10000)))

# ---------------------------------------------------------------- 9. Bitrix24 development
la_page(dict(path='/bitrix-development', slug='bitrix-development', crumb='Bitrix24 development',
    title='Bitrix24 development in Dubai: API and integrations | MakeBiz',
    desc='Bitrix24 development for UAE companies: REST API, webhooks, apps, exchange with your website and in-house systems. AED 200 per hour, estimate before start.',
    eyebrow='Bitrix24 · development', h1='Bitrix24 <span>development</span>',
    lead='When the standard setup is not enough: links to your website and in-house systems, custom automation and apps inside the portal',
    answer='MakeBiz Technologies, an official Bitrix24 partner in the UAE, extends portals where the standard setup is not enough: REST API and webhook integrations, exchange with your website and in-house systems, custom apps and automation steps. AED 200 per hour with the estimate in AED fixed before start; accounting integration from AED 10,000. Prices as of ' + LA_DATE2 + '.',
    cta='Discuss development', vis=V_SYNC,
    chips=[('AED 200/hr', 'development'), ('from AED 10,000', 'accounting link'), ('REST API', 'webhooks, apps'), ('Partner', 'Bitrix24')],
    alt='Bitrix24 development and integrations',
    sections=[
        section('What we build', '', cards([
            ('Website exchange', 'Leads, orders and statuses without retyping'),
            ('In-house systems', 'Warehouse, ERP, TMS or your own database, both ways'),
            ('Custom automation steps', 'Actions the standard Bitrix24 set does not have'),
            ('Event handlers', 'A deal changes stage, the external system gets the data'),
            ('App inside the portal', 'Your own tab or widget inside Bitrix24'),
            ('Exports and reports', 'CRM data to BI and spreadsheets on a schedule'),
        ], 3)),
        section('Bitrix24 plan and REST API', 'apidocs.bitrix24.com, checked ' + LA_DATE2, la2_card('Ongoing REST API access in the cloud now comes with Vibe+ plans, not Essentials. Existing subscriptions may keep access for a transition period, and a 15-day Professional Vibe+ trial is available for testing. The cloud limit is 2 requests per second with a burst of up to 50, on Enterprise 5 and 250. On-premise, your server sets the load. So we check the plan before the estimate and for heavy exchanges consider ' + LA('/bitrix-korobka', 'on-premise Bitrix24') + '; see our news on ' + LA('/news/oblako-ili-svoy-server-dlya-crm-v-oae', 'cloud or own server'))),
        section('How we work', '', steps([
            ('Review', 'What to connect, which data, which direction'),
            ('Map and estimate', 'Objects, fields, events, hours and price in AED'),
            ('Build and test', 'Test data first, then live data'),
            ('Launch and support', 'Exchange documentation, then a support package'),
        ]), tone='tint'),
        section('Example: website and warehouse', '', la2_card('An illustration, not a case. Website leads land in a deal with their source, and warehouse stock shows in the CRM. At, say, 30 hours, that is AED 6,000. If invoices and payments are involved, it is an ' + LA('/bitrix-integrations', 'accounting integration') + ' from AED 10,000, and ' + LA('/bi-analitika', 'BI analytics') + ' from AED 300 a month gives the combined view.')),
    ],
    table_title='What development costs', table_sub='You pay for hours',
    table=la2_tbl([('Task review', 'free', '30-60 minutes by video call'), ('Development and integrations', 'AED 200 per hour', 'estimate in AED before start'), ('Accounting integration', 'from AED 10,000', 'Zoho Books, QuickBooks, Odoo, 1C'), ('Support after launch', 'from AED 1,250', 'a month, 5 hours; 10 hours AED 2,300, 20 hours AED 4,200'), ('Hour beyond a package', 'AED 250', 'as used')], '. The Bitrix24 licence is separate'),
    mid=('We will scope the work before it starts', 'Describe what needs to connect, we return an exchange map and an estimate in AED', 'Get an estimate'),
    cases=['cdek-b2b', 'unilin-crm', 'apartika-crm'],
    faq=[
        ('How much does Bitrix24 development cost?', 'AED 200 per hour with the estimate in AED fixed before start. Accounting integration from AED 10,000.'),
        ('Do we need a specific plan for an integration?', 'A cloud portal needs REST API access, which per the Bitrix24 documentation comes with Vibe+ plans, not Essentials.'),
        ('Do you work on a portal set up by another partner?', 'Yes. We review what has been done first and do not rebuild what works.'),
        ('Do you work with on-premise Bitrix24?', 'Yes, cloud and on-premise. Our cases include on-premise Bitrix24 at Unilin linked with 1C and ERP.'),
    ],
    form=('Let us discuss your Bitrix24 development', 'Tell us what needs to connect with what. We reply within a business day'),
    svc=('Bitrix24 development', 'Bitrix24 customisation, REST API integrations and apps for UAE companies', None)))

# ---------------------------------------------------------------- 10. Travel agency
la_page(dict(path='/bitrix-travel', slug='bitrix-travel', crumb='CRM for travel agencies',
    title='CRM for a travel agency in Dubai on Bitrix24 | MakeBiz',
    desc='CRM for travel agencies and tour operators in Dubai on Bitrix24: WhatsApp enquiries, options, bookings, payments, repeat trips. Setup from AED 10,000.',
    eyebrow='CRM · travel', h1='CRM for a <span>travel agency</span>',
    lead='Enquiries, options, bookings, payments and repeat trips in one system instead of personal phones',
    answer='MakeBiz Technologies sets up CRM for travel agencies and tour operators in Dubai on Bitrix24: enquiries from WhatsApp, the website and social media, options and quotes, supplier bookings, payments, pre-trip reminders and repeat sales. Standard setup from AED 10,000, WhatsApp AED 500, custom work AED 200 per hour. Prices as of ' + LA_DATE2 + '.',
    cta='Discuss a travel agency CRM', vis=V_CHAT,
    chips=[('from AED 10,000', 'setup'), ('AED 500', 'WhatsApp'), ('AED 200/hr', 'custom work'), ('Partner', 'Bitrix24')],
    alt='CRM for a travel agency',
    sections=[
        section('What we set up for a travel agency', '', cards([
            ('Enquiries in one pipeline', 'WhatsApp, website, calls and social media with source and owner'),
            ('Options and quote', 'Dates, travellers and budget in the record, a quote from a template'),
            ('Bookings and suppliers', 'Hotels, flights and transfers as a process with statuses'),
            ('Payments', 'Deposit and balance with due dates and reminders'),
            ('Before the trip', 'Documents, payment and departure date tracked in the record'),
            ('Repeat trips', 'Travel history and an offer for next season'),
        ], 3)),
        section('Where a travel agency loses sales', '', cards([
            ('A reply after an hour', 'The client asked three agencies and booked with the first to answer'),
            ('A quote in a chat', 'Options and prices are scattered across chats'),
            ('Payments without control', 'The balance date passed and the booking is at risk'),
            ('The client after the trip', 'Came back happy, booked the next trip elsewhere'),
        ], 2)),
        section('First reply and the right plan', '', la2_card('Night enquiries can go to an ' + LA('/ai-agents/rop', 'AI agent') + ' that clarifies dates, budget and travellers and hands over a ready enquiry; see our news on ' + LA('/news/ai-agent-v-whatsapp-vhodyashchie-zayavki', 'an AI agent on WhatsApp') + '. WhatsApp integration comes with the Basic plan, invoices, estimates and web forms from Standard (bitrix24.ae, checked ' + LA_DATE2 + '). A similar path from enquiry to booking, in property rental, is in the ' + LA('/keysy/apartika-crm', 'Apartico case')), tone='tint'),
        section('Example: an agency with 6 agents', '', la2_card('An illustration, not a case. 6 agents, enquiries mostly from WhatsApp. Setup AED 10,000, WhatsApp AED 500, and bookings and payments at, say, 20 hours, or AED 4,000: AED 14,500 one-off in total. Basic covers 5 users, so a team of 6 needs Standard for up to 50 users at AED 364 a month billed annually.')),
    ],
    table_title='What a travel agency CRM costs', table_sub='Our work and the licence',
    table=la2_tbl([LA2_SETUP, LA2_HOUR('Bookings, suppliers, payments'), LA2_WA, ('AI agent for enquiries', 'from AED 5,000', 'maintenance 10% a month'), LA2_SUP, LA2_LIC]),
    mid=('We will show a travel pipeline in a demo', 'Tell us your destinations, we show the CRM and the price', 'Book a demo'),
    cases=['apartika-crm', 'performia-crm', 'cdek-b2b'],
    faq=[
        ('Does Bitrix24 work for a travel agency?', 'Yes. Enquiries run in a pipeline, bookings and payments in their own processes.'),
        ('How much does a travel agency CRM cost in Dubai?', 'Standard setup from AED 10,000, WhatsApp AED 500, custom work AED 200 per hour after a survey. The Bitrix24 licence is separate, from AED 180 a month.'),
        ('Can clients get a reply at night?', 'Yes, an AI agent from AED 5,000 can reply first and clarify details, and agents get ready enquiries in the morning.'),
        ('Will you connect our booking systems?', 'If it has an API, we scope the exchange at AED 200 per hour. A cloud portal needs a plan with REST API access.'),
    ],
    form=('Let us discuss your travel agency CRM', 'Tell us your team size. We reply within a business day'),
    svc=('CRM for travel agencies', 'Bitrix24 implementation for travel agencies and tour operators in the UAE', 10000)))

# ---------------------------------------------------------------- 11. Event management
la_page(dict(path='/bitrix-events', slug='bitrix-events', crumb='CRM for event companies',
    title='CRM for an event management company in Dubai | MakeBiz',
    desc='CRM for event management companies in Dubai on Bitrix24: enquiries, budgets, venues and vendors, project tasks, payments in instalments. From AED 10,000.',
    eyebrow='CRM · events', h1='CRM for an <span>event management company</span>',
    lead='Enquiry, budget, venue and vendors, team tasks and payments for every event in one system',
    answer='MakeBiz Technologies sets up CRM for event management companies in Dubai on Bitrix24: event enquiries, budgets and proposals, venues and vendors, a project with tasks and deadlines for every event, payments in instalments and feedback afterwards. Standard setup from AED 10,000, custom work AED 200 per hour, WhatsApp AED 500. Prices as of ' + LA_DATE2 + '.',
    cta='Discuss an event CRM', vis=V_BOARD,
    chips=[('from AED 10,000', 'setup'), ('AED 200/hr', 'custom work'), ('Projects', 'and tasks'), ('Partner', 'Bitrix24')],
    alt='CRM for an event management company',
    sections=[
        section('What we set up for events', '', cards([
            ('Enquiries', 'Date, format, guests and budget from the first contact'),
            ('Budget and proposal', 'Lines from the catalogue, a proposal from a template'),
            ('Venues and vendors', 'A supplier base with terms and work history'),
            ('A project per event', 'Team tasks with deadlines, a checklist and owners'),
            ('Payments in instalments', 'Advance and balance by date, a debt reminder'),
            ('After the event', 'Feedback, closing documents, a repeat order'),
        ], 3)),
        section('Where an event company loses money', '', cards([
            ('A budget in a spreadsheet', 'A vendor raised the price, the client got the old version'),
            ('An enquiry without a reply', 'While the budget was prepared, the client chose a faster agency'),
            ('Tasks in chats', 'A week before the event nobody knows who books the equipment'),
            ('Margin not visible', 'What remains after vendors is counted by hand'),
        ], 2)),
        section('Projects, plan and analytics', '', la2_card('Each event works best as a separate project with tasks and owners, linked to the deal. On bitrix24.ae unlimited projects, invoices and estimates come from the Standard plan, task time tracking from Professional (checked ' + LA_DATE2 + '). Revenue and margin by event and client come together in ' + LA('/bi-analitika', 'BI analytics') + ' from AED 300 a month; see our news on ' + LA('/news/tri-dashborda-rukovoditelya-prodazh', 'three dashboards')), tone='tint'),
        section('Example: 10 events a month', '', la2_card('An illustration, not a case. About 10 corporate events a month, a team of 12. Setup AED 10,000, WhatsApp AED 500, and budgets and event projects at, say, 25 hours, or AED 5,000: AED 15,500 one-off in total. Standard for up to 50 users costs AED 364 a month billed annually. A similar flow of sales, handover and payments in instalments, in education, is in the ' + LA('/keysy/performia-crm', 'Performia case'))),
    ],
    table_title='What an event CRM costs', table_sub='Our work and the licence',
    table=la2_tbl([LA2_SETUP, LA2_HOUR('Budgets, vendors, event projects'), LA2_WA, LA2_BI, LA2_SUP, LA2_LIC]),
    mid=('We will map your event process in the CRM', 'Tell us what events you run, we show the map and the price', 'Get a map'),
    cases=['performia-crm', 'apartika-crm', 'cdek-b2b'],
    faq=[
        ('Does Bitrix24 work for an event management company?', 'Yes. Enquiries and budgets run in the pipeline, each event is a project with tasks.'),
        ('How much does an event CRM cost in Dubai?', 'Standard setup from AED 10,000, custom work AED 200 per hour after a survey, WhatsApp AED 500. The Bitrix24 licence is separate.'),
        ('Can we see margin per event?', 'Yes, income and vendor costs are tracked per event; BI analytics from AED 300 a month sums them up.'),
        ('Will there be payment reminders?', 'Yes, the advance and balance have due dates. An automation rule sets the task; bitrix24.ae lists sales automation from Professional.'),
    ],
    form=('Let us discuss your event CRM', 'Tell us what events you run. We reply within a business day'),
    svc=('CRM for event management companies', 'Bitrix24 implementation for event management companies in the UAE', 10000)))

# ---------------------------------------------------------------- 12. Marketing agency
la_page(dict(path='/bitrix-agency', slug='bitrix-agency', crumb='CRM for agencies',
    title='CRM for a marketing agency in Dubai on Bitrix24 | MakeBiz',
    desc='CRM for marketing and digital agencies in Dubai on Bitrix24: leads, proposals, retainers, projects and tasks, hours per client. Setup from AED 10,000.',
    eyebrow='CRM · agencies', h1='CRM for a <span>marketing agency</span>',
    lead='Leads, proposals, retainers and tasks in one system: which client brings money and which eats hours',
    answer='MakeBiz Technologies sets up CRM for marketing, digital and creative agencies in Dubai on Bitrix24: leads and proposals, monthly retainers as recurring deals, projects and tasks for each client, hours tracking and a profitability report. Standard setup from AED 10,000, custom work AED 200 per hour, BI analytics from AED 300 a month. Prices as of ' + LA_DATE2 + '.',
    cta='Discuss an agency CRM', vis=V_TICKETS,
    chips=[('from AED 10,000', 'setup'), ('AED 200/hr', 'custom work'), ('from AED 300/mo', 'BI analytics'), ('Partner', 'Bitrix24')],
    alt='CRM for a marketing agency',
    sections=[
        section('What we set up for an agency', '', cards([
            ('Leads and briefs', 'Website, WhatsApp and social media leads with the brief in the record'),
            ('Proposals', 'A proposal from a template right from the deal'),
            ('Retainers', 'Monthly contracts as recurring deals on a schedule'),
            ('Client projects', 'Team tasks for each client with deadlines'),
            ('Hours and budget', 'Hours spent on a client versus what they pay for'),
            ('Reports', 'Revenue, team workload and profit by client'),
        ], 3)),
        section('Where an agency loses money', '', cards([
            ('Hours not tracked', 'The client pays a fixed fee and nobody counts the hours'),
            ('A verbal renewal', 'The contract ended, no invoice went out, the work goes on for free'),
            ('Tasks in chats', 'Client edits arrive in five places and half get lost'),
            ('Leads without a reply', 'While the proposal was in progress, the client signed elsewhere'),
        ], 2)),
        section('The right Bitrix24 plan for an agency', '', la2_card('Recurring deals come with the Basic plan, unlimited projects, invoices and estimates from Standard, task time tracking from Professional (bitrix24.ae, checked ' + LA_DATE2 + '). So we pick the plan by how the agency earns: if clients pay for hours, you need Professional; for a fixed package Standard may be enough. Plan prices in AED: ' + LA('/bitrix-licenses', 'Bitrix24 licences') + '. Who sees client amounts is in our news on ' + LA('/news/prava-dostupa-v-crm-kto-chto-vidit', 'access rights')), tone='tint'),
        section('Example: an agency of 15 people', '', la2_card('An illustration, not a case. 15 staff, 12 clients on retainer. Setup AED 10,000 plus retainers, projects and hours tracking at, say, 20 hours, or AED 4,000: AED 14,000 one-off in total. Time tracking needs Professional for up to 100 users, AED 731 a month billed annually. BI analytics from AED 300 a month shows profit by client.')),
    ],
    table_title='What an agency CRM costs', table_sub='Our work and the licence',
    table=la2_tbl([LA2_SETUP, LA2_HOUR('Retainers, projects, hours tracking'), LA2_BI, LA2_WA, LA2_SUP, LA2_LIC]),
    mid=('We will show the profitability of your clients', 'Tell us how many retainer clients you have, we show the map and the price', 'Get a map'),
    cases=['performia-crm', 'cdek-b2b', 'unilin-crm'],
    faq=[
        ('Does Bitrix24 work for a marketing agency?', 'Yes. Leads and proposals run in a pipeline, retainers as recurring deals, client work in projects and tasks.'),
        ('How much does an agency CRM cost in Dubai?', 'Setup from AED 10,000, custom work AED 200 per hour, BI analytics from AED 300 a month, licence separate.'),
        ('Can we track hours per client?', 'Yes, with task time tracking, which per bitrix24.ae comes from the Professional plan.'),
        ('How do we not forget to invoice a retainer?', 'A recurring deal is created on schedule and appears as a new deal for the responsible manager.'),
    ],
    form=('Let us discuss your agency CRM', 'Tell us your team size. We reply within a business day'),
    svc=('CRM for marketing agencies', 'Bitrix24 implementation for marketing and digital agencies in the UAE', 10000)))

UPDATED, UPDATED_ISO = _LA_UPD
