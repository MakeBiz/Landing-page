# /local-llm and /en/local-llm: local LLM server (calculator, buy or rent, partners).
# Runs inside build_ae.py and build_en_ae.py via exec with LLM_PY = 'ru' | 'en' and uses their helpers
# (hero, section, faq, form_block, page, VIS, esc, U, built). Numbers come from llm/figures.mjs, the same engine as the calculator.
# Prices: .seo/v2/llm/engine.js (CFG). Partners: LLM_PARTNERS below. Spec: TZ of 20.11.2026
import json as _json, subprocess as _sp, os as _os
_LD = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'llm')  # __file__ is the builder in .seo/v2
LF = _json.loads(_sp.run(['node', _os.path.join(_LD, 'figures.mjs'), LLM_PY], capture_output=True, text=True, check=True).stdout)
_EN = LLM_PY == 'en'
_UPD, _UPD_ISO = UPDATED, UPDATED_ISO
UPDATED, UPDATED_ISO = ('November 20, 2026' if _EN else '20 ноября 2026'), '2026-11-20'

# partners for rent: only from the partner master file and allowed for Dubai (no Aeza, no providers with a Russian-language site).
# Hostman: add when GPU plans are confirmed. Vast.ai and other GPU marketplaces: when Anton gives a referral link
LLM_PARTNERS = [
    ('ishosting', 'is*hosting', 'https://ishosting.io/affiliate/NzI2MSM2', ('Dedicated and GPU servers', 'Выделенные и GPU-серверы')),
    ('datapacket', 'DataPacket', 'https://portal.datapacket.net/aff.php?aff=189', ('Dedicated servers, GPU servers on request', 'Выделенные серверы, GPU-серверы под заказ')),
]
SC_URL = 'https://servercalc.com/?utm_source=makebiz&utm_medium=site&utm_campaign=local-llm'

def _t(en, ru): return en if _EN else ru
def _pc(x): return f'{x:g}' if _EN else f'{x:g}'.replace('.', ',')
P = {p['id']: p for p in LF['packs']}
C, G = LF['cases'], LF['cfg']
MMIN = min(p['m'][0] for p in LF['packs'] if p['m']); MMAX = max(p['m'][1] for p in LF['packs'] if p['m'])
def _mo(m): return f'{m[0]}-{m[1]} ' + _t('months', 'мес.')

# ---------- hero
_vis = VIS('license', _t('Local LLM · your server', 'Локальная LLM · ваш сервер'), _t('Online <b>✓</b>', 'Онлайн <b>✓</b>'),
    '<div class="tiers">' + ''.join(f'<div class="tier"><span><b>{esc(p["n"])}</b><small>{esc(p["w"])}</small></span><span class="us">{esc(p["from"])}</span></div>' for p in LF['packs']) + '</div>',
    (_t('Data', 'Данные'), _t('stays inside', 'внутри компании')), (_t('Per-seat fees', 'Подписки'), _t('not needed', 'не нужны'))
    ).replace(_t('>demo data<', '>демо-данные<'), '>' + _t('prices as of ', 'цены на ') + esc(G['priceDate']) + '<')
llm_body = hero(_t('Local LLM server', 'Локальная нейросеть'), _t('Your own ChatGPT <span>on your server</span>', 'Свой ChatGPT <span>на вашем сервере</span>'),
    _t('Works like ChatGPT, but company data never leaves the company and you do not pay a subscription for every employee',
       'Работает как ChatGPT, но данные не покидают компанию, а подписки на каждого сотрудника не нужны'),
    _t(f'MakeBiz Technologies installs open-weight large language models on a company server in the UAE: an AI chat for staff, a knowledge base on your documents, assistants for sales, calls and documents. '
       f'A turnkey server with installation starts {P["start"]["from"]}, for a company of up to 100 people it is about {P["biz"]["short"]}. You can also rent a GPU server from a partner, and we install the AI on it.',
       f'MakeBiz Technologies ставит открытые языковые модели на сервер компании в ОАЭ: AI-чат для сотрудников, базу знаний по вашим документам, помощников для продаж, звонков и документов. '
       f'Сервер под ключ с установкой стоит {P["start"]["from"]}, для компании до 100 человек около {P["biz"]["short"]}. Можно арендовать GPU-сервер у партнёра, а ИИ на него установим мы.'),
    ('#calc', _t('Calculate my server', 'Рассчитать сервер')), ('#form', _t('Talk to us', 'Обсудить задачу')), _vis,
    [(P['start']['from'], _t('server with installation', 'сервер с установкой')), (f'{MMIN}-{MMAX}', _t('months payback in packages', 'месяцев окупаемость пакетов')),
     ('10', _t('AI tasks to choose from', 'задач для ИИ на выбор')), (_t('Buy or rent', 'Купить или арендовать'), _t('your choice', 'на ваш выбор'))],
    _t('Local LLM server', 'Локальная нейросеть на сервере'))
