/* =====================================================================
   MakeBiz. CASE LIST (English version, /en). This is the only file you edit
   when adding a case in English. Everything else picks it up automatically:
   the Cases tab, the block under a product, and the individual case page.

   Rules are the same as the Russian file (keysy/cases-data.js):
   - No long dashes anywhere. Commas, colons and periods only.
   - slug is the case address in latin letters, unique per case.
   - ind is the industry key (one of eight, see the Russian file).
   - products is an ARRAY of direction keys: ai-agents, crm, analytics, itdev.
   - Keep the slug identical to the Russian case so the language switch lands
     on the same case in the other language.
   ===================================================================== */

window.MB_CASES = [

  {
    slug:'haval-vector', ind:['prodazhi','uslugi','logistika'], products:['analytics','ai-agents','itdev'], date:'2026-07',
    title:'HAVAL: Vector speech analytics <b>for a dealer network</b>',
    lead:'We analyze dealership sales calls across Russia: Vector checks over 300,000 minutes of conversation a month against 40+ criteria, escalates to a senior manager when quality drops below 70%, and rolls everything up into BI dashboards.',
    client:'HAVAL, a global carmaker', region:'Russia', built:'Vector, BI dashboards and AI agents', term:'',
    was:'hundreds of thousands of call minutes went unchecked',
    now:'40+ criteria on every call and escalation on risk',
    metric:'300 000+',
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


  /* --- SAMPLES. Delete these once you add your real cases. --- */

  {
    slug:'diler-pod-klyuch', ind:'prodazhi', products:['crm','ai-agents','analytics'], date:'2026-07',
    title:'A car dealership, end to end: <b>CRM, agent and analytics</b>',
    lead:'We brought a car dealership sales into one system: a CRM for leads, an AI agent for first contact and end to end analytics for the manager.',
    client:'Car dealership', region:'Dubai, UAE', built:'CRM, agent, analytics', term:'6 weeks',
    was:'leads, calls and ads lived apart',
    now:'one system from enquiry to report',
    metric:'',
    problem:'Leads came in from ads, calls and messengers but never met in one place. Managers lost enquiries, and the owner could not tell which advertising paid off, so budget decisions were made blind.',
    solution:'We delivered three things together: a CRM on Bitrix24 for every lead, an AI agent for instant replies to first contact, and end to end Vector analytics that ties ads, leads and sales together. We rolled it out in stages over six weeks.',
    result:'Now every enquiry lands in the CRM, the agent answers at once, and the owner sees in a single report which channel brings deals. Sales became manageable, and advertising decisions are based on data.',
    soft:'Three directions working together: <b>CRM</b>, <b>agent</b> and <b>analytics</b>.',
    quote:{ text:'It used to be three separate worlds. Now it is one system and I see the whole picture.', who:'Director', org:'Car dealership, Dubai' }
  },

  {
    slug:'ai-agent-logistika', ind:'logistika', products:['ai-agents'], date:'2026-07',
    title:'An AI agent in Telegram <b>that never sleeps</b>',
    lead:'The night time gap in sales is closed: the agent replies in seconds at any hour, clarifies the order and creates a deal in the CRM without a manager.',
    client:'Logistics, B2B', region:'Dubai, UAE', built:'a 24/7 agent', term:'3 weeks',
    was:'up to a third of night enquiries were lost',
    now:'zero losses, a reply in 4 seconds',
    metric:'1 396',
    problem:'The company gets enquiries in Telegram around the clock, but managers are only available during the day. At night and on weekends messages piled up unanswered, and in logistics a client who does not get a quick reply moves on to the next carrier. Some enquiries were lost before the first conversation.',
    solution:'We trained the AI agent on the company real knowledge base: rates, delivery zones, common questions and scenarios. The agent is built into Telegram and the CRM, replies to the client itself, clarifies the order and creates a deal, and brings in a manager only for a hot conversation. Rollout took three weeks.',
    result:'The client gets a reply in seconds at any time of day, and in the morning managers work with ready deals instead of a pile of chats. In the first quarter <span class="hl">about 1 400 deals</span> went through the agent, and night enquiries stopped getting lost.',
    soft:'In the first quarter: <b>about 1 400</b> deals through the agent, a reply in <b>4 seconds</b>.',
    quote:{ text:'The agent closed the night time gap in sales. Managers now work only with warm clients.', who:'Head of sales', org:'Logistics company, Dubai' }
  },

  {
    slug:'bitrix-nedvizhimost', ind:'nedvizhimost', products:['crm'], date:'2026-06',
    title:'A pipeline and reminders <b>for a real estate agency</b>',
    lead:'Every lead is carried through to a viewing and a deal: the system never lets a client be forgotten.',
    client:'Real estate agency', region:'Dubai', built:'CRM and auto tasks', term:'3 weeks',
    was:'viewings and calls slipped through',
    now:'every lead is carried to a deal',
    metric:'',
    problem:'There were plenty of leads, but agents forgot to call back, viewings fell through, and long deals dropped off the radar. Everything relied on memory and notes.',
    solution:'We set up a Bitrix24 pipeline for the real estate deal cycle: automatic reminders for calls and viewings, tasks at every stage, and control over long deals.',
    result:'An agent handles more clients and loses no one: the system reminds them of the next step. Long deals no longer fall between stages.',
    soft:'Reminders at <b>every stage</b>, control over <b>long deals</b>.',
    quote:null
  },

  {
    slug:'vector-analitika', ind:'prodazhi', products:['analytics'], date:'2026-06',
    title:'End to end analytics <b>across every channel</b>',
    lead:'The company sees the whole path from click to payment and understands which advertising actually brings money.',
    client:'Service business', region:'UAE', built:'Vector, end to end analytics', term:'3 weeks',
    was:'could not see where deals came from',
    now:'see the whole path from click to payment',
    metric:'',
    problem:'Money went into advertising, but leads and payments could not be tied to a source. Budget decisions were made blind.',
    solution:'We connected Vector: data from ads, the website and the CRM came together in one report. You can see which channel brings leads and, most importantly, payments, not just clicks.',
    result:'The manager sees the full client journey and shifts budget into the channels that drive revenue. Reports build themselves, with no manual exports.',
    soft:'The client journey <b>in full</b>, reports <b>with no manual exports</b>.',
    quote:null
  }

];
