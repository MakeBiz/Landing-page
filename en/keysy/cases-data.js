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
    title:'Apartico: property rental <b>across Russia in one CRM</b>',
    lead:'We brought rental of apartments, serviced apartments, dachas and houses into one system: over a thousand objects across the country, auto posting of listings to Avito, Cian and other portals, an AI agent that qualifies enquiries and helps with booking, and Vector speech analytics that watches politeness and empathy on calls.',
    client:'Apartico, property rental', region:'Russia', built:'CRM, AI agent, portal integrations, Vector, BI', term:'',
    was:'listings, portals and enquiries handled by hand and apart',
    now:'posting, enquiries, bookings and analytics in one CRM',
    metric:'',
    problem:'Apartico rents out apartments, serviced apartments, dachas and houses across Russia, with over a thousand objects. Listings have to be posted and kept current on many portals at once, enquiries pour in from Avito, Cian and other sites, from messengers and by phone, and then they have to be qualified, taken into booking, confirmed and followed up for feedback. While all of this was done by hand and in different places, listings and enquiries got lost, managers drowned in routine, and there was no single picture of objects, bookings and service quality.',
    solution:'We rolled out a CRM for property rental and tied it to the whole external loop. We set up automatic posting of listings to Avito, Cian and other portals and a reverse feed: every enquiry from portals, the website, messengers and telephony lands straight in the CRM linked to its object. First response and qualification were taken over by an AI agent: it replies instantly, clarifies dates, parameters and budget, suggests suitable objects and passes hot enquiries to a manager. Managers run everything in the CRM, and the agent helps at every step: booking, booking confirmation and feedback collection after check in. We connected BI dashboards so the team sees its metrics by object, portal, enquiry and booking. Separately we deployed Vector speech analytics: it processes operator and client calls and scores how friendly, polite and empathetic the staff are, to keep service at a high level. The solution works the same for every object type and across all regions of the country.',
    result:'Now the whole rental business lives in one CRM: listings are published to portals automatically, enquiries from every source are collected and qualified by the agent, bookings, confirmations and feedback are run in the system, and management sees the metrics by object and portal in dashboards. Vector shows how the team talks to clients and keeps politeness and empathy under control. The same process works for a city apartment and a house in the countryside, across the whole country.',
    soft:'CRM + auto posting to portals + AI agent + <b>Vector</b> and BI across all objects.',
    quote:null
  },

  {
    slug:'unilin-crm', ind:['proizvodstvo','prodazhi'], products:['crm','analytics'], date:'2026-07',
    title:'Unilin: Bitrix24 for field managers <b>and market analytics</b>',
    lead:'For a third year we develop and support Unilin: an on-premise Bitrix24 on their server, deeply customized for regional sales, field managers working from mobile, integrations with 1C and ERP, and BI analytics on the market, retail points, products and the company.',
    client:'Unilin, a flooring manufacturer', region:'Russia', built:'On-premise Bitrix24, mobile processes, 1C and ERP, BI', term:'',
    was:'field managers and regions outside a single system',
    now:'the whole region in CRM from a phone, analytics on every cut',
    metric:'',
    problem:'Unilin has a large network of regional and field managers who work on the road: retail points, dealers and partners across the country. Data on visits, points and sales was scattered across spreadsheets and local files, the boxed CRM out of the box did not cover their processes, and management had no single picture of the market, points and products. They needed a system where a manager on the road works as comfortably as from the office.',
    solution:'We deployed and deeply customized the on-premise Bitrix24 on the client server for their processes. We set up business processes and field manager work straight from the mobile app: visits to retail points, tasks, deals and reports from a phone in the field. We custom developed the boxed version for regional sales and have supported it for a third year. We built end to end integrations with 1C and ERP so that catalogue, shipments and data move between systems without manual transfer. We assembled BI dashboards with analytics across several cuts: market analytics, retail point analytics, product analytics and company wide analytics.',
    result:'Now field managers run regions and retail points straight from a phone, and the data lands in a single system at once. Management sees the market, points, products and the company in dashboards, the boxed Bitrix24 is customized to Unilin real processes, and the link with 1C and ERP keeps data in one loop. This is the third year of development and support.',
    soft:'On-premise Bitrix24, mobile field managers, 1C and ERP, <b>BI across 4 cuts</b>.',
    quote:null
  },

  {
    slug:'cdek-b2b', ind:['prodazhi','logistika','uslugi'], products:['crm','ai-agents','analytics'], date:'2026-07',
    title:'CDEK: corporate B2B on Bitrix24 <b>with agents and analytics</b>',
    lead:'For a second year we develop CDEK corporate direction in Russia and Kazakhstan: an on-premise Bitrix24 built to fit, integrations with internal systems, AI agents and BI dashboards for corporate clients.',
    client:'CDEK, logistics and delivery', region:'Russia and Kazakhstan', built:'On-premise Bitrix24, integrations, agents, BI', term:'',
    was:'corporate clients spread across systems and handled by hand',
    now:'management, support and analytics in one loop',
    metric:'',
    problem:'CDEK has a large corporate direction and branches in Russia and Kazakhstan, and work with B2B clients was spread across different systems and largely manual. The standard boxed CRM did not cover their processes, after hours requests and manager routine slowed client management down, and there was no unified analytics on corporate clients.',
    solution:'We deployed and heavily customized the on-premise Bitrix24 for corporate client work across branches in Russia and Kazakhstan: management, tracking, support and account management. We built end to end integrations with their internal CRM, internal systems and resources, telephony and messengers. We assembled a set of AI agents: one answers after hours, one qualifies leads, one parses incoming email, one assists managers, and one keeps tasks and deadlines moving. We connected BI dashboards with end to end analytics on corporate clients.',
    result:'Now the CDEK corporate team works in one loop: every client is managed, tracked and supported in one place, agents cover routine and after hours, and management sees corporate clients in dashboards. This is the second year of the partnership.',
    soft:'On-premise Bitrix24, integrations, <b>5 AI agents</b> and BI dashboards.',
    quote:null
  },


  {
    slug:'haval-vector', ind:['prodazhi','uslugi','logistika'], products:['analytics','ai-agents'], date:'2026-07',
    title:'HAVAL: Vector speech analytics <b>for a dealer network</b>',
    lead:'We analyze dealership sales calls across Russia: Vector checks over 300,000 minutes of conversation a month against 40+ criteria, escalates to a senior manager when quality drops below 70%, and rolls everything up into BI dashboards.',
    client:'HAVAL, a global carmaker', region:'Russia', built:'Vector, BI dashboards and AI agents', term:'',
    was:'hundreds of thousands of call minutes went unchecked',
    now:'40+ criteria on every call and escalation on risk',
    metric:'',
    problem:'HAVAL has a dealership network across Russia and a huge flow of sales calls, over 300,000 minutes of conversation a month even on a sample. Checking that volume by hand is impossible, spot checks covered a fraction of a percent, and off the shelf tools could not cope with such volumes and 40+ communication criteria. Script deviations and lost sales went unnoticed.',
    solution:'We built Vector speech analytics as a fully custom solution: it processes calls across the whole network and scores every conversation against 40+ criteria based on a checklist and scripts, handling over 300,000 minutes a month. AI agents flag weak calls: if a conversation drops below 70%, it is automatically escalated to a senior manager so the sale is not lost. We connected BI dashboards with deep analytics on how calls influence sales and tracking of deals after a call, NPS and feedback collection, and we give management ready summaries. The speech analytics, the agents and the dashboards are all custom development. On top of that, agents book customers into the service center, remind about scheduled maintenance and upsells, and act as account managers.',
    result:'Now HAVAL sees how the whole network talks to customers, at a scale beyond manual review or off the shelf tools. Weak calls are caught and escalated in time, script compliance is measurable, and the link between a call and a sale is visible in dashboards rather than guessed.',
    soft:'Vector + agents + BI: <b>40+ criteria</b>, auto escalation below 70%, dashboards.',
    quote:null
  },


  {
    slug:'pink-rabbit-agent', ind:'ecom', products:['ai-agents'], date:'2026-07',
    title:'Pink Rabbit: an AI agent that <b>advises with tact</b>',
    lead:'A tactful AI expert works around the clock: helps choose products without judgment, verifies age, guides the customer to purchase, acts as support and hands hot leads to managers.',
    client:'Pink Rabbit, a chain of adult stores', region:'Saint Petersburg and Russia', built:'a 24/7 AI agent', term:'',
    was:'night and sensitive questions waited for an operator',
    now:'a tactful reply in seconds, around the clock',
    metric:'',
    problem:'The topic is intimate, so people tend to ask in the evening and at night and want privacy and expert advice without judgment. The chain has dozens of stores and an online shop with delivery across Russia, the flow of repetitive questions about availability, discreet delivery, product choice and care is huge, and operators cannot answer everyone around the clock. Some enquiries and hot customers were lost outside working hours.',
    solution:'We trained the AI agent on the assortment, delivery rules and safety and care information, and set up tactful expert consultation in the role of a sexologist, without judgment and with privacy. The agent verifies age 18+, selects products by need, occasion and budget, including for couples and as gifts, answers questions about discreet delivery, payment, returns, materials and compatibility, and works on the site and in messengers around the clock. It qualifies and guides the customer to purchase, hands hot leads to managers, and escalates sensitive or complex cases to a human consultant. It collects feedback and NPS, cross-sells related items and reactivates dormant customers. Inside, it helps run deals in the CRM, enriches cards, segments the client base and runs mailings: back in stock, promotions and personal recommendations.',
    result:'Now a customer gets an instant, private and tactful expert answer at any time of day. Fewer questions go unanswered, operators are freed to handle only the complex ones, more enquiries reach a purchase, and the brand tone of strengthening the family stays consistent in every chat.',
    soft:'One agent: <b>consultant</b>, support, sales, 18+, NPS and mailings.',
    quote:null
  },


  {
    slug:'performia-crm', ind:['obrazovanie','uslugi'], products:['crm','analytics'], date:'2026-07',
    title:'Performia: sales, training, finance and <b>end to end analytics</b>',
    lead:'We brought the company entire cycle into one system: two sales lines, running training groups across all programs, account management and a finance block with installments, receivables and payables, plus electronic document flow and a BI dashboard with end to end analytics on sales, leads, products and customer behavior.',
    client:'Performia, training and recruitment', region:'Moscow', built:'Bitrix24, turnkey, plus a BI dashboard', term:'110 working days',
    was:'sales, courses and finance lived apart',
    now:'the whole cycle and end to end analytics in one window',
    metric:'',
    problem:'The company runs many training and recruitment programs, has five legal entities and settles in several currencies. Sales, course delivery, account management and finance were kept in different places and largely by hand, so it was hard to control payments and installments, launch training groups on time, and see the full picture of a client and the money.',
    solution:'We rolled out Bitrix24 for the whole cycle. We set up the base for five legal entities and four currencies, two sales lines with qualification and payment control, handoff to delivery and a training-group funnel with attendance and surveys across all their programs and consulting. We added account management and upsell, finance smart-processes (installments, receivables and payables), electronic document flow, and 20 document templates for the finance team. We built a BI dashboard with end to end analytics: every metric in one window, by product, sales, leads and customer behavior, with charts for management. We trained the team by role and supported the launch for a month.',
    result:'Now the whole path from enquiry to a graduated group and closed payments lives in one system. Payments, installments and debts are under control, training groups launch by checklist, and the manager sees the client, sales, leads and money in a BI dashboard rather than scattered spreadsheets.',
    soft:'Sales, group delivery, finance, documents and <b>end to end analytics</b> in one loop.',
    quote:null
  },
];