_th = [(_t('Data stays inside', 'Данные внутри'), _t('Documents and chats are processed on your server, which helps meet UAE PDPL and EU GDPR data requirements',
                                                  'Документы и переписка обрабатываются на вашем сервере, это помогает выполнить требования к данным PDPL в ОАЭ и GDPR в ЕС')),
       (_t('Nothing leaves with an employee', 'Сотрудник ничего не унесёт'), _t('Chats, contracts and prompts stay in the company system, not in personal ChatGPT accounts',
                                                  'Переписка, договоры и запросы остаются в системе компании, а не в личных аккаунтах ChatGPT')),
       (_t('One purchase instead of subscriptions', 'Одна покупка вместо подписок'), _t('You pay for the server and setup once, there is no fee for every seat',
                                                  'Платите за сервер и настройку один раз, без оплаты за каждое рабочее место'))]
llm_body = llm_body.replace('</section>', '<div class="wrap llm-thesis">' + ''.join(f'<div class="gl"><b>{esc(a)}</b><span>{esc(b)}</span></div>' for a, b in _th) + '</div></section>', 1)

# ---------- calculator (static packs for crawlers and without JS, the script replaces them)
def _pk_static(p, on):
    tag = f'<span class="llm-tag">{esc(p["tag"])}</span>' if p['tag'] else ''
    li = ''.join(f'<li>{esc(x)}</li>' for x in p['inc'])
    return f'<div class="llm-pk{" on" if on else ""}">{tag}<b>{esc(p["n"])}</b><small>{esc(p["w"])}</small><span class="llm-pr">{esc(p["range"])}</span><ul>{li}</ul></div>'
_b = P['biz']
_right = (f'<div class="llm-res-l">{esc(_t("Package", "Пакет"))} «{esc(_b["n"])}»</div><div class="llm-res-p">{esc(_b["range"])}</div><div class="llm-res-c">{esc(_b["title"])}</div>'
          f'<div class="llm-pb"><div class="llm-pb-h">{_t("Payback", "Окупаемость")}</div><div class="llm-pb-big">{_t("Pays back in", "Окупится за")} {_mo(_b["m"])}</div></div>'
          f'<a class="btn btn-wide" href="#form" data-lead="buy" style="margin-top:18px">{_t("Get exact quote", "Получить точный расчёт")}</a>')
llm_calc = (f'<div class="llm-mode" id="llmMode" role="tablist" aria-label="{_t("Calculator mode", "Режим калькулятора")}"><button type="button" role="tab" data-mode="custom">{_t("Build my own", "Собрать под себя")}</button>'
            f'<button type="button" role="tab" data-mode="packs" class="on">{_t("Ready packages", "Готовые пакеты")}</button></div>'
            f'<div class="llm-calc"><div class="llm-left gl" id="c2Left"><div class="llm-static"><div class="llm-packs">{"".join(_pk_static(p, p["id"] == "biz") for p in LF["packs"])}</div>'
            f'<p class="llm-note" style="margin-top:14px">{_t("Prices include the server, assembly, installation and setup of the package tasks.", "В цене сервер, сборка, установка и настройка задач пакета.")}</p></div></div>'
            f'<aside class="llm-right gl" id="c2Right" aria-live="polite">{_right}</aside></div><div class="llm-bar" id="c2Bar"></div>')
llm_body += section(_t('Server <span>calculator</span>', 'Калькулятор <span>сервера</span>'),
    _t('Pick tasks and team size: the price and payback change right away. Or start from a ready package',
       'Выберите задачи и размер команды: цена и окупаемость меняются сразу. Или начните с готового пакета'), llm_calc, id_='calc')

