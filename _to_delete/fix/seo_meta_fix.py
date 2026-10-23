# SEO: title до 70 и description до 165 знаков на новых страницах (одинаково на Маке и в облаке)
import sys, os
D = sys.argv[1]
def R(f, pairs):
    p = os.path.join(D, f); s = open(p, encoding='utf-8').read()
    for a, b in pairs:
        assert s.count(a) == 1, (f, a[:70], s.count(a)); s = s.replace(a, b)
    open(p, 'w', encoding='utf-8').write(s)
R('build_en_ae.py', [
 ("'Turnkey Bitrix24 implementation in Dubai and the UAE: CRM, pipelines, WhatsApp, 5% VAT, accounting integrations, training. Standard setup from AED 10,000, launch from 14 days.'",
  "'Turnkey Bitrix24 implementation in Dubai and the UAE: CRM, pipelines, WhatsApp, 5% VAT, accounting integrations. Setup from AED 10,000, launch from 14 days.'"),
 ("f'Bitrix24 prices in the UAE: cloud from {lic(49)} a month, Enterprise from {lic(399)}, on-premise from {lic(3590)} a year. bitrix24.ae prices in AED and USD, plan selection and renewal.'",
  "f'Bitrix24 prices in the UAE: cloud from {lic(49)} a month, Enterprise from {lic(399)}, on-premise from {lic(3590)} a year. bitrix24.ae prices in AED and USD.'"),
 ("'On-premise Bitrix24 in the UAE: implementation on your server | MakeBiz'", "'On-premise Bitrix24 in the UAE: setup on your server | MakeBiz'"),
 ("f'On-premise Bitrix24 on a company server in the UAE: edition selection, installation, cloud migration, customization, integrations and support. License from {lic(3590)} a year.'",
  "f'On-premise Bitrix24 on your server in the UAE: edition choice, installation, cloud migration, customization and support. License from {lic(3590)} a year.'"),
 ("title='Liaison AI agent: contacts, reminders and client relationships | MakeBiz',", "title='Liaison AI agent: contacts, reminders, relationships | MakeBiz',"),
 ("title='AI speech analytics for calls: conversation and script scoring | MakeBiz',", "title='AI speech analytics: every sales call scored | MakeBiz',"),
 ("title='AI marketing agent: content and visibility in search and ChatGPT | MakeBiz',", "title='AI marketing agent: content and visibility in ChatGPT | MakeBiz',"),
 ("page('/ai-agents', 'ai-agents', 'AI agents for business in Dubai and the UAE: sales, calls, HR | MakeBiz',", "page('/ai-agents', 'ai-agents', 'AI agents for business in Dubai and the UAE | MakeBiz',"),
 ("'AI agents for business in Dubai and the UAE: sales head on WhatsApp, liaison, call speech analytics, HR, procurement, marketing and finance in Bitrix24. One agent from AED 5,000.',",
  "'AI agents for business in Dubai and the UAE: sales head on WhatsApp, call analytics, HR, procurement, marketing and finance in Bitrix24. From AED 5,000.',"),
 ("tt + ' | MakeBiz' if len(tt) <= 62 else tt", "tt + ' | MakeBiz' if len(tt) <= 60 else tt"),
 ("f'MakeBiz prices in AED as of {PRICE_DATE}: Bitrix24 CRM setup from AED 10,000, support from AED 1,250 a month, AED 200 an hour, AI agent from AED 5,000, licenses from {lic(49)}.'",
  "f'MakeBiz prices in AED: Bitrix24 CRM setup from AED 10,000, support from AED 1,250 a month, AED 200 an hour, AI agent from AED 5,000, licenses from {lic(49)}.'"),
 ("f'MakeBiz Technologies contacts in the UAE: WhatsApp and phone {PHONE}, Telegram @{TG}, email {EMAIL}. Bitrix24 and AI agent implementation in Dubai.'",
  "f'MakeBiz Technologies contacts in Dubai: WhatsApp and phone {PHONE}, Telegram @{TG}, email {EMAIL}. Bitrix24 and AI agents.'"),
])
R('build_ae.py', [
 ("title='ИИ-агент Связной: контакты, напоминания и отношения с клиентами | MakeBiz',", "title='ИИ-агент Связной: контакты и отношения с клиентами | MakeBiz',"),
 ("(lambda tt: tt + ' | MakeBiz' if len(tt) <= 62 else tt)", "(lambda tt: tt + ' | MakeBiz' if len(tt) <= 60 else tt)"),
 ("f'Контакты MakeBiz Technologies в ОАЭ: WhatsApp и телефон {PHONE}, Telegram @{TG}, почта {EMAIL}. Внедрение Битрикс24 и ИИ-агентов в Дубае.'",
  "f'Контакты MakeBiz Technologies в Дубае: WhatsApp и телефон {PHONE}, Telegram @{TG}, почта {EMAIL}. Битрикс24 и ИИ-агенты.'"),
])
print('ok')
R('build_ae.py', [
 ("desc='HR-агент: отклики с job-площадок и сайта, первое собеседование в Telegram или WhatsApp, оценка кандидатов, типажи мотивации, резерв и воронка от отклика до выхода на работу.',",
  "desc='HR-агент: отклики с job-площадок и сайта, первое собеседование ботом в Telegram или WhatsApp, оценка кандидатов, резерв и воронка до выхода на работу.',"),
 ("desc='ИИ-агент маркетинга: план тем по реальным вопросам клиентов, статьи и новости на английском и русском, публикация на сайте, GEO-видимость в ChatGPT, Claude и Perplexity, дашборды.',",
  "desc='ИИ-маркетолог: темы по вопросам клиентов, статьи и новости на английском и русском, публикация на сайте, видимость в ChatGPT, Claude и Perplexity.',"),
])
R('build_en_ae.py', [
 ("desc='The liaison AI agent watches all contacts: who is waiting for a reply, who to get in touch with, who is hot and who is cooling down. Network map and warmth of each contact.',",
  "desc='The liaison AI agent watches all contacts: who is waiting for a reply, who to get in touch with, who is hot and who is cooling down.',"),
 ("desc='HR agent: responses from job boards and your site, the first interview in a Telegram or WhatsApp bot, candidate scoring, motivation types, talent pool and a funnel from response to first day.',",
  "desc='HR agent: responses from job boards and your site, a first interview by bot in Telegram or WhatsApp, candidate scoring and a funnel to the first day.',"),
 ("desc='AI marketing agent: a content plan from real customer questions, articles and news in English and Russian, publishing, GEO visibility in ChatGPT, Claude and Perplexity, dashboards.',",
  "desc='AI marketing agent: topics from customer questions, articles and news in English and Russian, publishing and visibility in ChatGPT, Claude and Perplexity.',"),
])
print('ok2')
