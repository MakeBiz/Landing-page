/* =====================================================================
   MakeBiz. CASE LIST (English version, /en). This is the only file you edit
   when adding a case in English. Everything else picks it up automatically:
   the Cases tab, the block under a product, and the individual case page.

   Rules are the same as the Russian file (keysy/cases-data.js):
   - No long dashes anywhere. Commas, colons and periods only.
   - slug is the case address in latin letters, unique per case.
   - ind is the industry key (one of eight, see the Russian file).
   - products is an ARRAY of direction keys: ai-agents, crm, analytics.
   - Keep the slug identical to the Russian case so the language switch lands
     on the same case in the other language.
   ===================================================================== */

window.MB_CASES = [

  {
    slug:'apartika-crm', ind:['nedvizhimost','uslugi'], products:['crm','ai-agents','analytics'], date:'2026-07',
    title:'Apartico: a thousand rental objects <b>in one CRM</b>',
    lead:'Rental of apartments, serviced apartments, dachas and houses now runs in one system: over a thousand objects, listings posted to Avito, Cian and other portals on their own, an AI agent sorting enquiries and helping with bookings, and Vector listening in on calls for politeness.',
    client:'Apartico, property rental', region:'Russia', built:'CRM, AI agent, portal integrations, Vector, BI', term:'',
    was:'listings and enquiries lived in different places, by hand',
    now:'posting, enquiries, bookings and numbers in one system',
    metric:'',
    problem:'Apartico has over a thousand objects across Russia: apartments, serviced apartments, dachas and houses. Every listing has to go out to several portals at once and stay current, while enquiries pour in from Avito, Cian, messengers and the phone, and each one has to be qualified, turned into a booking, confirmed and followed up for feedback. As long as that lived in different places and ran on manual work, listings and enquiries slipped through, managers sat in routine, and nobody had a single picture of objects, bookings and service quality.',
    solution:'We put in a rental CRM and wired it to the whole external loop. Listings go out to Avito, Cian and other portals on their own, and every enquiry from portals, the website, messengers and telephony comes back into the CRM already linked to its object. An AI agent took over the first reply and the qualification: it answers instantly, checks dates, parameters and budget, suggests matching options and hands hot enquiries to a manager. The manager runs everything in the CRM while the agent steps in at every point: the booking, the confirmation, the feedback after check in. On top sit BI dashboards by object, portal, enquiry and booking. Vector speech analytics went in separately: it goes through operator conversations with clients and scores how friendly, polite and empathetic the person was. The same scheme works for a city apartment and for a house out of town, in any region.',
    result:'The rental business now sits entirely in one CRM: listings publish themselves, enquiries from every source are collected and go through the agent, bookings, confirmations and feedback are run in the system, and management looks at objects and portals in dashboards. Vector shows how the team speaks to clients and keeps politeness in check. One and the same process runs across the country, on any type of object.',
    soft:'CRM, auto posting of listings, an AI agent, <b>Vector</b> and BI across all objects.',
    quote:null
  },

  {
    slug:'unilin-crm', ind:['proizvodstvo','prodazhi'], products:['crm','analytics'], date:'2026-07',
    title:'Unilin: on-premise Bitrix24 in the field <b>and market analytics</b>',
    lead:'Third year on Unilin: an on-premise Bitrix24 on their own server, reworked for regional sales, managers working from a phone in the field, wired into 1C and ERP, with BI on the market, retail points, products and the company.',
    client:'Unilin, a flooring manufacturer', region:'Russia', built:'On-premise Bitrix24, mobile processes, 1C and ERP, BI', term:'',
    was:'field teams and regions outside any shared system',
    now:'a region run from a phone, analytics across four cuts',
    metric:'',
    problem:'The Unilin network of regional and field managers works on the road: retail points, dealers and partners across the country. Visits, points and sales settled into spreadsheets and local files, an out of the box CRM did not close their processes, and management never got a picture of the market, the points and the products. They needed a system where somebody on the road works no worse than from the office.',
    solution:'We deployed the on-premise Bitrix24 on the client server and reworked it deeply for their processes. Business processes and field manager work were set up straight from mobile: visits to retail points, tasks, deals and reports from a phone out in the field. The boxed version was custom built for regional sales and we have supported it for a third year. End to end integrations with 1C and ERP move catalogue, shipments and data between systems with no manual transfer. BI dashboards cover four cuts: the market, retail points, products and the company as a whole.',
    result:'Field managers run regions and retail points from a phone, and the data lands in the shared system straight away. Management looks at the market, points, products and the company in dashboards, the boxed Bitrix24 fits the real Unilin processes, and the link with 1C and ERP keeps data in one loop. This is the third year of development and support.',
    soft:'On-premise Bitrix24, field work from a phone, 1C and ERP, <b>BI across 4 cuts</b>.',
    quote:null
  },

  {
    slug:'cdek-b2b', ind:['prodazhi','logistika','uslugi'], products:['crm','ai-agents','analytics'], date:'2026-07',
    title:'CDEK: the B2B arm on Bitrix24 <b>with agents and dashboards</b>',
    lead:'Second year on the CDEK corporate arm in Russia and Kazakhstan: an on-premise Bitrix24 built to fit, wired into their internal systems, AI agents and BI dashboards for corporate clients.',
    client:'CDEK, logistics and delivery', region:'Russia and Kazakhstan', built:'On-premise Bitrix24, integrations, agents, BI', term:'',
    was:'corporate clients spread over systems and worked by hand',
    now:'management, support and numbers in one loop',
    metric:'',
    problem:'The CDEK corporate arm is large, with branches in Russia and Kazakhstan, and work with B2B clients was smeared across different systems and largely done by hand. A standard boxed CRM did not close the processes, after hours requests hung unanswered, managers drowned in routine, and unified analytics on corporate clients did not exist at all.',
    solution:'We put in the on-premise Bitrix24 and reworked it heavily for corporate client work across the branches in Russia and Kazakhstan: management, tracking, support and account management. End to end integrations tie it to their internal CRM, internal systems, telephony and messengers. A set of AI agents went in: the first answers after hours, the second qualifies leads, the third parses incoming email, the fourth assists managers, the fifth keeps tasks and deadlines moving. BI dashboards give end to end analytics on corporate clients.',
    result:'The CDEK corporate team works in one loop: a client is managed, tracked and supported in one place, agents cover the routine and the night requests, and management sees corporate clients in dashboards. This is the second year of the partnership.',
    soft:'On-premise Bitrix24, integrations, <b>five AI agents</b> and BI dashboards.',
    quote:null
  },


  {
    slug:'haval-vector', ind:['prodazhi','uslugi','logistika'], products:['analytics','ai-agents'], date:'2026-07',
    title:'HAVAL: Vector listens to <b>the whole dealer network</b>',
    lead:'Dealership sales calls across Russia go through Vector: over 300,000 minutes a month, 40+ criteria per conversation, anything under 70% pulled up to a senior manager, and the whole picture in BI dashboards.',
    client:'HAVAL, a global carmaker', region:'Russia', built:'Vector, BI dashboards and AI agents', term:'',
    was:'hundreds of thousands of call minutes with nothing to check them',
    now:'every call against 40+ criteria, the weak ones pushed up',
    metric:'',
    problem:'The HAVAL dealership network across Russia produces a huge flow of sales calls: over 300,000 minutes of conversation a month even on a sample. That volume cannot be checked by hand, spot checks reached a fraction of a percent, and off the shelf tools handled neither the volume nor 40+ communication criteria. Script deviations and lost sales went unnoticed.',
    solution:'Vector speech analytics was built as fully custom development: it goes through calls across the whole network and scores every conversation against 40+ criteria drawn from a checklist and the scripts, handling over 300,000 minutes a month. AI agents flag the weak calls: a conversation under 70% is pushed to a senior manager automatically so the sale is not lost. BI dashboards cover how calls influence sales, track deals after a call, collect NPS and feedback, and management gets ready summaries. The analytics, the agents and the dashboards are all custom work. On top of that the agents book customers into the service centre, remind them about scheduled maintenance and upsells, and act as account managers.',
    result:'HAVAL sees how the whole network speaks to customers, at a scale neither manual review nor off the shelf tools can take. Weak calls are caught and pushed up in time, script compliance is measurable, and the link between a call and a sale shows up in dashboards instead of being guessed.',
    soft:'Vector, agents and BI: <b>40+ criteria</b>, auto escalation under 70%, dashboards.',
    quote:null
  },


  {
    slug:'performia-crm', ind:['obrazovanie','uslugi'], products:['crm','analytics'], date:'2026-07',
    title:'Performia: from enquiry to graduating a group <b>in one system</b>',
    lead:'The whole company cycle now sits in one system: two sales lines, training groups run across every program, account management and a finance block with installments, receivables and payables, electronic document flow, and a BI dashboard over sales, leads, products and customer behaviour.',
    client:'Performia, training and recruitment', region:'Moscow', built:'Bitrix24, turnkey, plus a BI dashboard', term:'110 working days',
    was:'sales, courses and money were counted apart',
    now:'the entire cycle and end to end analytics in one window',
    metric:'',
    problem:'The company runs a lot of training and recruitment programmes, holds five legal entities and settles in several currencies. Sales, course delivery, account management and finance lived in different places and largely ran on manual work, so payments and installments were hard to control, training groups launched late, and the full picture of a client and the money never came together.',
    solution:'We rolled Bitrix24 out across the whole cycle. The base was set up for five legal entities and four currencies, with two sales lines carrying qualification and payment control, a handoff into delivery and a training-group funnel with attendance and surveys across every programme and consulting. We added account management and upsell, finance smart-processes (installments, receivables and payables), electronic document flow and 20 document templates for the finance team. A BI dashboard brings the metrics into one window by product, sales, leads and customer behaviour, with charts for management. We trained the team by role and stayed with the launch for a month.',
    result:'The path from enquiry to a graduated group and closed payments lives in one system. Payments, installments and debts are under control, training groups launch by checklist, and the manager sees the client, sales, leads and money in a BI dashboard instead of scattered spreadsheets.',
    soft:'Sales, group delivery, finance, documents and <b>end to end analytics</b> in one system.',
    quote:null
  },
];