# ---------- buy or rent
_rent_li = ''.join(f'<div class="llm-partner"><div><b>{esc(n)}</b><span>{esc(d[0] if _EN else d[1])}</span></div>'
                   f'<a href="{esc(u)}" target="_blank" rel="sponsored nofollow noopener" data-provider="{s}">{_t("Go to", "Перейти на")} {esc(n)} →</a></div>' for s, n, u, d in LLM_PARTNERS)
_two = f'''<div class="llm-two" data-px-place="local-llm">
  <div class="llm-card gl"><span class="eyebrow">MakeBiz</span><h3 style="margin-top:14px">{_t('Buy and install', 'Купить и установить')}</h3>
    <p>{_t('We pick and deliver the server or set up the one you already have, install the models, connect tasks and integrations and support the system',
           'Подберём и поставим сервер или настроим ваш, установим модели, подключим задачи и интеграции и возьмём систему на поддержку')}</p>
    <ul><li>{_t('Turnkey server of the right class or your own hardware', 'Сервер нужного класса под ключ или ваше оборудование')}</li>
      <li>{_t('Installation and setup', 'Установка и настройка')} {G['install']}</li>
      <li>{_t('Integrations with CRM, ERP, telephony and email', 'Интеграции с CRM, ERP, телефонией и почтой')}</li>
      <li>{_t('Support from', 'Поддержка от')} {G['support']['self']} {_t('a month or 24×7 SLA', 'в месяц или 24×7 SLA')}</li></ul>
    <a class="btn" href="#form" data-lead="buy">{_t('Get a quote', 'Получить расчёт')}</a></div>
  <div class="llm-card gl" id="rent"><span class="eyebrow">{_t('Partners', 'Партнёры')}</span><h3 style="margin-top:14px">{_t('Rent a GPU server', 'Арендовать GPU-сервер')}</h3>
    <p>{_t('Do not want to buy hardware? Rent a dedicated or GPU server from a partner, and we install the AI on it',
           'Не хотите покупать оборудование? Арендуйте выделенный или GPU-сервер у партнёра, а ИИ на него установим мы')}</p>
    <div class="llm-partners">{_rent_li}</div>
    <p class="llm-disc">{_t('Partner links: MakeBiz may receive a commission, your price does not change', 'Партнёрские ссылки: MakeBiz может получить вознаграждение, цена для вас не меняется')}</p>
    <a class="btn btn-ghost" href="#form" data-lead="rent">{_t('Rent and get it installed', 'Арендовать и установить')}</a></div>
</div>
<p class="llm-vps">{_t('For a regular VPS for a website, bot or app, compare providers and prices at', 'Обычный VPS для сайта, бота или приложения удобнее подобрать в нашем каталоге')} <a href="{SC_URL}" target="_blank" rel="noopener">servercalc.com</a></p>'''
llm_body += section(_t('Buy <span>or rent</span>', 'Купить <span>или арендовать</span>'),
    _t(f'By our estimate, renting costs {_pc(G["rent"][0])}-{_pc(G["rent"][1])}% of the hardware price a month, so owning pays off in about two years. Renting lets you start without buying hardware',
       f'По нашей оценке аренда стоит {_pc(G["rent"][0])}-{_pc(G["rent"][1])}% от цены оборудования в месяц, поэтому своё окупается примерно за два года. Аренда позволяет начать без покупки железа'),
    _two, id_='buy-or-rent', tone='tint')

# ---------- example calculations (scenarios from the calculator, not client projects)
def _ex(k, ttl, d):
    c = C[k]
    return (f'<div class="llm-ex gl"><div class="k">{esc(d)}</div><h3>{esc(ttl)}</h3><div class="v">{esc(c["short"])}</div><div class="c">{esc(c["title"])}</div>'
            f'<ul><li>{_t("Pays back in", "Окупаемость")}<b>{_mo(c["m"]) if c["m"] else "-"}</b></li><li>{_t("Subscriptions and API now", "Подписки и API сейчас")}<b>{esc(c["now"])}{_t(" a mo", " в мес")}</b></li>'
            f'<li>{_t("Staff time AI frees up", "Время, которое освободит ИИ")}<b>{esc(c["time"])}{_t(" a mo", " в мес")}</b></li></ul></div>')
