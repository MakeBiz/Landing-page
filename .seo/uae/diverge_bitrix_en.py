#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
То же, что diverge_bitrix.py, но для английской версии страницы Битрикс24.

Английские страницы дубайского и российского сайтов тоже были близнецами,
поэтому разводим их теми же смыслами: дирхамы и VAT, WhatsApp, два языка,
часовой пояс и календарь ОАЭ, free zone против mainland.

    python3 .seo/uae/diverge_bitrix_en.py .
"""
import io, os, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
os.chdir(ROOT)
F = 'en/bitrix.html'

PAIRS = [
    ('Bitrix24 · implementation and support', 'Bitrix24 in the UAE · implementation and support', 2),
    ('Bitrix24 as <span style="color:#16C15A">a digital environment</span> for running your business',
     'Bitrix24 <span style="color:#16C15A">in Dubai and the UAE</span>, set up for how you work', 1),
    ('We implement Bitrix24 not as a program but as a working system: processes, communications, accounting, roles and analytics come together into a single managed workflow of the company',
     'We set Bitrix24 up the way it actually runs in the Emirates: dirhams and VAT on the deal card, WhatsApp as the first channel instead of a phone call, one portal in two languages and a calendar with local public holidays', 1),

    ('Unified workflow', 'Your workflow', 1),
    ("All of your company's work in one environment", 'Your whole UAE operation in one system', 1),
    ('Bitrix24 connects sales, tasks, documents, and communications. Data stops living in scattered places: one source of truth appears that management can rely on',
     'Bitrix24 brings sales, tasks, documents and correspondence into one place. For a company in the Emirates that also means currency, language and channels: amounts in dirhams, English and Russian in one portal, WhatsApp next to the client card', 1),
    ('The team works in a unified structure of tasks, stages and owners',
     'Tasks, stages and owners in one structure, with a calendar of UAE weekends and public holidays', 1),
    ('Clients, deals, and the entire interaction history in one place',
     'Clients, deals and the whole conversation in one place, amounts in dirhams, VAT on its own line', 1),
    ('Telephony and email', 'WhatsApp, telephony and email', 1),
    ('Calls and correspondence are automatically linked to cards',
     'WhatsApp threads, calls and emails attach themselves to the client card', 1),
    ('Everyone sees only what they should: permissions are structured to fit the company',
     'Permissions follow the group structure: free zone, mainland and branches each see only their own', 1),
    ('Reports and dashboards on sales and processes to support decisions',
     'Reports and dashboards on sales and processes, in dirhams and roubles at the same time', 1),
    ('The system moves deals forward, sets tasks, and sends reminders on its own',
     'The system moves deals forward, sets tasks and reminds people on Dubai time', 1),

    ('What is included in the standard CRM setup', 'What the starter portal setup includes', 1),
    ('The starter package prepares a working platform: the team immediately works in a single structured environment. More complex logic, integrations, and additional workflows are assessed after the pre-project assessment',
     'The starter package gives you a working portal: the team starts on day one. Currency, time zone and language are set for the UAE from the start, while complex logic, integrations and extra workflows are quoted after the pre-project assessment', 1),
    ('Company profile: details, currency, time zone', 'Company profile: details, dirhams, Dubai time zone', 1),
    ('Counterparty and contact fields', 'Counterparty fields: TRN, licence, registration zone', 1),
    ('Introductory team training', 'Introductory team training in English or Russian', 1),

    ('When you need more than the standard setup', 'When one setup is not enough', 1),
    ('Multiple divisions, complex internal logic, analytics requirements or cross-functional processes: implementation starts with a pre-project assessment',
     'Several entities in different zones, work across two markets at once, reporting requirements or processes that cross departments: a project like that starts with a pre-project assessment', 1),
    ('We study your current business logic', 'We work out how the company runs today', 1),
    ('We map out processes and interaction points', 'We map the processes and where departments hand over', 1),
    ('We define the future CRM architecture', 'We put together the architecture of the future portal', 1),
    ('We identify bottlenecks and weak spots', 'We show where the process tears and where money leaks', 1),

    ('Initial analysis of the situation and current processes', 'We look at what you have now and where time is lost', 1),
    ('We map out the workflow and the future architecture of the system',
     'We describe the workflow and the architecture of the future portal', 1),
    ('We implement process logic, roles and automation', 'We build the processes, roles and automation', 1),
    ('We hand over the working logic and train employees', 'We show the team how to work in it, in their own language', 1),
    ('Support after launch and development of the system', 'We stay on after launch and grow the system with you', 1),

    ('Transparent packages based on the number of hours per month. Used hours are recorded openly, an extra hour beyond the package costs 250 AED',
     'Clear packages by hours per month. Hours spent are visible to you, an hour beyond the package costs AED 250', 1),
    ('Adjustment of CRM entity settings', 'Changes to CRM entity settings', 1),
    ('Updating processes and automations', 'Updating processes and robots', 1),
    ('Email, telephony, messengers', 'Email, telephony, WhatsApp', 1),
    ('Consultations on Bitrix24 functionality', 'Advice on what Bitrix24 can do', 1),

    ('Full-cycle IT company', 'Full-cycle IT company in the UAE', 1),
    ('Implementation, analytics, automation and AI in one team',
     'Implementation, analytics, automation and AI agents in one team', 1),
    ('We work with company processes, not just with configuring buttons',
     'We work with the company processes, not just with checkboxes in the settings', 1),
    ('One team from launch to growth, with no handing tasks over',
     'One team from launch to growth, with nobody passing you along', 1),

    ('Whether you need a standard setup or a large project, leave a request: we will run a diagnostic and propose a solution built for your company',
     'Whether you need the starter setup or a large project, leave a request: we will go through your situation and propose a solution for your company in the UAE', 1),
    # второй проход: остатки, совпадавшие с makebiz.life
    ('CRM setup: modules and reference books', 'CRM modules and reference books for your profile', 1),
    ('User and permission administration', 'Managing users and access rights', 1),
    ('Editing roles, groups and access logic', 'Changes to roles, groups and access', 1),
    ('Setup of notifications and workflow logic', 'Notifications and how the portal behaves', 1),
    ('We prepare the scope of work, the estimate, and the roadmap', 'We put together the scope, an estimate in dirhams and a roadmap', 1),
]


def main():
    h = io.open(F, encoding='utf-8').read()
    before = h
    done = skipped = 0
    for old, new, n in PAIRS:
        if h.count(new) >= n:
            skipped += 1
            continue
        c = h.count(old)
        if c == 0:
            raise SystemExit('НЕ НАЙДЕНО и не заменено ранее: %s' % old[:70])
        if c != n:
            raise SystemExit('ожидалось %d вхождений, найдено %d: %s' % (n, c, old[:70]))
        h = h.replace(old, new)
        done += 1
    if h != before:
        io.open(F, 'w', encoding='utf-8').write(h)
    print('%s: заменено %d, уже было %d' % (F, done, skipped))


if __name__ == '__main__':
    main()