llm_body += section(_t('Example <span>calculations</span>', 'Примеры <span>расчёта</span>'),
    _t('Typical configurations calculated with the same calculator. These are scenarios, not client projects', 'Типовые конфигурации, посчитанные тем же калькулятором. Это сценарии, а не проекты клиентов'),
    '<div class="grid g3">' +
    _ex('distr', _t('Distributor, 50 people', 'Дистрибьютор, 50 человек'), _t('Chat, knowledge base, documents, CRM assistant · CRM and ERP · 24×7', 'Чат, база знаний, документы, ассистент в CRM · CRM и ERP · круглосуточно')) +
    _ex('cc', _t('Call center, 200 people', 'Колл-центр, 200 человек'), _t('Chat, knowledge base, sales, call analysis up to 750k minutes · CRM and telephony · no downtime', 'Чат, база знаний, продажи, анализ до 750 тыс. минут звонков · CRM и телефония · без остановок')) +
    _ex('prod', _t('Manufacturing, 300 people', 'Производство, 300 человек'), _t('Chat, knowledge base, documents, developer help, data analytics · ERP · high quality', 'Чат, база знаний, документы, помощь разработчикам, аналитика данных · ERP · высокое качество')) +
    '</div>')

# ---------- FAQ
_sup = G['support']
llm_faq = [
    (_t('Which models do you install?', 'Какие модели ставите?'),
     _t('Open-weight models that run on your own server: families such as Llama, Qwen, Mistral and Gemma for chat and documents, Whisper-class models for speech. We pick the model for the task and the hardware and switch to better versions as they come out.',
        'Открытые модели, которые работают на вашем сервере: семейства Llama, Qwen, Mistral и Gemma для чата и документов, модели класса Whisper для речи. Модель подбираем под задачу и железо и переводим на новые версии, когда они выходят.')),
    (_t('Do I need a GPU?', 'Нужна ли видеокарта?'),
     _t('For a team, yes: models answer fast only on graphics cards with enough memory, from one 32 GB card in the smallest configuration to four 96 GB cards in the largest. The calculator picks the server class from A to F for your load.',
        'Для команды да: быстро модели отвечают только на видеокартах с достаточной памятью, от одной карты на 32 ГБ в самой простой конфигурации до четырёх по 96 ГБ в самой мощной. Калькулятор подбирает класс сервера от A до F под вашу нагрузку.')),
    (_t('What about updates?', 'Что с обновлениями?'),
     _t('Updates of models and software are part of support: with “Help” and “24×7 SLA” we install new versions after checking them on your tasks, with “Self” you get instructions and monitoring on request.',
        'Обновления моделей и программ входят в поддержку: в вариантах «Нужна помощь» и «24×7 SLA» ставим новые версии после проверки на ваших задачах, в варианте «Справимся сами» даём инструкции и мониторинг по желанию.')),
    (_t('Can you install it on a rented server?', 'Можно поставить на арендованный сервер?'),
     _t('Yes. Rent a dedicated or GPU server from a partner (is*hosting, DataPacket) or from your own provider, and we install and set up the AI on it. In the calculator choose “Rent” to see the monthly cost.',
        'Да. Арендуйте выделенный или GPU-сервер у партнёра (is*hosting, DataPacket) или у своего провайдера, а мы установим и настроим ИИ. В калькуляторе выберите «Аренда», чтобы увидеть цену в месяц.')),
    (_t('How long does the launch take?', 'Сколько занимает запуск?'),
     _t('It depends on hardware delivery and on the number of tasks and integrations. On a server that is already available we start the installation right after the technical meeting. The exact schedule comes with the quote.',
        'Зависит от поставки оборудования и числа задач и интеграций. Если сервер уже есть, установку начинаем сразу после технической встречи. Точный график присылаем вместе с расчётом.')),
    (_t('What is included in support?', 'Что входит в поддержку?'),
     _t(f'Three options a month: “Self” {_sup["self"]} (monitoring on request), “Help” {_sup["help"]} (updates and assistance), “24×7 SLA” {_sup["sla"]} (on-call team and response times).',
        f'Три варианта в месяц: «Справимся сами» {_sup["self"]} (мониторинг по желанию), «Нужна помощь» {_sup["help"]} (обновления и помощь), «24×7 SLA» {_sup["sla"]} (дежурство и сроки реакции).')),
    (_t('How is the price calculated?', 'Как считается цена?'),
     _t(f'Server of the chosen class with assembly and test, installation {G["install"]}, setup of each task and integrations; for “No downtime” a standby server is added. Services are shown as a range. Monthly costs are support and, if you rent, the rent. Prices as of {G["priceDate"]}, the exact quote follows a technical meeting.',
        f'Сервер выбранного класса со сборкой и тестом, установка {G["install"]}, настройка каждой задачи и интеграций, для режима «Без остановок» добавляется запасной сервер. Услуги показаны вилкой. Каждый месяц: поддержка и, если выбрана аренда, аренда. Цены на {G["priceDate"]}, точный расчёт после технической встречи.')),
]
llm_body += faq(llm_faq)

# ---------- form: company, team size, intent and calculation (ui.js puts them into the comment)
_form = form_block('local-llm', _t('Get an exact quote', 'Получить точный расчёт'),
    _t('Leave a contact: an engineer checks your calculation and arranges a technical meeting. We reply within a business day',
       'Оставьте контакт: инженер проверит расчёт и назначит техническую встречу. Ответим в течение рабочего дня'))
_lab = _t('<label>Task', '<label>Задача')
_form = _form.replace(_lab, f'<label>{_t("Company", "Компания")}<input name="company" autocomplete="organization"></label>'
    f'<label>{_t("Team size", "Размер команды")}<input name="team" inputmode="numeric" placeholder="{_t("e.g. 80 people", "например, 80 человек")}"></label>'
    f'<p class="llm-calc-note" hidden>{_t("Your calculation is attached", "Ваш расчёт приложен к заявке")} · <b></b></p>'
    f'<input type="hidden" name="intent" value="buy"><input type="hidden" name="calc" value="">' + _lab, 1)
llm_body += _form
llm_body += f'<script>var LLM_LANG="{LLM_PY}";</script><script src="{U("/assets/llm.js")}?v={V}" defer></script>'

# ---------- JSON-LD: service with the package prices
_cur = LF['cur']
_url = SITE + (en_path('/local-llm') if _EN else '/local-llm')
llm_ld = [{"@type": "Service", "name": _t('Local LLM server installation', 'Установка локальной нейросети на сервер'),
           "serviceType": _t('Private AI server', 'Локальный ИИ-сервер'), "url": _url, "provider": {"@id": SITE + "/#organization"},
           "areaServed": {"@type": "Country", "name": "United Arab Emirates"}, "inLanguage": LLM_PY,
           "description": _t('Turnkey on-premise LLM server or installation on a rented GPU server, with support', 'Локальная LLM на сервере под ключ или установка на арендованный GPU-сервер, с поддержкой'),
           "offers": {"@type": "AggregateOffer", "priceCurrency": _cur, "lowPrice": str(min(p['loAbs'] for p in LF['packs'])), "highPrice": str(max(p['hiAbs'] for p in LF['packs'])), "offerCount": str(len(LF['packs']))},
           "hasOfferCatalog": {"@type": "OfferCatalog", "name": _t('Local LLM packages', 'Пакеты локальной нейросети'), "itemListElement": [
               {"@type": "Offer", "name": p['n'], "description": p['w'], "url": _url + '#calc', "priceSpecification": {"@type": "PriceSpecification", "minPrice": str(p['loAbs']), "maxPrice": str(p['hiAbs']), "priceCurrency": _cur}}
               for p in LF['packs']]}}]
_crumbs = [('/', _t('Home', 'Главная')), ('/local-llm', _t('Local LLM server', 'Локальная нейросеть'))]
built.append(page('/local-llm', 'local-llm',
    _t('Local LLM server in the UAE: your own ChatGPT, price | MakeBiz', 'Локальная нейросеть на своём сервере в ОАЭ: цена | MakeBiz'),
    _t(f'Private ChatGPT on your own server in Dubai and the UAE: data stays inside, no per-seat subscriptions. Turnkey {P["start"]["from"]}, calculator with payback, or rent a GPU server.',
       f'Свой ChatGPT на сервере компании в Дубае и ОАЭ: данные внутри, без подписок на каждого сотрудника. Под ключ {P["start"]["from"]}, калькулятор с окупаемостью или аренда GPU-сервера.'),
    'ai', llm_body, llm_ld, _crumbs, llm_faq))
UPDATED, UPDATED_ISO = _UPD, _UPD_ISO
