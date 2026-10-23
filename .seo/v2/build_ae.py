# -*- coding: utf-8 -*-
"""Сборка новой русской версии makebiz.life в папку v2 (превью).
Запуск: python3 build_v2.py <папка_сайта>  -> пишет <папка_сайта>/v2/...
BASE = '/v2' на превью; при переносе на прод BASE = '' и PREVIEW = False.
"""
import os, sys, json, html, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from en_slugs import en_path

ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
BASE = os.environ.get('MB_BASE', '/v2')
PREVIEW = os.environ.get('MB_PREVIEW', '1') == '1'
OUT = os.path.join(ROOT, os.environ.get('MB_OUT', BASE.strip('/') or '.'))
# ===== константы сайта (makebiztechnologies.com, ОАЭ)
SITE = 'https://makebiztechnologies.com'
UPDATED = '23 октября 2026'
UPDATED_ISO = '2026-10-23'
V = os.environ.get('MB_V', 'a1')
PHONE = '+971 50 262 0927'
PHONE_TEL = '+971502620927'
TG = 'Anton_MakeBiz'
EMAIL = 'info@makebiztechnologies.com'
WA = '971502620927'
YM_ID = '112503709'
GA_ID = 'G-YPNHBR4DXK'
YA_VERIF = '4da996bcccf8e587'
CUR = 'AED'
LEGAL = 'MakeBiz Technologies FZE LLC · Ajman NuVentures Centre · рег. номер 2624215090888 · Amber Gem Tower, Аджман, ОАЭ'
USD_AED = 3.6725
def aed(usd): return f'{round(usd * USD_AED):,}'.replace(',', '\u00a0') + '\u00a0AED'

def U(p):
    """адрес внутри нового сайта"""
    if p == '/':
        return (BASE + '/') if BASE else '/'
    return BASE + p

def esc(s):
    return html.escape(s, quote=True)

# ---------------------------------------------------------------- навигация
BITRIX_MENU = [
    ('/bitrix', 'Внедрение Битрикс24', 'CRM, воронки, процессы под ключ'),
    ('/bitrix-support', 'Поддержка', 'Пакеты часов, администрирование'),
    ('/bitrix-messengers', 'Мессенджеры', 'WhatsApp, Telegram, соцсети'),
    ('/bitrix-integrations', 'Интеграции с учётом', 'Zoho Books, QuickBooks, Odoo, 1С'),
    ('/bitrix-korobka', 'Коробочный Битрикс24', 'Внедрение на вашем сервере'),
    ('/bitrix-licenses', 'Лицензии и цены', 'Облако от 180 AED, коробка от 13 184 AED'),
    ('/bi-analitika', 'BI-аналитика', 'Дашборды для руководителя'),
]
AI_MENU = [
    ('/ai-agents', 'Внедрение ИИ-агентов', 'Агенты в продажах, финансах, закупках'),
    ('/ai-agents/rop', 'ИИ-РОП', 'Переписки, план, разбор ошибок'),
    ('/ai-agents/svyaznoy', 'Связной', 'Контакты и отношения'),
    ('/ai-agents/zvonki', 'Речевая аналитика', 'Оценка каждого звонка'),
    ('/ai-agents/hr', 'HR-агент', 'Отбор и собеседования ботом'),
    ('/ai-agents/zakupki', 'Закупки', 'Запросы и сравнение КП'),
    ('/ai-agents/marketing', 'Маркетолог', 'SEO, GEO и реклама'),
    ('/ai-agents/finansy', 'Финансы', 'Пульс компании'),
]

def nav_href(p):
    if p == 'CALC':
        return '/calculator-agents'
    return U(p)

def header(active):
    def dd(title, items, key):
        cls = ' is-active' if active.startswith(key) else ''
        links = ''.join(
            f'<a class="dd-item" href="{nav_href(p)}"><b>{esc(t)}</b><span>{esc(s)}</span></a>'
            for p, t, s in items)
        return (f'<div class="nav-dd{cls}"><button class="nav-link" type="button" aria-expanded="false">{title}'
                f'<svg width="10" height="10" viewBox="0 0 10 10" aria-hidden="true"><path d="M2 3.5 5 6.5 8 3.5" fill="none" stroke="currentColor" stroke-width="1.6"/></svg></button>'
                f'<div class="dd-panel">{links}</div></div>')
    def a(p, t, key):
        cls = ' is-active' if active == key else ''
        return f'<a class="nav-link{cls}" href="{p}">{t}</a>'
    return f'''<header class="hdr" id="top">
  <div class="wrap hdr-in">
    <a class="logo" href="{U('/')}" aria-label="MakeBiz, на главную"><img src="{U('/img/logo.png')}" width="234" height="80" alt="MakeBiz"></a>
    <nav class="nav" aria-label="Основное меню">
      {dd('Битрикс24', BITRIX_MENU, 'bitrix')}
      {dd('ИИ-агенты', AI_MENU, 'ai')}
      {a(U('/keysy'), 'Кейсы', 'keysy')}
      {a(U('/news'), 'Новости', 'news')}
      {a(U('/partners'), 'Партнёрам', 'partners')}
      {a(U('/contacts'), 'Контакты', 'contacts')}
    </nav>
    <div class="hdr-right">
      <div class="lang" role="group" aria-label="Язык сайта"><svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M3 12h18M12 3c2.6 2.6 3.8 5.6 3.8 9s-1.2 6.4-3.8 9c-2.6-2.6-3.8-5.6-3.8-9S9.4 5.6 12 3z" fill="none" stroke="currentColor" stroke-width="1.8"/></svg><span class="on" aria-current="true">RU</span><a href="/en" hreflang="en" lang="en" title="English version">EN</a></div>
      <a class="hdr-phone" href="tel:{PHONE_TEL}">{PHONE}</a>
      <a class="btn btn-sm" href="#form">Обсудить задачу</a>
      <button class="burger" type="button" aria-label="Открыть меню" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
  <div class="mnav" hidden>
    <div class="mnav-group"><div class="mnav-t">Битрикс24</div>{''.join(f'<a href="{nav_href(p)}">{esc(t)}</a>' for p,t,_ in BITRIX_MENU)}</div>
    <div class="mnav-group"><div class="mnav-t">ИИ-агенты</div>{''.join(f'<a href="{nav_href(p)}">{esc(t)}</a>' for p,t,_ in AI_MENU)}</div>
    <div class="mnav-group"><a href="{U('/o-kompanii')}">О компании</a><a href="{U('/ceny')}">Цены</a><a href="{U('/keysy')}">Кейсы</a><a href="{U('/vps')}">Серверы и VPS</a><a href="{U('/news')}">Новости</a><a href="{U('/partners')}">Партнёрам</a><a href="{U('/contacts')}">Контакты</a><a href="https://wa.me/{WA}">WhatsApp</a><a href="tel:{PHONE_TEL}">{PHONE}</a></div>
  </div>
</header>'''

from landings_ae_list import LANDINGS_AE
def footer():
    return f'''<footer class="ftr">
  <div class="wrap ftr-grid">
    <div class="ftr-brand">
      <a class="logo" href="{U('/')}"><img src="{U('/img/logo.png')}" width="234" height="80" alt="MakeBiz"></a>
      <p>Официальный партнёр Битрикс24 в ОАЭ. Внедряем Битрикс24 и ИИ-агентов для компаний в Дубае и по всем Эмиратам. 8 лет в IT, работаем на русском и английском</p>
      <p class="ftr-contacts"><a href="tel:{PHONE_TEL}">{PHONE}</a><br><a href="https://wa.me/{WA}">WhatsApp</a> · <a href="https://t.me/{TG}">Telegram @{TG}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
    </div>
    <div><div class="ftr-t">Битрикс24</div>{''.join(f'<a href="{U(p)}">{esc(t)}</a>' for p,t,_ in BITRIX_MENU)}</div>
    <div><div class="ftr-t">ИИ-агенты</div><a href="{U('/ai-agents')}">Внедрение ИИ-агентов</a><a href="{U('/ai-agents/rop')}">ИИ-РОП</a><a href="{U('/ai-agents/zvonki')}">Речевая аналитика</a><a href="{U('/ai-agents/hr')}">HR-агент</a><a href="{U('/ai-agents/marketing')}">Маркетолог</a></div>
    <div><div class="ftr-t">Компания</div><a href="{U('/o-kompanii')}">О компании</a><a href="{U('/ceny')}">Цены</a><a href="{U('/keysy')}">Кейсы</a><a href="{U('/vps')}">Серверы и VPS</a><a href="{U('/news')}">Новости</a><a href="{U('/partners')}">Партнёрам</a><a href="https://t.me/makebizchannel">Telegram-канал</a><a href="{U('/contacts')}">Контакты</a><a href="{BASE}/en">English version</a></div>
  </div>
  <div class="wrap ftr-sol" style="display:flex;flex-wrap:wrap;gap:4px 18px;align-items:baseline;padding-top:18px;margin-top:18px;border-top:1px solid rgba(127,140,170,.18)"><span class="ftr-t" style="margin:0 6px 0 0">Под задачу</span>{''.join(f'<a style="display:inline;padding:2px 0" href="{U(p)}">{esc(t)}</a>' for p,t,_,_,_ in LANDINGS_AE)}</div>
  <div class="wrap ftr-legal">
    <span>{LEGAL}</span>
    <span><a href="/privacy">Политика конфиденциальности</a> · <a href="/terms">Пользовательское соглашение</a> · © 2026 MakeBiz</span>
  </div>
</footer>
<div class="mbar"><a href="tel:{PHONE_TEL}">Позвонить</a><a href="https://wa.me/{WA}">WhatsApp</a><a class="mbar-cta" href="#form">Заявка</a></div>'''

# ---------------------------------------------------------------- блоки
def crumbs(items):
    """items: [(href|None, title)]"""
    parts = []
    for href, t in items:
        parts.append(f'<a href="{href}">{esc(t)}</a>' if href else f'<span aria-current="page">{esc(t)}</span>')
    return '<nav class="crumbs wrap" aria-label="Хлебные крошки">' + '<i>/</i>'.join(parts) + '</nav>'

def hero(eyebrow, h1, lead, answer, cta, cta2, img, chips, alt):
    chips_html = ''.join(f'<li><b>{esc(a)}</b><span>{esc(b)}</span></li>' for a, b in chips)
    c2 = f'<a class="btn btn-ghost" href="{cta2[0]}">{esc(cta2[1])}</a>' if cta2 else ''
    return f'''<section class="hero">
  <div class="wrap hero-grid">
    <div class="hero-text">
      <span class="eyebrow">{esc(eyebrow)}</span>
      <h1>{h1}</h1>
      <p class="lead">{lead}</p>
      <p class="answer">{answer}</p>
      <div class="cta-row"><a class="btn" href="{cta[0]}">{esc(cta[1])}</a>{c2}</div>
      <p class="updated">Обновлено {UPDATED}</p>
    </div>
    {img if img.startswith('<') else f'<figure class="hero-img"><img src="{img}" alt="{esc(alt)}" width="1376" height="768" fetchpriority="high"></figure>'}
  </div>
  <div class="wrap"><ul class="chips">{chips_html}</ul></div>
</section>'''

def section(title, sub='', body='', id_='', tone=''):
    idattr = f' id="{id_}"' if id_ else ''
    cls = 'sec' + (' ' + tone if tone else '')
    sub_html = f'<p class="sec-sub">{sub}</p>' if sub else ''
    return f'<section class="{cls}"{idattr}><div class="wrap"><h2>{title}</h2>{sub_html}{body}</div></section>'

def cards(items, cols=3, numbered=False):
    out = []
    for i, it in enumerate(items, 1):
        t, d = it[0], it[1]
        tag = f'<span class="num">{i:02d}</span>' if numbered else ''
        out.append(f'<div class="card">{tag}<h3>{esc(t)}</h3><p>{d}</p></div>')
    return f'<div class="grid g{cols}">' + ''.join(out) + '</div>'

def steps(items):
    out = ''.join(f'<li><span class="step-n">{i}</span><h3>{esc(t)}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(items, 1))
    return f'<div class="track"><i></i></div><ol class="steps">{out}</ol>'

def prices(items, note=''):
    out = []
    for it in items:
        name, price, unit, lines, hot = it
        li = ''.join(f'<li>{esc(x)}</li>' for x in lines)
        out.append(f'<div class="price{" is-hot" if hot else ""}"><div class="price-name">{esc(name)}</div>'
                   f'<div class="price-val">{price}</div><div class="price-unit">{esc(unit)}</div><ul>{li}</ul>'
                   f'<a class="btn {"" if hot else "btn-ghost"}" href="#form">Выбрать</a></div>')
    n = f'<p class="note">{note}</p>' if note else ''
    return f'<div class="grid g{min(len(items),4)} prices">' + ''.join(out) + '</div>' + n

def ba(items):
    """было/стало"""
    out = ''.join(f'<div class="ba"><div class="ba-was"><span>Было</span>{esc(w)}</div><div class="ba-now"><span>Стало</span>{esc(n)}</div></div>' for w, n in items)
    return f'<div class="ba-list">{out}</div>'

CASES = {
    'cdek-b2b': ('СДЭК', 'Корпоративный B2B на Битрикс24 с агентами и аналитикой', 'корпоративные клиенты в разных системах и вручную', 'ведение, поддержка и аналитика в одном контуре', 'Логистика · Битрикс24 · ИИ-агенты · BI'),
    'unilin-crm': ('Unilin', 'Битрикс24 для разъездных менеджеров и аналитика по рынку', 'регионы и торговые точки вне единой системы', 'весь регион в CRM с телефона, интеграция с 1С и ERP', 'Производство · Битрикс24 · 1С · BI'),
    'haval-vector': ('HAVAL', 'Контроль звонков сети автосалонов', 'сотни тысяч минут звонков никто не мог проверить', 'более 300 000 минут в месяц по 40+ критериям', 'Автодилеры · ИИ-анализ звонков · BI'),
    'performia-crm': ('Перформия', 'Продажи, обучение, финансы и сквозная аналитика', 'продажи, курсы и финансы жили порознь', 'весь цикл и сквозная аналитика в одном окне', 'Обучение · Битрикс24 · BI'),
    'apartika-crm': ('Апартика', 'Аренда недвижимости по всей России в одной CRM', 'объявления, площадки и заявки вручную и порознь', 'постинг, заявки, брони и аналитика в одной CRM', 'Недвижимость · CRM · ИИ-агент · BI'),
}

CASEJ = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'cases.json'), encoding='utf-8'))
SPHERES = [('prodazhi', 'Продажи и B2B'), ('logistika', 'Логистика'), ('avto', 'Автобизнес'), ('ecom', 'Интернет-магазины'), ('uslugi', 'Услуги и сервис'),
           ('nedvizhimost', 'Недвижимость'), ('obrazovanie', 'Образование'), ('medicina', 'Медицина'), ('proizvodstvo', 'Производство и опт')]
SPH = dict(SPHERES)
PRODS = [('crm', 'Битрикс24 и CRM'), ('ai-agents', 'ИИ-агенты'), ('analytics', 'BI и аналитика')]
PRD = dict(PRODS)
# без бренда Vector на сайте ОАЭ: речевая аналитика
VFIX = [('а Vector слушает звонки', 'а речевая аналитика слушает звонки'), ('интеграции с площадками, Vector, BI', 'интеграции с площадками, речевая аналитика, BI'),
        ('Vector показывает, как команда', 'Речевая аналитика показывает, как команда'), ('<b>Vector</b> и BI', '<b>речевая аналитика</b> и BI'),
        ('HAVAL: Vector слушает', 'HAVAL: речевая аналитика слушает'), ('разбирает Vector:', 'разбирает речевая аналитика:'),
        ('Vector, BI-дашборды и AI-агенты', 'Речевая аналитика, BI-дашборды и AI-агенты'), ('Речевую аналитику Vector сделали', 'Речевую аналитику сделали'),
        ('Vector, агенты и BI:', 'Речевая аналитика, агенты и BI:'), ('речевую аналитику Vector:', 'речевую аналитику:')]
for c in CASEJ:
    for k, v in list(c.items()):
        if isinstance(v, str):
            for a, b in VFIX: v = v.replace(a, b)
            c[k] = v
IND_FIX = {'haval-vector': ['avto', 'prodazhi']}
for c in CASEJ:
    if c['slug'] in IND_FIX: c['ind'] = IND_FIX[c['slug']]
CASE_METRIC = {'haval-vector': ('300 000+', 'минут звонков в месяц'), 'apartika-crm': ('1 000+', 'объектов в одной CRM'),
               'cdek-b2b': ('5', 'ИИ-агентов в работе'), 'unilin-crm': ('4', 'среза BI-аналитики'), 'performia-crm': ('110', 'рабочих дней до запуска')}
for c in CASEJ:
    if not c.get('metric') and c['slug'] in CASE_METRIC: c['metric_v'], c['metric_t'] = CASE_METRIC[c['slug']]
    elif c.get('metric'): c['metric_v'], c['metric_t'] = c['metric'], ''
CJ = {c['slug']: c for c in CASEJ}
def notag(s): return re.sub('<[^>]+>', '', s or '')
def clip(s, n):
    s = s.strip()
    if len(s) <= n: return s
    cut = s[:n]
    i = cut.rfind('. ')
    if i > n * 0.6: return cut[:i + 1]
    return cut[:cut.rfind(' ')].rstrip(',:;') 
def case_card(c):
    org = c['client'].split(',')[0]
    tags = ' · '.join([SPH.get(i, i) for i in c['ind'][:2]] + [PRD.get(p, p) for p in c['products']])
    return (f'<a class="case tilt" href="{U("/keysy/" + c["slug"])}" data-ind="{" ".join(c["ind"])}" data-prod="{" ".join(c["products"])}">'
            f'<div class="case-org">{esc(org)}</div>' + (f'<div class="case-metric"><b>{esc(c["metric_v"])}</b><span>{esc(c["metric_t"])}</span></div>' if c.get("metric_v") else '') + f'<h3>{esc(notag(c["title"]).split(":", 1)[-1].strip())}</h3>'
            f'<div class="case-ba"><p><span>Было</span>{esc(c["was"])}</p><p><span>Стало</span>{esc(c["now"])}</p></div>'
            f'<div class="case-tags">{esc(tags)}</div><span class="case-more">Читать кейс →</span></a>')
def case_cards(slugs):
    return '<div class="grid g3 cases">' + ''.join(case_card(CJ[s]) for s in slugs if s in CJ) + '</div>'


def contract_block():
    items = [
        ('Работаем по договору', 'Договор с MakeBiz Technologies FZE LLC, счета в дирхамах, оплата на счёт компании в ОАЭ. Проект договора пришлём до созвона, если нужно согласовать заранее'),
        ('Фиксированная смета', 'Стандартные работы по прайсу, сложные после короткого обследования: вы видите объём и цену до начала работ'),
        ('Доступы и данные у вас', 'Портал, сервер и аккаунты остаются за компанией. Работаем под отдельной учётной записью, доступы закрываются по окончании'),
        ('Одна команда', 'Внедрение, поддержка, интеграции и ИИ-агенты делает одна команда, не нужно собирать подрядчиков'),
    ]
    return section('Договор и гарантии', 'Что вы получаете, кроме самой работы', cards(items, 4), tone='tint')

def faq(items):
    out = ''.join(f'<details><summary>{esc(q)}</summary><p>{a}</p></details>' for q, a in items)
    return section('Вопросы и ответы', '', f'<div class="faq">{out}</div>', id_='faq')

def form_block(page, title='Обсудим задачу', sub='Оставьте контакт, ответим в течение рабочего дня. Проведём короткую диагностику и скажем, с чего начать'):
    return f'''<section class="sec formsec" id="form"><div class="wrap form-grid">
  <div class="form-text"><h2>{esc(title)}</h2><p class="sec-sub">{esc(sub)}</p>
    <ul class="form-direct"><li><a href="https://wa.me/{WA}">WhatsApp {PHONE}</a></li><li><a href="https://t.me/{TG}">Telegram @{TG}</a></li><li><a href="tel:{PHONE_TEL}">{PHONE}</a></li></ul></div>
  <form class="lead-form" data-page="{esc(page)}" novalidate>
    <label>Имя<input name="name" autocomplete="name" required></label>
    <label>Телефон или Telegram<input name="phone" autocomplete="tel" required placeholder="+971 ... или @username"></label>
    <label>Задача<textarea name="comment" rows="3" placeholder="Коротко: что нужно сделать"></textarea></label>
    <input class="hp" name="_gotcha" tabindex="-1" autocomplete="off" aria-hidden="true">
    <button class="btn btn-wide" type="submit">Отправить заявку</button>
    <p class="form-note">Нажимая кнопку, вы соглашаетесь с <a href="/privacy">политикой конфиденциальности</a></p>
    <p class="form-ok" hidden>Спасибо! Заявка принята, скоро свяжемся</p>
    <p class="form-err" hidden>Не получилось отправить. Напишите нам в <a href="https://wa.me/{WA}">WhatsApp</a></p>
  </form>
</div></section>'''

def crosslink(to):
    if to == 'ai':
        return section('Второе направление: ИИ-агенты', 'Когда CRM настроена, следующий шаг убрать рутину. Агенты работают внутри Битрикс24 и Telegram',
            f'<div class="cross"><div><h3>ИИ-агенты для продаж, финансов и закупок</h3><p>Отвечают клиентам, разбирают звонки, следят за воронкой и деньгами. Один агент от 5 000 AED</p></div><a class="btn" href="{U("/ai-agents")}">Смотреть ИИ-агентов</a></div>', tone='dark')
    return section('Второе направление: Битрикс24', 'Агенты работают лучше, когда процессы собраны в CRM',
        f'<div class="cross"><div><h3>Внедрение и поддержка Битрикс24</h3><p>CRM, воронки, WhatsApp, интеграции с учётом, лицензии и BI-аналитика. Стандартная настройка от 10 000 AED</p></div><a class="btn" href="{U("/bitrix")}">Смотреть Битрикс24</a></div>', tone='dark')

# ---------- статьи по теме (журнал и новости) для перелинковки
J = lambda slug: '/journal/' + slug + '/'
N = lambda slug: U('/news/' + slug)
RELATED = {
 '/': [(N('vnedrenie-bitrix24-v-oae-otlichiya'), 'Внедрение Битрикс24 в ОАЭ: чем проект отличается от российского'), (N('iz-chego-skladyvaetsya-smeta-vnedreniya-crm'), 'Смета внедрения CRM в ОАЭ: из чего складывается цена'), (N('chto-avtomatiziruyut-pervym-v-dubae'), 'С чего начинают автоматизацию компании в Дубае'), (N('ai-agent-v-whatsapp-vhodyashchie-zayavki'), 'ИИ-агент в WhatsApp: как он разбирает входящие заявки')],
}
def add_related(path, body):
    items = RELATED.get(path)
    if not items or 'class="sec formsec"' not in body: return body
    li = ''.join(f'<a class="rel-a gl" href="{u}"><small>Новости</small><b>{esc(t)}</b><span>Читать →</span></a>' for u, t in items)
    blk = f'<section class="sec rel-sec"><div class="wrap"><h2>Статьи по теме</h2><p class="sec-sub">Разбираем подробнее в новостях MakeBiz</p><div class="rel">{li}</div><p class="more"><a href="{U("/news")}">Все новости →</a></p></div></section>'
    i = body.index('<section class="sec formsec"')
    return body[:i] + blk + body[i:]

# ---------------------------------------------------------------- страница
COUNTERS = ('<script defer src="https://makebiz-makebiz-platform-3628.twc1.net/px/t.js" data-site="makebiz-com" data-endpoint="https://makebiz-makebiz-platform-3628.twc1.net/px"></script>\n'
            '<script>' + open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'consent_ym.js'), encoding='utf-8').read() + '</script>\n'
            '<script>' + open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'consent_banner.js'), encoding='utf-8').read() + '</script>\n'
            '<script async src="https://www.googletagmanager.com/gtag/js?id=' + GA_ID + '"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag(\'js\',new Date());gtag(\'config\',\'' + GA_ID + '\');</script>')
ORG = {
    "@type": ["Organization", "ProfessionalService"], "@id": SITE + "/#organization", "name": "MakeBiz", "alternateName": "MakeBiz Technologies",
    "legalName": "MakeBiz Technologies FZE LLC", "url": SITE + "/", "logo": SITE + "/favicon.png", "image": SITE + "/og-image.jpg",
    "telephone": PHONE_TEL, "email": EMAIL, "priceRange": "AED",
    "address": {"@type": "PostalAddress", "streetAddress": "Amber Gem Tower, Sheikh Khalifa Street", "addressLocality": "Ajman", "addressCountry": "AE"},
    "identifier": {"@type": "PropertyValue", "propertyID": "Ajman NuVentures Centre registration number", "value": "2624215090888"},
    "areaServed": [{"@type": "City", "name": "Dubai"}, {"@type": "Country", "name": "United Arab Emirates"}],
    "knowsLanguage": ["ru", "en"],
    "founder": {"@type": "Person", "@id": SITE + "/#founder", "name": "Антон Чернобаев"},
    "knowsAbout": ["Битрикс24", "внедрение CRM в ОАЭ", "коробочный Битрикс24", "интеграция Битрикс24 с Zoho Books", "WhatsApp в CRM", "VAT в CRM", "BI-аналитика", "ИИ-агенты", "речевая аналитика звонков"],
    "disambiguatingDescription": "Официальный партнёр и интегратор Битрикс24 в ОАЭ: Битрикс24, ИИ-агенты и BI. Не занимается регистрацией компаний, визами и лицензиями",
    "hasCredential": {"@type": "EducationalOccupationalCredential", "name": "Официальный партнёр Битрикс24", "credentialCategory": "partner"},
    "sameAs": ["https://t.me/makebizchannel", "https://makebiz.life/"],
}


EN_PAGES = {'/', '/bitrix', '/bitrix-support', '/ai-agents', '/keysy', '/contacts'}
def hreflang(path):
    ru = SITE + (path if path != '/' else '/')
    en = SITE + en_path(path)
    return (f'\n<link rel="alternate" hreflang="ru" href="{ru}"><link rel="alternate" hreflang="en" href="{en}">'
            f'<link rel="alternate" hreflang="x-default" href="{ru}">')

def page(path, slug, title, desc, active, body, ld_extra, crumb_items, faq_items=None):
    body = add_related(path, body)
    canon = SITE + (path if path != '/' else '/')
    graph = [ORG, {"@type": "WebPage", "@id": canon + "#webpage", "url": canon, "name": title, "description": desc,
                   "inLanguage": "ru", "dateModified": UPDATED_ISO, "isPartOf": {"@id": SITE + "/#website"},
                   "publisher": {"@id": SITE + "/#organization"}}]
    if crumb_items:
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": t, "item": SITE + p} for i, (p, t) in enumerate(crumb_items)]})
    if faq_items:
        graph.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub('<[^>]+>', '', a)}} for q, a in faq_items]})
    graph += ld_extra
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False).replace('</', '<\\/')
    robots = 'noindex, nofollow' if PREVIEW else 'index, follow, max-image-preview:large'
    preview_bar = (f'<div class="pv">Превью нового сайта · закрыто от поисковиков · <a href="/">текущий сайт</a></div>' if PREVIEW else '')
    og_img = SITE + U('/img/og.jpg')
    doc = f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canon}">{hreflang(path)}
<meta name="yandex-verification" content="{YA_VERIF}">
<meta property="og:type" content="website"><meta property="og:locale" content="ru_RU"><meta property="og:site_name" content="MakeBiz">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{canon}"><meta property="og:image" content="{og_img}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="icon" href="/favicon-32.png" sizes="32x32"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="{U('/assets/onest-cyrillic.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{U('/assets/site.css')}?v={V}">
<meta name="theme-color" content="#04050A">
<script type="application/ld+json">{ld}</script>
{'' if PREVIEW else COUNTERS}
</head>
<body data-page="{slug}"><div class="flag" aria-hidden="true"><i></i><i></i><i></i></div>
{preview_bar}
{header(active)}
<main>
{crumbs([(U(p) if p != crumb_items[-1][0] else None, t) for p, t in crumb_items]) if crumb_items and len(crumb_items) > 1 else ''}
{body}
</main>
{footer()}
<script src="{U('/assets/site.js')}?v={V}" defer></script>
</body>
</html>'''
    doc = doc.replace('href="/en" hreflang="en"', 'href="' + BASE + en_path(path) + '" hreflang="en"', 1)
    fn = 'index.html' if path == '/' else path.strip('/') + '.html'
    os.makedirs(os.path.dirname(os.path.join(OUT, fn)), exist_ok=True)
    open(os.path.join(OUT, fn), 'w', encoding='utf-8').write(doc)
    return fn

def service_ld(name, desc, url, price=None, area='United Arab Emirates'):
    s = {"@type": "Service", "name": name, "description": desc, "url": SITE + url, "provider": {"@id": SITE + "/#organization"},
         "areaServed": {"@type": "Country", "name": area}, "serviceType": name}
    if price:
        s["offers"] = {"@type": "Offer", "price": str(price), "priceCurrency": "AED", "url": SITE + url}
    return s

IMG = lambda n: U('/img/' + n)

# ---------------------------------------------------------------- живые 3D-панели героя
def VIS(kind, top_left, top_right, body, f1=None, f2=None):
    fl = ''
    if f1: fl += f'<div class="flt f1"><small>{esc(f1[0])}</small><b>{esc(f1[1])}</b></div>'
    if f2: fl += f'<div class="flt f2"><small>{esc(f2[0])}</small><b>{esc(f2[1])}</b></div>'
    return (f'<div class="vis-wrap"><div class="vis" data-vis="{kind}"><div class="vis-top"><span class="live">{esc(top_left)}</span><span>{top_right}</span></div>'
            f'<div class="vis-body">{body}</div><span class="vis-note">демо-данные</span></div>{fl}</div>')

V_BOARD = VIS('board', 'Битрикс24 · воронка онлайн', 'Сделок в работе <b data-cnt>24</b>',
    '<div class="cols"><div class="col"><h4>Новые</h4></div><div class="col"><h4>Квалификация</h4></div><div class="col"><h4>КП отправлено</h4></div><div class="col"><h4>Оплата ✓</h4></div></div>',
    ('Сделка из WhatsApp', 'создана за 2 сек'), ('Счёт с VAT 5%', 'оплачен ✓'))
V_TICKETS = VIS('tickets', 'Поддержка Битрикс24', 'Решено за месяц <b data-cnt>128</b>', '<div class="rows"></div>',
    ('Ответ на заявку', 'в течение дня'), ('Пакет 10 часов', '2 300 AED'))
V_CHAT = VIS('chat', 'Мессенджеры в Битрикс24', 'Каналов <b>5</b>',
    '<div class="deal"><div class="deal-h"><b>Сделка: Al Noor Trading LLC</b><span>этап «Новая»</span></div><div class="msgs"></div></div>',
    ('Новое сообщение', 'сделка создана'), ('Переписка', 'в карточке клиента'))
V_SYNC = VIS('sync', 'Обмен Битрикс24 ↔ Zoho Books', 'Документов <b data-cnt>1 240</b>',
    '<div class="sync"><div class="sys"><h4>Битрикс24</h4><div class="it">Сделка · Al Noor</div><div class="it">Компания · Palm Supply</div><div class="it">Счёт INV-418</div><div class="it">Товары и цены</div><div class="it">Оплата получена</div></div>'
    '<div class="pipe"><span class="pk"></span><span class="pk b"></span></div>'
    '<div class="sys"><h4>Zoho Books</h4><div class="it">Customer</div><div class="it">TRN и VAT 5%</div><div class="it">Invoice INV-418</div><div class="it">Остатки склада</div><div class="it">Payment</div></div></div>',
    ('Двойной ввод', 'больше не нужен'), ('Оплата в учёте', 'двинула сделку'))
V_LIC = VIS('license', 'Лицензии Битрикс24', 'в месяц <b>AED</b>',
    f'<div class="tiers"><div class="tier"><span><b>Basic</b><small>5 пользователей</small></span><span class="us">{aed(49)}</span></div>'
    f'<div class="tier"><span><b>Standard</b><small>50 пользователей</small></span><span class="us">{aed(99)}</span></div>'
    f'<div class="tier"><span><b>Professional</b><small>100 пользователей</small></span><span class="us">{aed(199)}</span></div>'
    f'<div class="tier"><span><b>Коробка</b><small>ваш сервер, год</small></span><span class="us">{aed(3590)}</span></div></div>',
    ('Цены', 'bitrix24.ae'), ('Продление', 'без простоя'))
V_BOX = VIS('license', 'Битрикс24 · ваш сервер', 'Лицензия <b>✓</b>',
    f'<div class="tiers"><div class="tier"><span><b>Business</b><small>50 пользователей</small></span><span class="us">{aed(3590)}</span></div>'
    '<div class="tier"><span><b>Business</b><small>100, 250, 500</small></span><span class="us">по запросу</span></div>'
    f'<div class="tier"><span><b>Enterprise</b><small>от 1 000 пользователей</small></span><span class="us">{aed(24990)}</span></div>'
    '<div class="tier"><span><b>Сервер</b><small>ваш или в ОАЭ</small></span><span class="us">под ключ</span></div></div>',
    ('Сервер', 'ваш дата-центр'), ('Данные', 'в своём контуре'))
V_BI = VIS('bi', 'Дашборд руководителя', 'Обновлено <b>сейчас</b>',
    '<div class="kpis"><div class="kpi"><small>Выручка, тыс. AED</small><b data-to="860">0</b></div><div class="kpi"><small>Конверсия</small><b data-to="23" data-suf="%">0</b></div><div class="kpi"><small>Сделок</small><b data-to="148">0</b></div></div>'
    '<div class="chart"><svg viewBox="0 0 400 190" preserveAspectRatio="none"><defs><linearGradient id="ga" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7FA0FF"/><stop offset="1" stop-color="#7FA0FF" stop-opacity="0"/></linearGradient></defs>'
    + ''.join(f'<rect class="bar" x="{18+i*38}" y="{190-h}" width="22" height="{h}" rx="5" style="animation-delay:{i*0.15:.2f}s"/>' for i, h in enumerate([60, 80, 70, 105, 95, 130, 120, 150, 165, 175]))
    + '<path class="ar" d="M0 160 C60 150 90 120 140 118 S220 90 260 70 S340 40 400 25 L400 190 L0 190Z"/><path class="ln" d="M0 160 C60 150 90 120 140 118 S220 90 260 70 S340 40 400 25"/></svg></div>',
    ('План месяца', 'выполнен на 104%'), ('Источник', 'CRM + учёт + реклама'))
V_AGENTS = VIS('agents', 'ИИ-агенты · работают', 'Агентов <b>7</b>', '<span class="core"></span><div class="rows" style="margin-right:84px"></div>',
    ('Ответ клиенту', 'за 12 сек'), ('Работают', '24/7'))
V_HOME = V_BOARD

# ================================================================ СТРАНИЦЫ
built = []

# ---------- ГЛАВНАЯ
home_faq = [
    ('Чем занимается MakeBiz в ОАЭ?', 'Два направления. Первое: внедрение и поддержка Битрикс24 для компаний в Дубае и по всем Эмиратам, включая WhatsApp, интеграции с учётными системами, лицензии и BI-аналитику. Второе: ИИ-агенты, которые берут на себя рутину в продажах, финансах, закупках и найме.'),
    ('Вы официальный партнёр Битрикс24?', 'Да, MakeBiz Technologies официальный партнёр Битрикс24 в ОАЭ: внедряем, поддерживаем порталы и помогаем с лицензиями облачного и коробочного Битрикс24.'),
    ('Сколько стоит внедрение Битрикс24?', 'Стандартная настройка CRM Битрикс24 от 10 000 AED. Работы сверх стандарта считаем по ставке 200 AED в час, смету фиксируем после короткого обследования. Лицензия Битрикс24 оплачивается отдельно.'),
    ('Сколько стоят ИИ-агенты?', 'Один агент на вашем процессе от 5 000 AED, обслуживание 10% от стоимости внедрения в месяц. Демонстрацию на вашем процессе проводим бесплатно.'),
    ('Можно подключить WhatsApp к Битрикс24?', 'Да. Подключение WhatsApp и других мессенджеров стоит 500 AED, подписка сервиса оплачивается отдельно. Каждое сообщение создаёт сделку и попадает в карточку клиента.'),
    ('Вы работаете только в Дубае?', 'Работаем с компаниями по всем Эмиратам, встречи в Дубае или по видеосвязи. Говорим на русском и английском, документы и счета в дирхамах.'),
    ('С чего начать?', 'Оставьте заявку. Проведём бесплатную диагностику: посмотрим, где теряются заявки и время, и предложим первый шаг с ценой и сроком.'),
]
ICON = {
 'server': '<svg viewBox="0 0 40 40"><rect x="7" y="7" width="26" height="9" rx="3" class="i1"/><rect x="7" y="19" width="26" height="9" rx="3" class="i2"/><circle cx="12" cy="11.5" r="1.6" class="i3"/><circle cx="12" cy="23.5" r="1.6" class="i3"/><rect x="17" y="31" width="6" height="3" rx="1" class="i3"/></svg>',
 'flow': '<svg viewBox="0 0 40 40"><rect x="5" y="9" width="8" height="22" rx="3" class="i1"/><rect x="16" y="9" width="8" height="15" rx="3" class="i2"/><rect x="27" y="9" width="8" height="9" rx="3" class="i3"/></svg>',
 'pulse': '<svg viewBox="0 0 40 40"><path d="M4 21h8l3-8 5 15 4-11 3 4h9" fill="none" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" class="ip"/></svg>',
 'chat': '<svg viewBox="0 0 40 40"><rect x="5" y="8" width="20" height="13" rx="5" class="i1"/><rect x="15" y="19" width="20" height="13" rx="5" class="i2"/></svg>',
 'sync': '<svg viewBox="0 0 40 40"><g class="ir"><path d="M30 15a11 11 0 0 0-19-3M10 25a11 11 0 0 0 19 3" fill="none" stroke-width="2.8" stroke-linecap="round"/><path d="M9 7v6h6M31 33v-6h-6" fill="none" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/></g></svg>',
 'key': '<svg viewBox="0 0 40 40"><circle cx="14" cy="20" r="7" class="i1"/><path d="M20 20h15M29 20v5M34 20v4" stroke-width="3" stroke-linecap="round" class="ik"/></svg>',
 'bars': '<svg viewBox="0 0 40 40"><rect x="6" y="20" width="6" height="14" rx="2" class="b1"/><rect x="17" y="12" width="6" height="22" rx="2" class="b2"/><rect x="28" y="6" width="6" height="28" rx="2" class="b3"/></svg>',
}
MOD_IC = {'/bitrix': 'flow', '/bitrix-support': 'pulse', '/bitrix-messengers': 'chat', '/bitrix-integrations': 'sync', '/bitrix-licenses': 'key', '/bitrix-korobka': 'server', '/bi-analitika': 'bars'}
def mods_html():
    return '<div class="mods">' + ''.join(f'<a class="md gl tilt" href="{U(p)}"><div class="ic">{ICON[MOD_IC[p]]}</div><h3>{esc(t)}</h3><p>{esc(s)}</p><b>Подробнее →</b></a>' for p, t, s in BITRIX_MENU) + '</div>'
INDS = ''.join(f'<span>{x}</span>' for x in ['Недвижимость', 'Торговля и дистрибуция', 'Логистика', 'Автодилеры', 'Клиники', 'Обучение', 'Услуги B2B', 'Ритейл'] * 2)
STATS3 = ('<div class="stats gl"><div><div class="n3"><b>8</b></div><span>лет в IT и CRM</span></div><div><div class="n3"><b>1</b><b>5</b><b>0</b><i>+</i></div><span>проектов внедрения</span></div>'
          '<div><div class="n3"><b>7</b></div><span>услуг по Битрикс24</span></div><div><div class="n3"><b>2</b><b>4</b><i>/7</i></div><span>работают ИИ-агенты</span></div></div>'
          f'<div class="mq"><div>{INDS}</div></div>')
def sec_head(ey, h2, sub=''):
    return f'<div class="sec-head"><span class="eyebrow">{esc(ey)}</span><h2>{h2}</h2>' + (f'<p class="sec-sub">{sub}</p>' if sub else '') + '</div>'

home_body = f'''
<section class="hero hero-home">
  <div class="wrap hero-grid">
    <div class="hero-text">
      <span class="eyebrow">Официальный партнёр Битрикс24 в ОАЭ</span>
      <h1>Битрикс24, который <span>продаёт за вас</span></h1>
      <p class="lead">Внедряем и поддерживаем Битрикс24 для компаний в ОАЭ: сделки, звонки, WhatsApp, счета в дирхамах и аналитика в одной системе. А рутину забирают ИИ-агенты</p>
      <p class="answer">MakeBiz Technologies, официальный партнёр Битрикс24, внедряет и поддерживает Битрикс24 для компаний в Дубае и по всем Эмиратам и разрабатывает ИИ-агентов. Стандартная настройка CRM от 10 000 AED, один ИИ-агент от 5 000 AED, работаем на русском и английском.</p>
      <div class="cta-row"><a class="btn" href="#form">Записаться на диагностику →</a><a class="btn btn-ghost" href="#bitrix24">Что внедряем</a></div>
    </div>
    {V_HOME}
  </div>
  <div class="wrap">{STATS3}</div>
</section>

<section class="sec" id="bitrix24"><div class="wrap">
  {sec_head('Битрикс24 · главное направление', 'Всё про Битрикс24 <span>в одной команде</span>', 'От первой настройки CRM до ежедневной поддержки: внедряем, подключаем WhatsApp и учётные системы, помогаем с лицензиями и строим аналитику')}
  {mods_html()}
  <div class="pricebar gl"><span>Стандартная настройка CRM Битрикс24 · <b>от 10 000 AED</b> · поддержка от 1 250 AED в месяц</span><a class="btn" href="{U('/bitrix')}">Смотреть внедрение</a></div>
</div></section>

<section class="sec" style="padding-top:0"><div class="wrap"><div class="aiblk"><div><span class="eyebrow">Второе направление</span>
  <h2 style="margin-top:4px">ИИ-агенты поверх <span>вашего Битрикс24</span></h2><p>Когда CRM настроена, рутину забирают агенты: отвечают клиентам в WhatsApp, разбирают звонки, следят за воронкой и деньгами. Один агент от 5 000 AED</p>
  <a class="btn btn-ghost" href="{U('/ai-agents')}">Подробнее об агентах</a></div>
  <ul><li><a href="{U('/ai-agents/rop')}">ИИ-РОП<small>ответ, если менеджер молчит</small></a></li><li><a href="{U('/ai-agents/zvonki')}">Звонки<small>оценка каждого разговора</small></a></li>
  <li><a href="{U('/ai-agents/hr')}">Найм<small>бот проводит первое собеседование</small></a></li><li><a href="{U('/ai-agents/marketing')}">Маркетинг<small>SEO, GEO и реклама</small></a></li></ul></div></div></section>

<section class="sec" style="padding-top:0"><div class="wrap">{sec_head('Кейсы', 'Проекты, которые <span>ведём годами</span>')}{case_cards(['cdek-b2b','unilin-crm','haval-vector'])}<p class="more"><a href="{U('/keysy')}">Все кейсы →</a></p></div></section>

<section class="sec" style="padding-top:0"><div class="wrap">{sec_head('Как работаем', 'От диагностики <span>до роста прибыли</span>')}{steps([
    ('Диагностика', 'Разбираем процессы и находим, где теряются заявки, деньги и время. Бесплатно, 30-60 минут, в Дубае или по видеосвязи'),
    ('Решение и смета', 'Предлагаем первый шаг с ценой в дирхамах и сроком. Стандартные работы по прайсу, сложные после обследования'),
    ('Внедрение', 'Настраиваем CRM, интеграции и агентов, переносим данные, проверяем на живых сделках'),
    ('Обучение и поддержка', 'Обучаем команду и остаёмся на поддержке пакетами часов'),
])}</div></section>

{contract_block()}
{faq(home_faq)}
{form_block('index', 'Запишитесь на диагностику', 'Покажем, что настроить в Битрикс24 в первую очередь и сколько это стоит. Ответим в течение рабочего дня')}
'''
built.append(page('/', 'index', 'Внедрение Битрикс24 в Дубае и ОАЭ, ИИ-агенты | MakeBiz',
    'Внедрение и поддержка Битрикс24 в Дубае и ОАЭ: WhatsApp, интеграции с Zoho Books и QuickBooks, лицензии, BI-аналитика. ИИ-агенты для продаж. Цены в AED.',
    'home', home_body, [{"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "MakeBiz", "inLanguage": "ru"}],
    [('/', 'Главная')], home_faq))

# ---------- ВНЕДРЕНИЕ БИТРИКС24
bx_faq = [
    ('Сколько стоит внедрение Битрикс24 в ОАЭ?', 'Стандартная настройка CRM Битрикс24 стоит от 10 000 AED. Всё, что сложнее (несколько подразделений, интеграции с учётом, перенос данных, своя разработка), считаем по ставке 200 AED в час и фиксируем смету после короткого обследования. Лицензия Битрикс24 оплачивается отдельно.'),
    ('За сколько можно запустить CRM?', 'Базовый запуск от 14 дней. Интеграции с учётными системами, телефонией и нестандартные процессы занимают больше времени, срок называем после обследования.'),
    ('Входит ли лицензия в стоимость?', f'Нет, лицензия Битрикс24 оплачивается отдельно по тарифу вендора. Облако от {aed(49)} в месяц при оплате за год, подберём тариф под число сотрудников.'),
    ('Учитываете VAT и особенности ОАЭ?', 'Да. Настраиваем валюту AED, VAT 5% в счетах и товарах, реквизиты компаний free zone и материка, выходные в субботу и воскресенье, работу на русском, английском и при необходимости арабском.'),
    ('Облачный или коробочный Битрикс24?', 'Работаем с обоими. Облако быстрее запустить, коробку ставим на ваш сервер, когда данные должны храниться у вас или нужны глубокие доработки.'),
    ('Что будет после запуска?', 'Обучаем команду и остаёмся на поддержке пакетами часов: от 5 часов в месяц за 1 250 AED.'),
]
bx_body = hero('Битрикс24 · внедрение в ОАЭ', 'Внедрение Битрикс24 <span>под ключ в Дубае</span>',
    'Настраиваем Битрикс24 как рабочую систему: сделки, WhatsApp, звонки, счета с VAT и отчёты в одном месте, а у каждого сотрудника понятная роль',
    'MakeBiz Technologies, официальный партнёр Битрикс24 в ОАЭ, внедряет Битрикс24 под ключ для компаний в Дубае и по всем Эмиратам: воронки, бизнес-процессы, WhatsApp и телефония, интеграции с Zoho Books, QuickBooks и Odoo, BI-аналитика и обучение команды. Стандартная настройка от 10 000 AED, базовый запуск от 14 дней.',
    ('#form', 'Обсудить внедрение'), ('#price', 'Цены'), V_BOARD,
    [('от 10 000 AED', 'стандартная настройка'), ('от 14 дней', 'базовый запуск'), ('200 AED/ч', 'работы сверх стандарта'), ('Партнёр', 'Битрикс24')],
    'Рабочее пространство Битрикс24: воронка продаж, переписка и аналитика')
bx_body += section('Знакомо?', 'С этим приходят чаще всего', cards([
    ('Заявки теряются в WhatsApp', 'Клиенты пишут менеджерам на личные номера, часть обращений никто не обрабатывает, история уходит вместе с сотрудником'),
    ('CRM есть, но ей не пользуются', 'Менеджеры ведут клиентов в таблицах и телефонах, данные в портале устаревают'),
    ('Руководитель не видит картину', 'Чтобы понять план, конверсию и деньги в дирхамах, приходится собирать отчёты вручную'),
], 3))
bx_body += section('Что входит в стандартную настройку', 'Стартовый пакет готовит рабочую платформу, команда сразу работает в единой среде', cards([
    ('Профиль и структура', 'Реквизиты компании, валюта AED, часовой пояс Дубая, подразделения, до 20 пользователей'),
    ('Роли и доступы', 'Группы, права и параметры безопасности: каждый видит своё'),
    ('CRM и воронка', 'Модули, справочники, поля компаний и контактов, логика карточек и стадии продаж'),
    ('Счета с VAT 5%', 'Товары и услуги с налогом, шаблон счёта на английском и русском'),
    ('Уведомления', 'Базовые уведомления и логика ролей, чтобы задачи не терялись'),
    ('Обучение', 'Вводное обучение команды на ваших сделках, на русском или английском'),
], 3, numbered=True))
bx_body += section('Как проходит внедрение', '', steps([
    ('Разбор запроса', 'Смотрим текущие процессы и задачи, бесплатно, в Дубае или по видеосвязи'),
    ('Обследование', 'Описываем процессы и будущую архитектуру CRM, готовим смету в AED и план'),
    ('Настройка', 'Воронки, роли, роботы, WhatsApp, интеграции, перенос данных'),
    ('Обучение и поддержка', 'Передаём систему команде и сопровождаем после запуска'),
]), tone='tint')
bx_body += section('Цены', 'Прозрачно: стандарт по прайсу, всё сложнее после обследования', prices([
    ('Стандартная настройка CRM', 'от 10 000 AED', 'разово', ['Структура, роли и доступы', 'CRM, воронка, карточки', 'До 20 пользователей', 'Вводное обучение'], True),
    ('Сложный проект', '200 AED', 'за час работы', ['Предпроектное обследование', 'Несколько подразделений', 'Интеграции и перенос данных', 'Фиксированная смета до старта'], False),
    ('Поддержка после запуска', 'от 1 250 AED', 'в месяц, 5 часов', ['Администрирование и права', 'Доработки процессов', 'Консультации команды', 'Пакеты 5, 10 и 20 часов'], False),
], 'Лицензия Битрикс24 оплачивается отдельно по тарифу вендора. Отдельно оплачиваются платные сервисы, сложные интеграции, перенос данных и своя разработка'), id_='price')
bx_body += section('Всё про Битрикс24 в одной команде', '', '<div class="grid g3 links">' + ''.join(
    f'<a class="lcard tilt" href="{U(p)}"><b>{esc(t)}</b><span>{esc(s)}</span></a>' for p, t, s in BITRIX_MENU[1:]) + '</div>')
from solutions_src import solutions
SOL = solutions('ru')
if SOL:
    bx_body += section('Решения для ОАЭ', 'Битрикс24 под задачи бизнеса в Дубае: отрасли, налоги, звонки, переезд', '<div class="grid g3 links">' + ''.join(
        f'<a class="lcard tilt" href="{U(u)}"><small>{esc(e)}</small><b>{esc(t)}</b><span>{esc(d)}</span></a>' for e, t, d, u in SOL) + '</div>', id_='solutions')
bx_body += section('Под задачу и отрасль', 'Отдельные страницы с составом работ и ценами в AED', '<div class="grid g3 links">' + ''.join(
    f'<a class="lcard tilt" href="{U(p)}"><b>{esc(t)}</b><span>{esc(s_)}</span></a>' for p, t, s_, _, _ in LANDINGS_AE) + '</div>')
bx_body += section('Кейсы', '', case_cards(['cdek-b2b', 'unilin-crm', 'performia-crm']), tone='tint')
bx_body += contract_block() + faq(bx_faq) + form_block('bitrix', 'Обсудим внедрение Битрикс24') + crosslink('ai')
built.append(page('/bitrix', 'bitrix', 'Официальный партнёр Битрикс24 в Дубае: внедрение под ключ | MakeBiz',
    'Официальный партнёр Битрикс24 в ОАЭ: внедрение под ключ, WhatsApp, VAT 5%, интеграции с учётом, обучение. Настройка от 10 000 AED, запуск от 14 дней.',
    'bitrix', bx_body, [service_ld('Внедрение Битрикс24', 'Внедрение CRM Битрикс24 под ключ в ОАЭ', '/bitrix', 10000)],
    [('/', 'Главная'), ('/bitrix', 'Внедрение Битрикс24')], bx_faq))

# ---------- ПОДДЕРЖКА
sp_faq = [
    ('Сколько стоит поддержка Битрикс24?', 'Пакеты часов в месяц: 5 часов за 1 250 AED, 10 часов за 2 300 AED, 20 часов за 4 200 AED. Час сверх пакета 250 AED.'),
    ('Возьмёте портал, который настраивали другие?', 'Да. Начинаем с аудита: смотрим, как настроены процессы, права и интеграции, и говорим, что починить в первую очередь.'),
    ('Что если часы закончились раньше?', 'Докупаете часы по 250 AED или переходите на пакет больше. Перед крупной задачей называем оценку в часах.'),
    ('Как быстро отвечаете?', 'Заявки принимаем в рабочем чате в WhatsApp или Telegram, отвечаем в течение рабочего дня, срочные поломки берём в первую очередь.'),
    ('Видно, на что ушли часы?', 'Да, каждую задачу и потраченное время фиксируем открыто, в конце месяца присылаем отчёт.'),
]
sp_body = hero('Битрикс24 · сопровождение', 'Техподдержка Битрикс24 <span>в Дубае и ОАЭ</span>',
    'Портал уже стоит, но процессы ломаются, сотрудники работают мимо CRM или некому развивать систему? Берём ваш Битрикс24 на поддержку',
    'MakeBiz Technologies ведёт порталы Битрикс24 компаний в ОАЭ после запуска: администрирование, доработки воронок и роботов, интеграции с почтой, телефонией и WhatsApp, обучение сотрудников. Пакеты от 5 часов в месяц за 1 250 AED, час сверх пакета 250 AED.',
    ('#form', 'Получить поддержку'), ('#price', 'Пакеты'), V_TICKETS,
    [('1 250 AED', '5 часов в месяц'), ('250 AED', 'час сверх пакета'), ('1 день', 'ответ на заявку'), ('RU · EN', 'язык работы')], 'Поддержка портала Битрикс24')
sp_body += section('Когда нужна поддержка', '', cards([
    ('Портал живёт своей жизнью', 'Процессы менялись, а система нет. Сделки ведут мимо воронки, отчёты не сходятся'),
    ('Внедряли давно и не у нас', 'Начинаем с аудита и составляем план работ по приоритету'),
    ('Нужны доработки', 'Новые поля, воронки, права, роботы, а руки не доходят'),
    ('Нет своего администратора', 'Штатный специалист дороже пакета часов, а задачи появляются каждую неделю'),
    ('Не работают интеграции', 'Сломались WhatsApp, телефония, почта или обмен с учётной системой'),
    ('Компания растёт', 'Новые отделы, роли и направления продаж, и каждое изменение требует правок в системе'),
], 3))
sp_body += section('Пакеты сопровождения', 'Пакеты по числу часов в месяц. Дополнительный час сверх пакета 250 AED', prices([
    ('5 часов', '1 250 AED', 'в месяц', ['Новые сотрудники и права', 'Правки полей и уведомлений', 'Консультации команды'], False),
    ('10 часов', '2 300 AED', 'в месяц', ['Доработки процессов и отчётов', 'Интеграции', 'Обучение новых людей'], True),
    ('20 часов', '4 200 AED', 'в месяц', ['Несколько направлений', 'Сложные автоматизации', 'Постоянные изменения'], False),
]), id_='price')
sp_body += section('Что входит', '', cards([
    ('Пользователи и права', 'Доступы, роли, структура компании, подключение новых сотрудников'),
    ('CRM', 'Поля, карточки, справочники, логика сделок и контактов'),
    ('Процессы и роботы', 'Доработка бизнес-процессов и автоматизаций под изменения'),
    ('Каналы связи', 'Почта, телефония, WhatsApp и другие мессенджеры: подключение и разбор сбоев'),
    ('Отчёты', 'Отчёты и дашборды под новые вопросы руководителя'),
    ('Консультации', 'Подсказываем, как сделать правильно, обучаем новых сотрудников'),
], 3), tone='tint')
sp_body += contract_block() + faq(sp_faq) + form_block('bitrix-support', 'Возьмём ваш портал на поддержку') + crosslink('ai')
built.append(page('/bitrix-support', 'bitrix-support', 'Техподдержка Битрикс24 в Дубае и ОАЭ: пакеты часов | MakeBiz',
    'Поддержка Битрикс24 для компаний в ОАЭ: администрирование, доработки, WhatsApp, интеграции, обучение. Пакеты 5, 10 и 20 часов от 1 250 AED в месяц.',
    'bitrix', sp_body, [service_ld('Техподдержка Битрикс24', 'Сопровождение портала Битрикс24 пакетами часов', '/bitrix-support', 1250)],
    [('/', 'Главная'), ('/bitrix', 'Битрикс24'), ('/bitrix-support', 'Поддержка')], sp_faq))

# ---------- МЕССЕНДЖЕРЫ
ms_faq = [
    ('Можно ли подключить WhatsApp к Битрикс24?', 'Да. Номер компании подключаем через официальный WhatsApp Business Platform от Meta и коннектор в Контакт-центре Битрикс24. Переписка попадает в карточку сделки, менеджер отвечает прямо из CRM.'),
    ('Сколько стоит подключение?', 'Подключение WhatsApp или другого мессенджера стоит 500 AED. Подписка провайдера и платные сообщения по шаблонам оплачиваются отдельно, расходы считаем до подключения.'),
    ('Какие каналы подключаете?', 'WhatsApp, Telegram, сообщения из соцсетей, онлайн-чат сайта и почту. Все диалоги в одном окне Битрикс24.'),
    ('Почему не через QR-код веб-версии?', 'Такое подключение не официальное, при рассылках и жалобах номер продаж могут заблокировать. Для основного номера используем только официальный API.'),
    ('Сохранится ли переписка, если менеджер уволится?', 'Да, вся история остаётся в карточке клиента в Битрикс24, а не в личном телефоне.'),
]
ms_body = hero('Битрикс24 · мессенджеры', 'WhatsApp и мессенджеры <span>в Битрикс24</span>',
    'В ОАЭ клиент пишет в WhatsApp, а не на почту. Подключаем номер компании к CRM: каждый диалог в карточке клиента, руководитель видит, кто и как быстро ответил',
    'MakeBiz Technologies подключает WhatsApp к Битрикс24 через официальный WhatsApp Business Platform, а также Telegram, соцсети и чат сайта: новое сообщение создаёт лид или сделку, назначает ответственного, история остаётся в компании. Подключение 500 AED.',
    ('#form', 'Подключить WhatsApp'), ('#rules', 'Правила WhatsApp'), V_CHAT,
    [('500 AED', 'подключение канала'), ('1 номер', 'на всю команду'), ('API', 'официально от Meta'), ('100%', 'диалогов в CRM')], 'Переписка из мессенджеров в карточке сделки')
ms_body += section('Что происходит без интеграции', '', cards([
    ('Клиенты в личных телефонах', 'Каждый менеджер переписывается со своего номера. Уходит сотрудник, уходят его клиенты и вся история договорённостей'),
    ('Нет ответа, и никто не знает', 'Сообщение пришло вечером в пятницу, менеджер увидел в понедельник. Руководитель узнаёт, когда клиент уже купил у конкурента'),
    ('История живёт в чате', 'Цены, скидки и сроки обсудили в WhatsApp, а в CRM пусто. Следующий менеджер начинает разговор с нуля'),
], 3))
ms_body += section('Как подключаем', '', cards([
    ('Официальный WhatsApp Business Platform', 'Номер компании подключается к API от Meta через коннектор в Контакт-центре Битрикс24. Провайдера выбираем по объёму переписки и цене сообщений'),
    ('Открытые линии', 'Диалоги распределяются между менеджерами по очереди, по языку или по направлению. Видно время ответа, диалог можно передать коллеге'),
    ('Лид или сделка из первого сообщения', 'Новый номер сразу создаёт лид или сделку с источником WhatsApp, повторный клиент попадает в свою карточку'),
    ('Автоответ вне рабочего времени', 'С учётом выходных в ОАЭ и праздников, на русском, английском и при необходимости арабском'),
    ('Контроль скорости ответа', 'Если на сообщение нет ответа 15 минут, уведомление уходит руководителю'),
    ('Отчёт по каналу', 'Сколько диалогов, сколько без ответа и сколько дошло до сделки'),
], 3), tone='tint')
ms_body += section('Правила WhatsApp, которые надо знать заранее', '', '''<div class="grid g2"><div class="card"><h3>Окно 24 часа</h3><p>Свободным текстом можно отвечать в течение 24 часов после последнего сообщения клиента. Когда окно закрылось, первым пишем только шаблоном, который одобрила Meta: напоминание, статус заказа, счёт</p></div>
<div class="card"><h3>Шаблоны и рассылки</h3><p>Сообщения по шаблонам платные, цену выставляет провайдер. Рассылки только тем, кто дал согласие, иначе растут жалобы и номер ограничивают</p></div></div>''', id_='rules')
ms_body += section('Что делаем мы', 'Подключить канал мало, его надо встроить в продажи', steps([
    ('Номер и провайдер', 'Выбираем номер компании и провайдера API, проходим проверку Meta'),
    ('Открытые линии', 'Очередь, распределение, рабочее время и автоответы'),
    ('CRM и роботы', 'Диалоги связываем с лидами и сделками, ставим контроль времени ответа'),
    ('Шаблоны и запуск', 'Отправляем шаблоны на одобрение, обучаем команду, остаёмся на поддержке'),
]))
ms_body += contract_block() + faq(ms_faq) + form_block('bitrix-messengers', 'Подключим WhatsApp к вашему Битрикс24') + crosslink('ai')
built.append(page('/bitrix-messengers', 'bitrix-messengers', 'WhatsApp в Битрикс24 для бизнеса в ОАЭ | MakeBiz',
    'Подключаем WhatsApp к Битрикс24 через официальный API Meta, а также Telegram, соцсети и чат сайта: переписка в карточке сделки, контроль ответа. От 500 AED.',
    'bitrix', ms_body, [service_ld('WhatsApp и мессенджеры в Битрикс24', 'Подключение WhatsApp Business Platform, Telegram и соцсетей к Битрикс24', '/bitrix-messengers', 500)],
    [('/', 'Главная'), ('/bitrix', 'Битрикс24'), ('/bitrix-messengers', 'Мессенджеры')], ms_faq))

# ---------- ИНТЕГРАЦИИ С УЧЁТОМ
c1_faq = [
    ('С какими учётными системами интегрируете Битрикс24?', 'Чаще всего в ОАЭ это Zoho Books, QuickBooks и Odoo, у части компаний 1С. Также подключаем банковские выписки, склад и внутренние сервисы через API.'),
    ('Какие данные передаются?', 'Клиенты и компании, товары и цены, счета с VAT, оплаты и остатки. Состав и направление обмена определяем на обследовании под ваши процессы.'),
    ('Сколько стоит интеграция?', 'Интеграция Битрикс24 с учётной системой стоит от 10 000 AED. Точная цена зависит от системы и состава обмена, смету фиксируем после обследования.'),
    ('Учитывается VAT 5%?', 'Да. Ставки налога, TRN компаний и счета с VAT передаются между системами одинаково, чтобы бухгалтерия не правила документы вручную.'),
    ('Что если обмен сломается после обновления?', 'Берём интеграцию на поддержку: следим за обменом и чиним в рамках пакета часов.'),
]
c1_body = hero('Битрикс24 · интеграции с учётом', 'Интеграция Битрикс24 <span>с учётной системой</span>',
    'Менеджер видит в CRM цены, остатки и оплаты, а бухгалтерия получает сделки и счета с VAT без ручного ввода',
    'MakeBiz Technologies связывает Битрикс24 с Zoho Books, QuickBooks, Odoo и 1С: клиенты, товары, счета с VAT 5%, оплаты и остатки синхронизируются автоматически, без двойного ввода. Интеграция от 10 000 AED, точную смету фиксируем после обследования.',
    ('#form', 'Обсудить интеграцию'), None, V_SYNC,
    [('Без двойного ввода', 'данные в обе стороны'), ('от 10 000 AED', 'интеграция'), ('VAT 5%', 'в счетах и товарах'), ('Zoho · QuickBooks', 'Odoo · 1С')], 'Обмен данными между Битрикс24 и учётной системой')
c1_body += section('Что даёт интеграция', '', cards([
    ('Нет двойного ввода', 'Клиент, счёт или заказ заводится один раз и появляется в обеих системах'),
    ('Цены и остатки в CRM', 'Менеджер не пишет на склад и в бухгалтерию, всё видно в карточке'),
    ('Оплаты в сделке', 'Поступила оплата, сделка в Битрикс24 сама двигается дальше'),
    ('Счета с VAT', 'Ставки налога и реквизиты не перепечатывают руками'),
    ('Аналитика по деньгам', 'Продажи из CRM и деньги из учёта сводятся в один отчёт'),
    ('Под ваши процессы', 'Состав и направление обмена настраиваем под то, как вы работаете'),
], 3))
c1_body += section('С чем связываем', '', cards([
    ('Zoho Books', 'Клиенты, счета, платежи и товары между Zoho Books и CRM'),
    ('QuickBooks', 'Счета, оплаты и клиенты для компаний на QuickBooks Online'),
    ('Odoo', 'Продажи, склад и учёт для компаний, где Odoo уже работает как ERP'),
    ('1С и банки', 'Обмен с 1С и загрузка банковских выписок для сверки оплат'),
], 4), tone='tint')
c1_body += section('Как подключаем', '', steps([
    ('Обследование', 'Смотрим учётную систему, процессы и что нужно передавать'),
    ('Схема обмена', 'Описываем объекты, направления и правила, фиксируем смету в AED'),
    ('Настройка и тест', 'Настраиваем обмен, проверяем на тестовых и реальных документах'),
    ('Запуск и поддержка', 'Включаем в работу и следим за обменом на поддержке'),
]))
c1_body += section('Кейсы', '', case_cards(['unilin-crm', 'performia-crm', 'cdek-b2b']), tone='tint')
c1_body += contract_block() + faq(c1_faq) + form_block('bitrix-integrations', 'Свяжем Битрикс24 с вашим учётом') + crosslink('ai')
built.append(page('/bitrix-integrations', 'bitrix-integrations', 'Интеграция Битрикс24 с Zoho Books, QuickBooks, Odoo | MakeBiz',
    'Интеграция Битрикс24 с Zoho Books, QuickBooks, Odoo и 1С для компаний в ОАЭ: клиенты, счета с VAT 5%, оплаты и остатки без двойного ввода. От 10 000 AED.',
    'bitrix', c1_body, [service_ld('Интеграция Битрикс24 с учётными системами', 'Обмен данными между Битрикс24 и Zoho Books, QuickBooks, Odoo, 1С', '/bitrix-integrations', 10000)],
    [('/', 'Главная'), ('/bitrix', 'Битрикс24'), ('/bitrix-integrations', 'Интеграции с учётом')], c1_faq))

# ---------- ЛИЦЕНЗИИ (цены bitrix24.ae, USD -> AED по курсу 3.6725)
PRICE_DATE = '23 октября 2026'
def lic(usd): return f'{aed(usd)}'
def nb(x): return re.sub(r'(\d) (?=\d{3})', '\\1\u00a0', x)
CLOUD = [
    ('Basic', f'{lic(49)}', f'в месяц при оплате за год (${49}) · {lic(69)} помесячно (${69})', ['5 пользователей', 'CRM, задачи, чаты, диск', 'Сайты и онлайн-запись'], False),
    ('Standard', f'{lic(99)}', f'в месяц при оплате за год (${99}) · {lic(144)} помесячно (${144})', ['50 пользователей', 'Маркетинг, документы онлайн', 'Всё из Basic'], False),
    ('Professional', f'{lic(199)}', f'в месяц при оплате за год (${199}) · {lic(289)} помесячно (${289})', ['100 пользователей', 'Автоматизация продаж и процессов', 'Сквозная аналитика'], True),
    ('Enterprise', f'от {lic(399)}', f'в месяц при оплате за год (от ${399}) · от {lic(579)} помесячно', ['от 250 до 10 000 пользователей', 'Филиалы и холдинг', 'Расширенная безопасность'], False),
]
ENT = [('250', 399, 579), ('500', 639, 919), ('1 000', 799, 1149), ('10 000', 7999, 11499)]
BOX = [
    ('Business', '50 (варианты на 100, 250 и 500)', f'{lic(3590)} ($3 590)'),
    ('Enterprise', 'от 1 000', f'{lic(24990)} ($24 990)'),
]
def ent_table():
    rows = ''.join(f'<tr><td><b>Enterprise {u}</b></td><td class="pt-p">{lic(a)} <small>(${a:,})</small></td><td>{lic(m)} <small>(${m:,})</small></td></tr>'.replace(',', ' ') for u, a, m in ENT)
    return (f'<div class="ptw gl"><table class="ptab"><thead><tr><th>Тариф</th><th>В месяц при оплате за год</th><th>Помесячно</th></tr></thead><tbody>{rows}</tbody></table></div>')
def box_table():
    rows = ''.join(f'<tr><td><b>{esc(n)}</b></td><td>{esc(u)}</td><td class="pt-p">{esc(p)}</td></tr>' for n, u, p in BOX)
    return (f'<div class="ptw gl"><table class="ptab"><thead><tr><th>Редакция</th><th>Пользователей</th><th>Лицензия на год</th></tr></thead><tbody>{rows}</tbody></table></div>'
            f'<p class="note">Цены вендора с bitrix24.ae на {PRICE_DATE} в долларах США, пересчёт в AED по курсу 3,6725. Цены на варианты Business для 100, 250 и 500 пользователей и точную сумму фиксируем в счёте</p>')
lc_faq = [
    ('Сколько стоит Битрикс24 в ОАЭ?', f'По ценам вендора с bitrix24.ae на {PRICE_DATE} при оплате за год: Basic {lic(49)} в месяц, Standard {lic(99)}, Professional {lic(199)}, Enterprise от {lic(399)}. Есть бесплатный тариф на 1-2 пользователя. Коробочная версия Business {lic(3590)} в год.'),
    ('В какой валюте цены?', 'Вендор публикует цены для ОАЭ в долларах США. Мы показываем их в дирхамах по курсу 3,6725 и рядом цену в долларах, точную сумму фиксируем в счёте.'),
    ('Сколько экономит оплата за год?', 'При оплате облачного тарифа за год цена в месяц примерно на 30% ниже, чем при помесячной оплате.'),
    ('Какой тариф выбрать?', 'Для отдела продаж до 5 человек хватает Basic. Для компании до 50 человек Standard. Если нужна автоматизация процессов и сквозная аналитика, Professional. Филиалы и сотни сотрудников: Enterprise или коробка.'),
    ('Облако или коробка?', 'Облако быстрее запустить и не нужно держать сервер. Коробку ставят, когда данные должны храниться у себя, нужна глубокая доработка кода или пользователей много. Подробно на странице про коробочный Битрикс24.'),
    ('Поможете с продлением и сменой тарифа?', 'Да, напомним о продлении заранее и поможем перейти на тариф выше или ниже без потери данных.'),
]
lc_body = hero('Битрикс24 · лицензии и цены', f'Цены Битрикс24 в ОАЭ <span>от {lic(49).replace(" ", "&nbsp;")} в&nbsp;месяц</span>',
    'Подберём тариф под ваши задачи, поможем оформить покупку и продлить вовремя, чтобы портал не встал',
    f'Цены на облачный Битрикс24 для ОАЭ по данным bitrix24.ae на {PRICE_DATE}: Basic {lic(49)}, Standard {lic(99)}, Professional {lic(199)} в месяц при оплате за год, Enterprise от {lic(399)}. Коробочная версия от {lic(3590)} в год. MakeBiz Technologies как официальный партнёр Битрикс24 помогает подобрать тариф, оформить и продлить лицензию.',
    ('#form', 'Подобрать тариф'), ('#ceny', 'Смотреть цены'), V_LIC,
    [(f'{lic(49)}', 'облако в месяц'), ('−30%', 'при оплате за год'), (f'{lic(3590)}', 'коробка в год'), ('USD → AED', 'курс 3,6725')], 'Лицензия Битрикс24')
lc_body += section('Цены на облачный Битрикс24', f'Цены вендора на {PRICE_DATE}, за всех пользователей тарифа. Есть бесплатный тариф Free на 1-2 пользователя', prices(CLOUD, 'Цены с bitrix24.ae в долларах США, в дирхамах по курсу 3,6725. Точную сумму и актуальные акции фиксируем в счёте'), id_='ceny')
lc_body += section('Тарифы Enterprise', 'Для филиалов, холдингов и сотен сотрудников', ent_table(), tone='tint')
lc_body += section('Цены на коробочный Битрикс24', 'Битрикс24 на вашем сервере: данные у вас, доступ к коду и доработкам', box_table() +
    f'<p class="more"><a href="{U("/bitrix-korobka")}">Внедрение коробочного Битрикс24 →</a></p>')
lc_body += section('Что делаем', '', cards([
    ('Подбор тарифа', 'Считаем пользователей и нужные функции, чтобы не переплачивать'),
    ('Оформление', 'Помогаем купить лицензию на компанию и разобраться с оплатой'),
    ('Продление', 'Напоминаем заранее, чтобы портал не перешёл на ограниченный режим'),
    ('Смена тарифа', 'Переход выше или ниже без потери данных и настроек'),
    ('Облако или коробка', 'Помогаем выбрать и, если нужно, переносим портал'),
    ('Сразу настройка', 'Лицензию можно оформить вместе со стандартной настройкой CRM от 10 000 AED'),
], 3), tone='tint')
lc_body += contract_block() + faq(lc_faq) + form_block('bitrix-licenses', 'Подберём тариф Битрикс24', 'Напишите, сколько сотрудников будет в портале и что нужно, пришлём подбор тарифа') + crosslink('ai')
built.append(page('/bitrix-licenses', 'bitrix-licenses', 'Цены Битрикс24 в ОАЭ 2026: тарифы в AED | MakeBiz',
    f'Цены Битрикс24 в ОАЭ: облако от {lic(49)} в месяц, Enterprise от {lic(399)}, коробка от {lic(3590)} в год. Цены bitrix24.ae в AED и USD, подбор тарифа и продление.',
    'bitrix', lc_body, [service_ld('Лицензии Битрикс24', 'Подбор, оформление и продление лицензий Битрикс24 в ОАЭ', '/bitrix-licenses', 180),
        {"@type": "OfferCatalog", "name": "Тарифы Битрикс24 в ОАЭ", "itemListElement": [
            {"@type": "Offer", "name": 'Битрикс24 ' + n, "price": str(round(u * USD_AED)), "priceCurrency": "AED", "seller": {"@id": SITE + "/#organization"}} for n, u in [('Basic', 49), ('Standard', 99), ('Professional', 199), ('Enterprise 250', 399), ('Business (коробка, год)', 3590), ('Enterprise (коробка, год)', 24990)]]}],
    [('/', 'Главная'), ('/bitrix', 'Битрикс24'), ('/bitrix-licenses', 'Лицензии и цены')], lc_faq))

# ---------- КОРОБКА
kb_faq = [
    ('Чем коробочный Битрикс24 отличается от облачного?', 'Коробка ставится на ваш сервер или в ваш дата-центр: данные хранятся у вас, есть доступ к коду, можно глубоко дорабатывать систему и подключать внутренние сервисы. Облако работает на серверах Битрикс24, его быстрее запустить, но доработки ограничены приложениями.'),
    ('Сколько стоит коробочный Битрикс24?', f'Лицензия по ценам bitrix24.ae на {PRICE_DATE}: Business на 50 пользователей {lic(3590)} в год ($3 590), есть варианты на 100, 250 и 500 пользователей. Enterprise от 1 000 пользователей {lic(24990)} ($24 990). Внедрение считаем по ставке 200 AED в час, смету фиксируем после обследования.'),
    ('Какой сервер нужен?', 'Свой физический сервер, виртуальная машина в облаке или дата-центр в ОАЭ. Подберём конфигурацию под число пользователей, развернём окружение и настроим резервное копирование.'),
    ('Можно перенести облачный портал в коробку?', 'Да. Переносим CRM, задачи, пользователей и файлы, настраиваем заново то, что не переносится автоматически, и проверяем данные до переключения команды.'),
    ('Кто будет обновлять и обслуживать коробку?', 'Можем взять на поддержку: обновления, резервные копии, мониторинг, безопасность и доработки. Пакеты от 1 250 AED в месяц.'),
]
kb_body = hero('Битрикс24 · на своём сервере', 'Коробочный Битрикс24: <span>внедрение на вашем сервере</span>',
    'Данные хранятся у вас, система дорабатывается под любые процессы и связывается с внутренними сервисами. Ставим, переносим, дорабатываем и сопровождаем',
    f'MakeBiz Technologies внедряет коробочный Битрикс24 на сервере компании в ОАЭ: подбираем редакцию и сервер, разворачиваем систему, переносим данные из облака или другой CRM, дорабатываем под процессы, интегрируем с учётными системами и берём на поддержку. Лицензия от {lic(3590)} в год, работы 200 AED в час.',
    ('#form', 'Обсудить коробку'), ('#ceny', 'Цены на лицензии'), V_BOX,
    [('Свой сервер', 'данные у вас'), ('Код', 'доработки без ограничений'), (f'{lic(3590)}', 'лицензия в год'), ('СДЭК, Unilin', 'коробка в работе')], 'Коробочный Битрикс24 на сервере')
kb_body += section('Когда нужна коробка', 'Если узнаёте себя хотя бы в двух пунктах, облако будет тесным', cards([
    ('Данные только у себя', 'Политика безопасности требует хранить клиентов и документы в своём контуре или в ОАЭ'),
    ('Нужны доработки кода', 'Свои модули, нестандартные сущности, логика, которую не сделать приложением'),
    ('Много внутренних систем', 'Своя ERP, учёт, телефония и сервисы, с которыми нужен глубокий обмен'),
    ('Сотни сотрудников', 'При большом числе пользователей лицензия на коробку выходит выгоднее подписки'),
    ('Филиалы и холдинг', 'Компании в free zone и на материке, разные юрлица и права в одной системе'),
    ('Контроль обновлений', 'Вы сами решаете, когда обновлять систему'),
], 3))
kb_body += section('Облако или коробка', '', '''<div class="vs"><div class="vs-col"><h3>Облако</h3><ul><li>Запуск за день, сервер не нужен</li><li>Обновления и резервные копии делает Битрикс24</li><li>Доработки через приложения и вебхуки</li><li>Подписка помесячно или за год</li></ul></div>
<div class="vs-col vs-good"><h3>Коробка</h3><ul><li>Ваш сервер или дата-центр, данные в своём контуре</li><li>Доступ к коду и доработки любой глубины</li><li>Прямые интеграции с внутренними системами</li><li>Лицензия на год, выгоднее при большом штате</li></ul></div></div>''', tone='tint')
kb_body += section('Что делаем', '', cards([
    ('Подбор редакции и сервера', 'Считаем пользователей и нагрузку, выбираем редакцию и конфигурацию сервера'),
    ('Развёртывание', 'Устанавливаем Битрикс24, настраиваем окружение, SSL, почту, резервное копирование'),
    ('Перенос данных', 'Из облачного Битрикс24, Zoho CRM, HubSpot или таблиц: клиенты, сделки, задачи, файлы'),
    ('Настройка и доработки', 'Воронки, права, бизнес-процессы, свои модули и доработки кода'),
    ('Интеграции', 'Zoho Books, QuickBooks, Odoo, 1С, телефония, WhatsApp и BI'),
    ('Поддержка', 'Обновления, мониторинг, безопасность и доработки по пакету часов'),
], 3))
kb_body += section('Цены на лицензии коробки', f'Цены вендора на {PRICE_DATE}', box_table(), id_='ceny', tone='tint')
kb_body += section('Как внедряем', '', steps([
    ('Обследование', 'Разбираем процессы, требования безопасности и интеграции, фиксируем смету'),
    ('Сервер и установка', 'Разворачиваем коробку на вашем сервере или в дата-центре'),
    ('Перенос и настройка', 'Переносим данные, настраиваем CRM, процессы и права, делаем доработки'),
    ('Запуск и поддержка', 'Обучаем команду, запускаем и берём систему на сопровождение'),
]))
kb_body += section('Кейсы на коробке', '', case_cards(['cdek-b2b', 'unilin-crm']))
kb_body += contract_block() + faq(kb_faq) + form_block('bitrix-korobka', 'Обсудим коробочный Битрикс24', 'Напишите, сколько пользователей и какие системы нужно связать, предложим редакцию, сервер и смету') + crosslink('ai')
built.append(page('/bitrix-korobka', 'bitrix-korobka', 'Коробочный Битрикс24 в ОАЭ: внедрение на своём сервере | MakeBiz',
    f'Коробочный Битрикс24 на сервере компании в ОАЭ: подбор редакции, установка, перенос из облака, доработки, интеграции и поддержка. Лицензия от {lic(3590)} в год.',
    'bitrix', kb_body, [service_ld('Внедрение коробочного Битрикс24', 'Установка, доработка и поддержка Битрикс24 на сервере клиента', '/bitrix-korobka', 13184)],
    [('/', 'Главная'), ('/bitrix', 'Битрикс24'), ('/bitrix-korobka', 'Коробочный Битрикс24')], kb_faq))

# ---------- витрина кабинета MakeBiz (скрины из видео, демо-данные)
SHOT_ALT = {
 'ai-chat': 'Чаты: подсказка РОПа, готовый ответ клиенту от ИИ-агента',
 'bi-puls': 'Пульс компании: доходы, прибыль, расходы и активы по направлениям',
 'bi-sales': 'Отдел продаж: лиды, оплаты, касания и скорость ответа по периодам',
 'bi-fin': 'Финансы: оборот, прибыль, рентабельность и запас денег',
 'bi-direct': 'Маркетинг: расход, клики и цена клика по рекламным кампаниям',
 'hr-obzor': 'Найм: отклики с job-площадок, переход в бота, средний балл и наймы',
 'hr-tests': 'Найм: тесты бота, распределение баллов и совпадение с решениями руководителя',
 'hr-kand': 'Найм: список кандидатов с баллом бота, типажом мотивации и решением',
 'calls-pok': 'Звонки: средний балл разговоров по дням и топ сотрудников',
 'calls-analytics': 'Звонки: топ вопросов клиентов и топ возражений',
 'calls-reco': 'Звонки: рекомендации по сотрудникам и отчёт по компании',
 'zak': 'Закупки: карта поставщиков по цене и надёжности',
}
def shots(keys, label):
    main = keys[0]
    def lab(k): return SHOT_ALT[k].split(':')[0]
    TABS = {'ai-chat': 'Чаты', 'rop-razbor': 'Разбор переписок', 'rop-plan': 'План продаж', 'bi-sales': 'Отдел продаж', 'bi-puls': 'Пульс компании',
            'bi-fin': 'Финансы', 'bi-direct': 'Реклама', 'mk-search': 'Поиск', 'mk-seo': 'SEO по сайтам', 'mk-geo': 'AI-видимость', 'mk-queries': 'Поисковые запросы',
            'hr-obzor': 'Найм · обзор', 'hr-kand': 'Кандидаты', 'hr-tests': 'Тесты бота', 'calls-analytics': 'Вопросы и возражения', 'calls-pok': 'Средний балл',
            'calls-reco': 'Рекомендации', 'zak': 'Карта поставщиков', 'zak-obzor': 'Закупки · обзор', 'svyaz-today': 'Сегодня', 'svyaz-set': 'Картина сети'}
    th = ''.join(f'<button type="button" class="sh-t{" on" if i==0 else ""}" data-src="{U("/img/agents/"+k+".webp")}" data-alt="{esc(SHOT_ALT[k])}">{esc(TABS.get(k, lab(k)))}</button>' for i, k in enumerate(keys)) if len(keys) > 1 else ''
    return (f'<figure class="shot"><div class="shot-bar"><i></i><i></i><i></i><span>{esc(label)}</span><em>демо-данные</em></div>'
            f'<img src="{U("/img/agents/"+main+".webp")}" alt="{esc(SHOT_ALT[main])}" width="1400" height="685" loading="lazy" decoding="async">'
            f'{"<div class=sh-tabs>"+th+"</div>" if th else ""}</figure>')
def feature(id_, ey, title, lead, bullets, keys, label, reverse=False, extra=''):
    li = ''.join(f'<li>{b}</li>' for b in bullets)
    return (f'<section class="sec feat-sec" id="{id_}"><div class="wrap feat{" feat-r" if reverse else ""}">'
            f'<div class="feat-tx"><div class="eyebrow">{esc(ey)}</div><h2>{title}</h2><p class="sec-sub">{lead}</p><ul class="ticks">{li}</ul>{extra}</div>'
            f'<div class="feat-vis">{shots(keys, label)}</div></div></section>')
VIDEO_LD = {"@type": "VideoObject", "name": "ИИ-агенты MakeBiz: как компанией управляют агенты",
    "description": "Обзор кабинета MakeBiz: пульс компании, чаты с подсказками РОПа, разбор переписок, воронка продаж, финансы, маркетинг, найм, речевая аналитика звонков и закупки.",
    "thumbnailUrl": [SITE + U('/media/agents-poster.jpg')], "uploadDate": "2026-10-22", "duration": "PT3M10S",
    "contentUrl": SITE + U('/media/agents.mp4'), "inLanguage": "ru", "publisher": {"@id": SITE + "/#organization"}}
def video_block():
    return (f'<section class="sec" id="video"><div class="wrap"><div class="sec-head"><div class="eyebrow">Видео · 3 минуты</div><h2>Кабинет, в котором <span>работают наши агенты</span></h2>'
            f'<p class="sec-sub">Так выглядит управление MakeBiz изнутри: деньги, продажи, звонки, найм, маркетинг и закупки в одной системе. Это то, что мы внедряем клиентам</p></div>'
            f'<div class="vid"><video controls preload="none" playsinline poster="{U("/media/agents-poster.jpg")}" width="1280" height="720">'
            f'<source src="{U("/media/agents.mp4")}" type="video/mp4"></video></div>'
            f'<div class="vid-links"><a href="https://www.youtube.com/watch?v=DTJ6tVOx6dg" target="_blank" rel="noopener">HR-блок: подбор от отклика на hh.ru до выхода на работу · 2:48</a>'
            f'<a href="https://www.youtube.com/watch?v=HknIeajCo18" target="_blank" rel="noopener">Речевая аналитика звонков для роста продаж</a></div></div></section>')

# ---------- BI
bi_faq = [
    ('Что такое BI-аналитика в Битрикс24?', 'Это дашборды для руководителя на данных из CRM и других систем: продажи, воронка, работа менеджеров, деньги в дирхамах. Строим их во встроенном BI-конструкторе Битрикс24 или во внешней BI-системе.'),
    ('Какие источники можно подключить?', 'Битрикс24, Zoho Books, QuickBooks, Odoo, 1С, телефонию, Google Ads, Meta, Google Analytics, таблицы и банковские выписки. Состав определяем под ваши вопросы.'),
    ('Сколько стоит BI-аналитика?', 'BI-аналитика стоит от 1 000 AED. Итоговая цена зависит от числа источников и показателей, смету фиксируем после того, как согласуем список показателей.'),
    ('Цифры будут правильными?', 'Начинаем с проверки данных в CRM: дашборд показывает правду, только если в системе нет мусора. Если нужно, сначала наводим порядок в карточках и стадиях.'),
]
bi_body = hero('Битрикс24 · BI-аналитика', 'BI-аналитика <span>для руководителя</span>',
    'Продажи, воронка, менеджеры и деньги на одном экране. Цифры из CRM и учётных систем, а не из ручных таблиц',
    'MakeBiz Technologies строит BI-дашборды для компаний в ОАЭ на данных Битрикс24, учётных систем, телефонии и рекламы: руководитель видит план, конверсию, работу каждого менеджера и деньги в дирхамах в реальном времени. BI-аналитика от 1 000 AED, смета после согласования показателей.',
    ('#form', 'Обсудить дашборд'), None, V_BI,
    [('1 экран', 'вместо отчётов'), ('CRM + учёт', 'и другие источники'), ('от 1 000 AED', 'BI-аналитика'), ('AED', 'деньги в дирхамах')], 'Дашборды BI-аналитики')
bi_body += section('Что видно в дашбордах', '', cards([
    ('Продажи и план', 'Выручка, план и факт по отделам и менеджерам'),
    ('Воронка', 'Конверсия по стадиям и где застревают сделки'),
    ('Менеджеры', 'Скорость ответа, активность, звонки и результат'),
    ('Деньги', 'Оплаты, дебиторка и VAT из учётной системы'),
    ('Реклама', 'Откуда приходят клиенты и какие каналы окупаются'),
    ('Операции', 'Загрузка, сроки и качество работы по вашим процессам'),
], 3))
bi_body += feature('pult', 'Пример из нашей компании', 'Пульс компании <span>на одном экране</span>',
    'Мы сами управляем MakeBiz через такой кабинет: данные идут из Битрикс24, банков, учётной системы, телефонии и рекламы и обновляются без ручных таблиц',
    ['Доходы, прибыль, расходы и активы по каждому направлению и проекту',
     'Отдел продаж: лиды, оплаты, касания, скорость ответа и провалы по неделям',
     'Финансы: оборот, рентабельность, дивиденды и запас денег в месяцах',
     'Маркетинг: расход, клики и цена клика по кампаниям, SEO и AI-видимость',
     'ИИ-агент читает те же цифры и сам подсвечивает риски'],
    ['bi-puls', 'bi-sales', 'bi-fin', 'bi-direct'], 'Пульс компании')
bi_body += section('Как делаем', '', steps([
    ('Вопросы руководителя', 'Фиксируем, какие решения должен поддерживать дашборд'),
    ('Данные', 'Проверяем источники, наводим порядок в CRM, если нужно'),
    ('Дашборды', 'Собираем показатели и срезы, проверяем цифры с вами'),
    ('Развитие', 'Добавляем показатели по мере роста, обучаем команду'),
]), tone='tint')
bi_body += section('Кейсы', '', case_cards(['performia-crm', 'unilin-crm', 'apartika-crm']))
bi_body += contract_block() + faq(bi_faq) + form_block('bi-analitika', 'Соберём дашборд под ваши вопросы') + crosslink('ai')
built.append(page('/bi-analitika', 'bi-analitika', 'BI-аналитика для Битрикс24 в ОАЭ: дашборды руководителя | MakeBiz',
    'BI-аналитика для компаний в ОАЭ от 1 000 AED: дашборды на данных Битрикс24, учётных систем, телефонии и рекламы. Продажи, воронка, менеджеры и деньги на одном экране.',
    'bitrix', bi_body, [service_ld('BI-аналитика для Битрикс24', 'Дашборды для руководителя на данных CRM и учётных систем', '/bi-analitika', 1000)],
    [('/', 'Главная'), ('/bitrix', 'Битрикс24'), ('/bi-analitika', 'BI-аналитика')], bi_faq))

# ---------- ИИ-АГЕНТЫ: хаб + страница на каждого агента
SHOT_ALT.update({
 'rop-razbor': 'Разбор переписок: где ошиблись, как надо было и что сделать',
 'rop-plan': 'Продажи: план месяца, лиды, сделки и оплаты по менеджерам',
 'svyaz-today': 'Связной: ждут ответа, шаги на сегодня, горячие и новые диалоги',
 'svyaz-set': 'Связной: картина сети, кто есть кто и теплота каждого контакта',
 'mk-search': 'Поиск: показы и клики в поисковиках по каждому сайту',
 'mk-seo': 'SEO по сайтам: страницы в поиске, показы, клики и новые страницы',
 'mk-geo': 'AI-видимость: как часто сайт цитируют ChatGPT, Perplexity и другие ассистенты',
 'mk-queries': 'Реклама: поисковые запросы, расход, клики и цена клика',
 'zak-obzor': 'Закупки: экономия, процедуры, объём и работа агента',
})
AGENTS = [
 dict(slug='rop', name='ИИ-РОП', short='Продажи и переписки',
  sub='Подсказки в каждом диалоге, разбор переписок, контроль плана',
  title='ИИ-агент РОП: контроль отдела продаж и переписок в Битрикс24 | MakeBiz',
  desc='ИИ-агент руководитель отдела продаж: готовит ответы клиентам, подхватывает диалог, если менеджер молчит, разбирает переписки и следит за планом в Битрикс24.',
  h1='ИИ-РОП, который <span>не пропускает ни одного клиента</span>',
  lead='Агент видит все переписки и сделки, подсказывает менеджеру ответ, сам отвечает, если никто не отреагировал, и каждое утро разбирает ошибки отдела',
  answer='ИИ-РОП от MakeBiz работает внутри Битрикс24 и мессенджеров: готовит ответ клиенту прямо в окне чата, через 15 минут тишины сам подхватывает диалог, разбирает переписки менеджеров и следит за планом продаж.',
  chips=[('15 минут', 'и агент отвечает сам'), ('Каждое утро', 'разбор переписок'), ('План', 'по каждому менеджеру'), ('Битрикс24', 'всё в сделке')],
  feats=[('Подсказка в каждом диалоге', 'Готовый ответ с ценой в AED и следующим шагом в окне чата: вставить, переписать короче или мягче одной кнопкой'),
         ('Подхватывает диалог', 'Если менеджер не ответил 15 минут, агент отвечает клиенту сам и ставит задачу ответственному'),
         ('Очередь «ждут ответа»', 'Видно, кто из клиентов ждёт и сколько минут, по всем каналам сразу'),
         ('Разбор переписок', 'Каждое утро: где ошиблись, как надо было ответить, каких лидов закрыли рано и кого вернуть'),
         ('План и воронка', 'План месяца, лиды, сделки и оплаты по каждому менеджеру, какие сделки закрыть первыми'),
         ('Кому позвонить сегодня', 'Список клиентов, с которыми пора связаться, с причиной и подсказкой, что сказать')],
  ticks=['WhatsApp, Telegram, соцсети, почта и чаты сайта в одной очереди', 'Оценка каждой переписки и типовые ошибки менеджеров', 'План и факт по менеджерам и стадиям воронки', 'Всё пишется в сделку Битрикс24'],
  shots=['ai-chat', 'rop-razbor', 'rop-plan', 'bi-sales'],
  faq=[('На каком языке агент отвечает клиентам?', 'На языке клиента: английском, русском, при необходимости арабском. Тон и правила ответа задаются под вашу компанию.'),
       ('ИИ-РОП заменит руководителя отдела продаж?', 'Нет, он забирает рутину: следит за скоростью ответа, разбирает переписки и подсказывает. Решения и люди остаются за руководителем.'),
       ('С какими каналами работает?', 'WhatsApp, Telegram, соцсети, почта и чаты сайта, подключённые к Битрикс24. Другие каналы подключаем по задаче.'),
       ('Агент сам пишет клиентам?', 'Только по правилам, которые вы задали: например, если менеджер молчит 15 минут. Всё, что агент написал, видно в сделке.')]),
 dict(slug='svyaznoy', name='Связной', short='Контакты и отношения',
  sub='Кто ждёт ответа, с кем пора связаться, картина всех контактов',
  title='ИИ-агент Связной: контакты и отношения с клиентами | MakeBiz',
  desc='ИИ-агент Связной следит за всеми контактами: кто ждёт ответа, с кем пора связаться, кто горячий, а кто остывает. Картина сети и теплота каждого контакта.',
  h1='Связной: агент, который <span>помнит каждого человека</span>',
  lead='Агент держит в голове все ваши контакты: клиентов, партнёров, подрядчиков. Напоминает, кому ответить и с кем пора связаться, и показывает, какие связи остывают',
  answer='ИИ-агент Связной от MakeBiz собирает контакты из WhatsApp, Telegram, CRM и почты, показывает, кто ждёт ответа и какие шаги запланированы на сегодня, и оценивает теплоту каждого контакта, чтобы связи не терялись.',
  chips=[('Ждут ответа', 'видно сразу'), ('Шаги', 'на сегодня'), ('Теплота', 'каждого контакта'), ('Telegram', 'и CRM')],
  feats=[('Ждут ответа', 'Кто написал и не получил ответ, сколько ждёт и что ему ответить'),
         ('Шаги на сегодня', 'Договорились созвониться или прислать КП: агент напомнит в нужный день'),
         ('Горячие и новые', 'Новые диалоги и контакты, которые сейчас готовы к разговору'),
         ('Картина сети', 'Кто есть кто: клиенты, партнёры, подрядчики, личные связи и спам'),
         ('Теплота контакта', 'Холодный, тёплый, близкий: видно, какие отношения остывают'),
         ('Утренний разбор', 'Короткая сводка в Telegram: что важно сегодня и кого нельзя забыть')],
  ticks=['Контакты из WhatsApp, Telegram, CRM и почты в одной картине', 'Статус и теплота каждой карточки', 'Даты рождения и поводы для касания', 'Сделки и лиды создаются в Битрикс24 одной кнопкой'],
  shots=['svyaz-today', 'svyaz-set'],
  faq=[('Чем Связной отличается от CRM?', 'CRM хранит сделки. Связной следит за людьми: кто ждёт ответа, с кем давно не общались, какие договорённости на сегодня, и передаёт в CRM то, что стало сделкой.'),
       ('Откуда агент берёт контакты?', 'Из WhatsApp, Telegram, Битрикс24 и почты. Состав источников определяем на старте.'),
       ('Кому это нужно?', 'Собственникам, руководителям и продажникам, у которых сотни контактов и договорённостей, которые нельзя терять.')]),
 dict(slug='zvonki', name='Звонки', short='Речевая аналитика',
  sub='Оценка каждого разговора, возражения, рекомендации',
  title='Речевая аналитика звонков с ИИ: оценка разговоров и скриптов | MakeBiz',
  desc='ИИ-агент слушает все звонки отдела продаж: расшифровка, оценка разговора, этапы скрипта, топ вопросов и возражений, рекомендации по каждому менеджеру.',
  h1='Речевая аналитика: <span>каждый звонок оценён</span>',
  lead='Система слушает все звонки и показывает, где менеджеры теряют клиентов, какие возражения повторяются и какие скрипты не работают',
  answer='Речевая аналитика от MakeBiz расшифровывает и оценивает каждый звонок отдела продаж: прохождение этапов скрипта, эмоции, вопросы и возражения клиентов. Руководитель видит средний балл по менеджерам и получает рекомендации, кого обучить и что изменить в скрипте. От 1 000 AED в месяц за 5 000 минут.',
  chips=[('100%', 'звонков проверено'), ('1 000 AED', 'в месяц, 5 000 минут'), ('Возражения', 'топ по компании'), ('EN · RU', 'языки звонков')],
  feats=[('Оценка разговора', 'Балл за каждый звонок и прохождение этапов: приветствие, выявление потребности, презентация, работа с возражениями, договорённость'),
         ('Детализация', 'Расшифровка, что сделано хорошо, где ошибка и конкретная подсказка менеджеру'),
         ('Вопросы и возражения', 'Топ вопросов клиентов и топ возражений по всем звонкам: что дописать в скрипт'),
         ('Динамика', 'Средний балл по дням и менеджерам, сравнение с прошлым периодом'),
         ('Рекомендации', 'Кому нужно обучение, кому контроль, где падает качество'),
         ('Отчёт по компании', 'Сколько звонков проверено, сколько проблемных, вероятность продажи')],
  ticks=['Подключаем телефонию и записи из Битрикс24', 'Критерии оценки под ваш скрипт', 'Итог разговора и оценка в карточке сделки', 'Сотни тысяч минут в месяц без ручной прослушки'],
  shots=['calls-analytics', 'calls-pok', 'calls-reco'], video=('https://www.youtube.com/watch?v=HknIeajCo18', 'Речевая аналитика для роста продаж'),
  faq=[('Сколько стоит речевая аналитика?', 'Помесячно по объёму звонков: 1 000 AED в месяц за 5 000 минут, 1 700 AED за 10 000 минут, от 4 000 AED от 30 000 минут. Подключение бесплатно.'),
       ('С какой телефонией работает?', 'С телефонией, подключённой к Битрикс24, и с большинством облачных АТС, которые отдают записи разговоров.'),
       ('По каким критериям оцениваются звонки?', 'По вашему скрипту: этапы, обязательные фразы, работа с возражениями. Критерии настраиваем на старте и меняем по ходу.'),
       ('На каких языках разбирает звонки?', 'На английском и русском, арабский подключаем по задаче. Отчёты и рекомендации на языке руководителя.'),
       ('Есть пример внедрения?', 'Да, сеть автосалонов HAVAL: больше 300 000 минут звонков в месяц по 40+ критериям. Кейс есть в разделе кейсов.')]),
 dict(slug='hr', name='HR-агент', short='Найм и собеседования',
  sub='Бот проводит собеседование, оценивает и ведёт воронку',
  title='ИИ-агент для найма: отбор кандидатов и собеседование ботом | MakeBiz',
  desc='HR-агент: отклики с job-площадок и сайта, первое собеседование ботом в Telegram или WhatsApp, оценка кандидатов, резерв и воронка до выхода на работу.',
  h1='Подбор с ИИ-агентом: <span>от отклика до выхода</span>',
  lead='Каждый кандидат получает ссылку на бота, бот проводит первое собеседование и ставит оценку, а руководитель видит каждый шаг в цифрах',
  answer='HR-агент от MakeBiz собирает отклики с job-площадок и вашего сайта, проводит первичное собеседование и тесты в боте на английском или русском, оценивает кандидата и предлагает решение: звать, резерв или отказ. Руководителю остаётся финальная встреча.',
  chips=[('Отклики', 'с площадок и сайта'), ('Бот', 'собеседование на EN и RU'), ('Оценка', 'каждого кандидата'), ('Воронка', 'до выхода на работу')],
  feats=[('Отклики в одном месте', 'Отклики с job-площадок и сайта собираются в воронку, каждый кандидат получает ссылку на бота'),
         ('Собеседование в боте', 'Бот задаёт вопросы по вакансии, проводит тесты и записывает ответы'),
         ('Оценка и решение', 'Балл кандидата, сильные стороны, красные флаги и решение одной кнопкой: звать, резерв или отказ'),
         ('Типажи мотивации', 'Бюджетник, денежник, результатник, статусник: понятно, чем удержать человека'),
         ('Зарплаты', 'Ожидания кандидатов в AED, вилка по рынку и цена навыков'),
         ('Резерв и итоги', 'Сильные кандидаты в резерве с напоминанием, когда написать снова. Итоги испытательного срока показывают, насколько точно бот отбирает людей')],
  ticks=['Сквозная воронка по каждой вакансии и каждому каналу', 'Совпадение решений бота и руководителя в цифрах', 'Сотрудники и итоги испытательного срока', 'Кандидаты и сотрудники в Битрикс24'],
  shots=['hr-obzor', 'hr-kand', 'hr-tests'], video=('https://www.youtube.com/watch?v=DTJ6tVOx6dg', 'HR-блок: подбор от отклика до выхода на работу · 2:48'),
  faq=[('Кандидаты не уходят из-за бота?', 'Бот проходит за 20-30 минут в удобное время, без ожидания звонка. Видно, сколько человек начали тест и сколько дошли до конца.'),
       ('Можно настроить вопросы под нашу вакансию?', 'Да, вопросы, тесты и критерии оценки задаются под каждую вакансию, на английском или русском.'),
       ('С какими площадками работает?', 'Отклики с любых площадок и сайта ведём через бота по ссылке. Прямую интеграцию с конкретной площадкой подключаем по задаче.')]),
 dict(slug='zakupki', name='Закупки', short='Поставщики и КП',
  sub='Рассылает запросы, собирает КП, сравнивает поставщиков',
  title='ИИ-агент для закупок: запросы поставщикам и сравнение КП | MakeBiz',
  desc='ИИ-агент закупок рассылает запросы поставщикам, собирает коммерческие предложения, сравнивает цены, сроки и надёжность и показывает экономию.',
  h1='Агент закупок: <span>недели работы за часы</span>',
  lead='Агент сам рассылает запросы поставщикам, собирает прайсы и КП и сравнивает: где дешевле, у кого быстрее логистика, кто держит цены',
  answer='ИИ-агент закупок от MakeBiz рассылает запросы поставщикам по спецификации, собирает и разбирает КП, сравнивает цену, сроки и надёжность и показывает экономию по каждой процедуре.',
  chips=[('Запросы', 'рассылает сам'), ('КП', 'собирает и сравнивает'), ('Экономия', 'по каждой закупке'), ('Карта', 'поставщиков')],
  feats=[('Запросы поставщикам', 'По спецификации агент рассылает запросы и напоминает тем, кто не ответил'),
         ('Сбор КП', 'Прайсы и предложения в любом виде разбираются в одну таблицу'),
         ('Сравнение', 'Цена, сроки, логистика и условия по каждой позиции'),
         ('Карта поставщиков', 'Цена к рынку против надёжности: кто дешевле, кто держит сроки'),
         ('Внимание', 'Кто дорожает, кто не отвечает, кто срывает сроки'),
         ('Экономия', 'Разница между выбранным и средним КП по каждой процедуре и за месяц')],
  ticks=['Процедуры и их статусы в одном списке', 'База поставщиков с историей ответов', 'Номенклатура и цены во времени', 'Документы закупки сохраняются в CRM'],
  shots=['zak-obzor', 'zak'],
  faq=[('Как агент находит поставщиков?', 'Работает по вашей базе и добавляет новых из открытых источников по номенклатуре.'),
       ('В каком виде нужны КП?', 'В любом: PDF, Excel, письмо или фото. Агент сам разбирает позиции и цены.'),
       ('Кто принимает решение?', 'Вы. Агент готовит сравнение и рекомендацию, выбор остаётся за закупщиком.')]),
 dict(slug='marketing', name='Маркетолог', short='Контент и AI-видимость',
  sub='Статьи, публикация и видимость в поиске и ИИ-ассистентах',
  title='ИИ-маркетолог: контент и видимость в поиске и ChatGPT | MakeBiz',
  desc='ИИ-маркетолог: темы по вопросам клиентов, статьи и новости на английском и русском, публикация на сайте, видимость в ChatGPT, Claude и Perplexity.',
  h1='ИИ-маркетолог: <span>контент и видимость на автопилоте</span>',
  lead='Агент каждую неделю планирует, пишет и публикует экспертные материалы о вашей компании, а потом следит, как они работают в поиске и в ИИ-ассистентах',
  answer='ИИ-маркетолог от MakeBiz находит вопросы, которые клиенты задают в поиске и в ИИ-чатах, пишет статьи и новости на английском и русском, публикует их на сайте с разметкой и проверяет, называют ли вашу компанию ChatGPT, Claude и Perplexity по ключевым запросам.',
  chips=[('Темы', 'по спросу клиентов'), ('EN · RU', 'статьи и новости'), ('GEO', 'ChatGPT, Claude, Perplexity'), ('Заявки', 'с темой-источником')],
  feats=[('Исследование тем', 'Находит вопросы клиентов в поиске и ИИ-чатах, собирает их в контент-план и показывает спрос за каждой темой'),
         ('Статьи и новости', 'Пишет статьи, новости и ответы для FAQ в вашем тоне, на английском и русском, с источниками и внутренними ссылками'),
         ('Публикация', 'Размещает одобренные тексты по графику: заголовки, мета-теги, разметка, картинки и быстрая отправка в индекс'),
         ('GEO, видимость в ответах ИИ', 'Пишет в формате «сначала ответ», который цитируют ассистенты, держит llms.txt и разметку в порядке, проверяет упоминания бренда'),
         ('Дашборды', 'Трафик, позиции, страницы в индексе, заявки с контента и упоминания в ИИ на одном экране'),
         ('Контроль у вас', 'Ничего не выходит без одобрения, если вы так решили. Любой текст можно поправить до публикации')],
  ticks=['Показы и клики в поиске по каждому сайту', 'Страницы в индексе и новые страницы', 'Упоминания в ИИ-ассистентах по месяцам', 'Заявки, которые принесла каждая тема'],
  shots=['mk-search', 'mk-seo', 'mk-geo', 'bi-direct', 'mk-queries'],
  faq=[('Сайт придётся переделывать?', 'Нет. Новые материалы добавляются к тому, что есть, основной сайт не трогаем.'),
       ('Что такое GEO?', 'Продвижение в ответах ИИ-ассистентов: чтобы ChatGPT, Claude и Perplexity называли вашу компанию, когда клиент спрашивает про вашу нишу.'),
       ('Тексты будут на английском?', 'Да, на английском и русском, в вашем тоне. Каждый текст можно поправить до публикации.'),
       ('Как понять, что работает?', 'В дашборде у каждой цифры есть источник: поиск, аналитика сайта, CRM. Видно, сколько заявок и какая тема их принесла.')]),
 dict(slug='finansy', name='Финансы', short='Пульс компании',
  sub='Деньги, прибыль и риски по направлениям',
  title='ИИ-агент финансов: пульс компании, прибыль и запас денег | MakeBiz',
  desc='ИИ-агент финансов: доходы, прибыль, расходы и остатки по каждому направлению на одном экране, маржа, рентабельность, запас денег и сигналы о рисках.',
  h1='Финансовый агент: <span>деньги компании на одном экране</span>',
  lead='Доходы, прибыль, расходы и остатки на счетах по каждому направлению. Агент считает маржу и запас денег и сразу подсвечивает риски',
  answer='Финансовый ИИ-агент от MakeBiz собирает данные из банков, учётной системы и Битрикс24, считает в дирхамах, показывает доходы, прибыль, рентабельность и запас денег по каждому направлению и предупреждает о рисках раньше, чем они станут проблемой.',
  chips=[('Банки', 'учёт и CRM'), ('Прибыль', 'по направлениям'), ('Запас денег', 'в месяцах'), ('Риски', 'сразу видно')],
  feats=[('Пульс компании', 'Доходы, прибыль, расходы и активы за месяц с прогнозом'),
         ('По направлениям', 'Каждый проект и бизнес отдельно и вместе'),
         ('Маржа и рентабельность', 'Где зарабатываете, а где работаете в ноль'),
         ('Запас денег', 'На сколько месяцев хватит денег при текущих расходах'),
         ('Дивиденды и выплаты', 'Сколько выведено и сколько осталось в компании'),
         ('Сигналы', 'Агент сам пишет, если расходы растут быстрее доходов, падает маржа или подходит срок VAT')],
  ticks=['Выписки банков и данные учёта без ручных таблиц', 'Динамика по месяцам и сравнение с прошлым годом', 'Сверка операций', 'Тот же экран для собственника и финансиста'],
  shots=['bi-puls', 'bi-fin'],
  faq=[('Откуда берутся цифры?', 'Из банковских выписок, Zoho Books, QuickBooks, Odoo или 1С и Битрикс24. Источники подключаем на старте.'),
       ('Это замена бухгалтерии?', 'Нет, это управленческий взгляд на деньги для собственника. Бухгалтерия продолжает работать как раньше.'),
       ('Можно вместе с BI-дашбордами?', 'Да, финансы обычно собираем вместе с BI-аналитикой продаж в Битрикс24.')]),
]
AG = {a['slug']: a for a in AGENTS}
YT = {'hr': ('DTJ6tVOx6dg', 'HR-блок с ИИ-агентом: подбор персонала от отклика на hh.ru до выхода на работу', 'Кабинет подключён к hh.ru, Telegram-бот проводит собеседование и ставит оценку, руководитель видит каждый шаг: воронка, оценка кандидатов, типажи мотивации, зарплаты, резерв, итоги испытательного срока.', '2026-10-20', 'PT2M48S'),
      'zvonki': ('HknIeajCo18', 'Речевая аналитика звонков для роста продаж', 'Как речевая аналитика показывает, где менеджеры теряют клиентов, какие возражения повторяются и какие скрипты работают слабо.', '2026-05-26', None)}
def yt_block(k):
    vid, name, desc, d, dur = YT[k]
    return (f'<section class="sec"><div class="wrap"><h2>Видео: <span>как это работает</span></h2><p class="sec-sub">{esc(desc)}</p>'
            f'<div class="yt" data-id="{vid}"><img src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" alt="{esc(name)}" width="480" height="360" loading="lazy"><button type="button" aria-label="Смотреть видео">▶</button></div>'
            f'<p class="more"><a href="https://www.youtube.com/watch?v={vid}" rel="noopener">Смотреть на YouTube →</a></p></div></section>')
def yt_ld(k):
    vid, name, desc, d, dur = YT[k]
    o = {"@type": "VideoObject", "name": name, "description": desc, "thumbnailUrl": [f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"], "uploadDate": d,
         "embedUrl": f"https://www.youtube.com/embed/{vid}", "contentUrl": f"https://www.youtube.com/watch?v={vid}", "inLanguage": "ru", "publisher": {"@id": SITE + "/#organization"}}
    if dur: o["duration"] = dur
    return o
def agent_url(s): return f'/ai-agents/{s}'
def agent_grid(exclude=None):
    out = ''
    for a in AGENTS:
        if a['slug'] == exclude: continue
        out += (f'<a class="agc" href="{U(agent_url(a["slug"]))}"><img src="{U("/img/agents/"+a["shots"][0]+".webp")}" alt="{esc(SHOT_ALT[a["shots"][0]])}" width="1400" height="685" loading="lazy">'
                f'<span class="agc-tx"><small>{esc(a["short"])}</small><b>{esc(a["name"])}</b><span>{esc(a["sub"])}</span></span></a>')
    return f'<div class="agrid">{out}</div>'

ai_faq = [
    ('Чем ИИ-агент отличается от чат-бота?', 'Чат-бот отвечает на вопрос и забывает его. У агента есть роль, память и доступ к вашим системам: он сам ведёт процесс и доводит его до результата, например подхватывает диалог, если менеджер не ответил.'),
    ('Сколько стоит внедрение ИИ-агентов?', 'Один агент от 5 000 AED. Пакеты: Старт 5 000 AED, Бизнес 10 000 AED, для холдингов считаем индивидуально. Обслуживание 10% от стоимости внедрения в месяц. Демонстрацию на вашем процессе проводим бесплатно.'),
    ('Где работают агенты?', 'В WhatsApp, Telegram и в вашей CRM. Система разворачивается на вашем сервере, в том числе в ОАЭ, доступы остаются у вас.'),
    ('На каком языке работают агенты?', 'На английском и русском, с клиентами на языке клиента, при необходимости на арабском. Суммы считают в дирхамах.'),
    ('С какими системами работают агенты?', 'Битрикс24, WhatsApp, Telegram, Zoho Books, QuickBooks, Odoo, 1С, банковские выписки, телефония, Google Ads, Google Analytics, Search Console. Остальное подключаем по задаче.'),
    ('С чего начать?', 'С одного агента там, где больше всего рутины или потерь: переписки, звонки, найм или закупки. Запускаем, меряем результат и добавляем следующих.'),
]
ai_body = hero('ИИ-агенты · внедрение', 'ИИ-агенты, которые <span>работают внутри бизнеса</span>',
    'Не чат-бот на сайте, а команда цифровых сотрудников: РОП, связной, речевая аналитика, HR, закупки, маркетинг и финансы',
    'MakeBiz Technologies разрабатывает и внедряет ИИ-агентов для компаний в Дубае и ОАЭ: РОП ведёт переписки в WhatsApp и план продаж, Связной следит за контактами, агент звонков оценивает каждый разговор, HR-агент проводит первое собеседование, агенты закупок, маркетинга и финансов работают на BI-дашбордах. Один агент от 5 000 AED.',
    ('#form', 'Записаться на демонстрацию'), ('#agenty', 'Все агенты'), V_AGENTS,
    [('7 агентов', 'по отделам'), ('от 5 000 AED', 'один агент'), ('Ваш сервер', 'данные у вас'), ('EN · RU', 'языки работы')], 'Команда ИИ-агентов за работой')
ai_body += section('Наши агенты', 'Нашей компанией сами управляют эти агенты: они встроены в CRM, банки, продажи, маркетинг, найм и закупки. Каждого можно внедрить отдельно, один агент от 5 000 AED', agent_grid(), id_='agenty')
ai_body += video_block()
ai_body += section('Агент, а не чат-бот', '', '''<div class="vs"><div class="vs-col"><h3>Чат-бот</h3><ul><li>Отвечает по сценарию и забывает разговор</li><li>Живёт на сайте, не видит CRM</li><li>Не доводит задачу до конца</li><li>Ждёт, пока к нему придут</li></ul></div>
<div class="vs-col vs-good"><h3>ИИ-агент</h3><ul><li>Помнит клиента и историю</li><li>Работает в CRM, WhatsApp, учёте и банке</li><li>Сам ведёт процесс до результата</li><li>Сам замечает проблему и подключает человека</li></ul></div></div>''', tone='tint')
ai_body += section('Пакеты внедрения', 'Малый вход: один агент, понятный результат, потом расширяем. Демонстрация на вашем процессе бесплатно', prices([
    ('Старт', '5 000 AED', 'разово', ['Один агент на ключевом процессе', 'Подключение CRM и мессенджеров', 'Замер результата'], False),
    ('Бизнес', '10 000 AED', 'разово', ['Команда агентов для нескольких отделов', 'Общие данные и дашборд', 'Запуск по очереди'], True),
    ('Холдинг', 'индивидуально', 'по смете', ['Несколько компаний и контуров', 'Free zone и материк раздельно', 'Свой сервер в ОАЭ'], False),
], 'Обслуживание агентов 10% от стоимости внедрения в месяц: донастройка, разбор сбоев и улучшения'))
ai_body += section('Как внедряем', '', steps([
    ('Диагностика', 'Находим процесс, где агент даст результат быстрее всего'),
    ('Сборка', 'Настраиваем роли агентов, доступы и интеграции на вашем сервере, в том числе в ОАЭ'),
    ('Запуск', 'Агенты работают вместе с командой, мы смотрим на качество'),
    ('Развитие', 'Добавляем агентов и процессы, обучаем сотрудников'),
]), tone='tint')
ai_body += section('Кейсы', '', case_cards(['haval-vector', 'apartika-crm', 'cdek-b2b']))
ai_body += contract_block() + faq(ai_faq) + form_block('ai-agents', 'Покажем агентов на вашем процессе') + crosslink('bitrix')
built.append(page('/ai-agents', 'ai-agents', 'ИИ-агенты для бизнеса в Дубае и ОАЭ: продажи, звонки, HR | MakeBiz',
    'ИИ-агенты для бизнеса в Дубае и ОАЭ: РОП в WhatsApp, связной, речевая аналитика звонков, HR, закупки, маркетинг и финансы в Битрикс24. Один агент от 5 000 AED.',
    'ai', ai_body, [service_ld('Внедрение ИИ-агентов', 'Разработка и внедрение ИИ-агентов для бизнеса в ОАЭ', '/ai-agents', 5000), VIDEO_LD,
                    {"@type": "ItemList", "name": "ИИ-агенты MakeBiz", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": a['name'], "url": SITE + agent_url(a['slug'])} for i, a in enumerate(AGENTS)]}],
    [('/', 'Главная'), ('/ai-agents', 'ИИ-агенты')], ai_faq))

for a in AGENTS:
    s = a['slug']
    vid = ''
    if a.get('video'):
        vid = f'<a class="btn btn-ghost" href="{a["video"][0]}" target="_blank" rel="noopener">▶ {esc(a["video"][1])}</a>'
    b = hero(f'ИИ-агенты · {a["name"]}', a['h1'], a['lead'], a['answer'], ('#form', 'Показать на нашем процессе'), (U('/ai-agents') + '#agenty', 'Все агенты'),
             '<div class="hero-shot">' + shots(a['shots'][:1], SHOT_ALT[a['shots'][0]].split(':')[0]) + '</div>', a['chips'], a['name'])
    b += section('Что делает агент', '', cards(a['feats'], 3))
    b += feature('ekrany', 'Кабинет', 'Что видит <span>руководитель</span>', 'Экраны из нашего кабинета на демо-данных. У вас будут ваши цифры', a['ticks'], a['shots'], SHOT_ALT[a['shots'][0]].split(':')[0], extra=vid)
    if s in YT: b += yt_block(s)
    b += section('Как запускаем', '', steps([
        ('Демонстрация', 'Показываем агента на живой системе и разбираем ваш процесс'),
        ('Подключение', 'Доступы к CRM, мессенджерам и нужным сервисам на вашем сервере'),
        ('Настройка', 'Правила, критерии и тексты под вашу компанию'),
        ('Работа', 'Агент работает вместе с командой, мы следим за качеством'),
    ]), tone='tint')
    b += section('Другие агенты', 'Агенты работают на общих данных и усиливают друг друга', agent_grid(exclude=s))
    b += contract_block() + faq(a['faq']) + form_block('ai-' + s, f'Покажем агента «{a["name"]}» на вашем процессе') + crosslink('bitrix')
    built.append(page(agent_url(s), 'ai-' + s, a['title'], a['desc'], 'ai', b,
        [service_ld(f'ИИ-агент {a["name"]}', a['desc'], agent_url(s))] + ([yt_ld(s)] if s in YT else []),
        [('/', 'Главная'), ('/ai-agents', 'ИИ-агенты'), (agent_url(s), a['name'])], a['faq']))

# ---------- КЕЙСЫ: фильтр по сферам и направлениям, страница на каждый кейс
used_ind = [k for k, _ in SPHERES if any(k in c['ind'] for c in CASEJ)]
used_prd = [k for k, _ in PRODS if any(k in c['products'] for c in CASEJ)]
chips_ind = '<button type="button" class="fchip on" data-f="ind" data-v="">Все сферы</button>' + ''.join(
    f'<button type="button" class="fchip" data-f="ind" data-v="{k}">{esc(SPH[k])}<i>{sum(k in c["ind"] for c in CASEJ)}</i></button>' for k in used_ind)
chips_prd = '<button type="button" class="fchip on" data-f="prod" data-v="">Все решения</button>' + ''.join(
    f'<button type="button" class="fchip" data-f="prod" data-v="{k}">{esc(PRD[k])}<i>{sum(k in c["products"] for c in CASEJ)}</i></button>' for k in used_prd)
ks_body = f'''<section class="hero hero-small"><div class="wrap"><div class="eyebrow">Кейсы</div><h1>Кейсы <span>MakeBiz</span></h1>
<p class="lead">Проекты по Битрикс24, ИИ-агентам и BI-аналитике, которые ведём годами. Выберите свою сферу или нужное решение</p></div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><div class="kfilter gl" data-target="#cases-all">
<div class="kf-row"><span class="kf-t">Сфера</span>{chips_ind}</div><div class="kf-row"><span class="kf-t">Решение</span>{chips_prd}</div></div>
<div id="cases-all">{case_cards([c["slug"] for c in CASEJ])}</div><p class="kf-empty" hidden>В этой сфере кейс пока готовим. Расскажем о похожих проектах на созвоне</p></div></section>
{form_block('keysy', 'Хотите так же?')}'''
built.append(page('/keysy', 'keysy', 'Кейсы внедрения Битрикс24 и ИИ-агентов по отраслям | MakeBiz',
    'Кейсы MakeBiz по сферам: логистика, производство, автобизнес, недвижимость, образование. Битрикс24, интеграция с 1С, BI-аналитика и ИИ-агенты.',
    'keysy', ks_body, [{"@type": "ItemList", "name": "Кейсы MakeBiz", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": notag(c['title']), "url": SITE + '/keysy/' + c['slug']} for i, c in enumerate(CASEJ)]}],
    [('/', 'Главная'), ('/keysy', 'Кейсы')]))

for c in CASEJ:
    s = c['slug']; org = c['client'].split(',')[0]
    h1 = c['title'].replace('<b>', '<span>').replace('</b>', '</span>')
    facts = ([('Результат', (c.get('metric_v', '') + ' ' + c.get('metric_t', '')).strip())] if c.get('metric_v') else []) + [('Клиент', c['client']), ('Регион', c['region']), ('Что внедрили', notag(c['built'])), ('Срок', c['term'])]
    facts_html = ''.join(f'<div class="kfact"><small>{esc(a)}</small><b>{esc(b)}</b></div>' for a, b in facts if b)
    q = ''
    if c.get('quote'):
        qq = c['quote']; q = f'<blockquote class="kquote gl"><p>{esc(notag(qq.get("text","")))}</p><cite>{esc(qq.get("name",""))}{", " + esc(qq.get("role","")) if qq.get("role") else ""}</cite></blockquote>'
    tags = ''.join(f'<a class="ktag" href="{U("/keysy")}#{k}">{esc(SPH.get(k, k))}</a>' for k in c['ind']) + ''.join(f'<span class="ktag ktag-p">{esc(PRD.get(p, p))}</span>' for p in c['products'])
    body = f'''<section class="hero hero-small"><div class="wrap"><div class="eyebrow">Кейс · {esc(SPH.get(c["ind"][0], ""))}</div><h1>{h1}</h1>
<p class="lead">{esc(notag(c["lead"]))}</p><div class="ktags">{tags}</div>
<div class="kfacts">{facts_html}</div>
<div class="case-ba kba"><p><span>Было</span>{esc(c["was"])}</p><p><span>Стало</span>{esc(c["now"])}</p></div></div></section>
<section class="sec" style="padding-top:0"><div class="wrap kbody">
<article class="kart gl"><h2>Задача</h2><p>{esc(notag(c["problem"]))}</p><h2>Что сделали</h2><p>{esc(notag(c["solution"]))}</p><h2>Результат</h2><p>{esc(notag(c["result"]))}</p>
{f'<p class="ksoft">{c["soft"]}</p>' if c.get("soft") else ""}</article>{q}</div></section>'''
    others = [x['slug'] for x in CASEJ if x['slug'] != s][:3]
    body += section('Другие кейсы', '', case_cards(others)) + form_block('case-' + s, 'Хотите так же?')
    built.append(page('/keysy/' + s, 'case-' + s, (lambda tt: tt + ' | MakeBiz' if len(tt) <= 60 else tt)(f'Кейс {org}: {notag(c["title"]).split(":", 1)[-1].strip()}'),
        clip(notag(c['lead']), 165), 'keysy', body,
        [{"@type": "Article", "headline": notag(c['title']), "description": notag(c['lead']), "datePublished": c['date'] + '-01',
          "dateModified": UPDATED_ISO, "author": {"@id": SITE + "/#organization"}, "publisher": {"@id": SITE + "/#organization"},
          "about": {"@type": "Organization", "name": org}, "mainEntityOfPage": SITE + '/keysy/' + s, "inLanguage": "ru"}],
        [('/', 'Главная'), ('/keysy', 'Кейсы'), ('/keysy/' + s, org)]))

# ---------- ПАРТНЁРАМ
pt_faq = [
    ('Как фиксируется мой клиент?', 'По имени и компании в момент знакомства. Клиент закрепляется за вами на 6 месяцев, все его оплаты в этот период считаются вашими.'),
    ('Что если клиент уже обращался к вам сам?', 'Тогда честно скажем об этом сразу, до начала работы. Спорных ситуаций не тянем.'),
    ('Мне нужно разбираться в CRM и ИИ?', 'Нет. Вы знакомите, всю работу от встречи до внедрения делаем мы.'),
    ('Когда я получу деньги?', 'После оплаты клиентом, в дирхамах на счёт.'),
    ('Нужен ли договор?', 'Да, простой партнёрский договор с MakeBiz Technologies FZE LLC на физлицо или компанию. Пришлём шаблон до старта.'),
    ('Есть ли планы и обязательства?', 'Нет. Один клиент в год тоже нормально.'),
]
pt_body = hero('Партнёрская программа', 'Приводите бизнес и <span>зарабатывайте с каждой оплаты</span>',
    'Вы рекомендуете, мы берём на себя встречи, внедрение и поддержку. Вы получаете 20% с первой сделки и 10% со всех платежей клиента ещё год',
    'Партнёрская программа MakeBiz Technologies в ОАЭ: 20% с первой оплаты приведённого клиента и 10% со всех его платежей в течение 12 месяцев за внедрение Битрикс24, ИИ-агентов и BI-аналитики. По договору, выплаты в дирхамах, продавать ничего не нужно.',
    ('#form', 'Стать партнёром'), ('#calc', 'Сколько я заработаю'),
    '''<div class="pcalc gl" id="calc"><div class="pc-h">Калькулятор партнёра</div>
<label>Клиентов за год <b data-o="n">5</b><input type="range" min="1" max="20" value="5" data-i="n"></label>
<label>Средний чек клиента <b data-o="c">15 000 AED</b><input type="range" min="5000" max="100000" step="5000" value="15000" data-i="c"></label>
<div class="pc-rows"><p><span>С первой оплаты · 20%</span><b data-o="first">0 AED</b></p><p><span>С повторных оплат · 10%</span><b data-o="rep">0 AED</b></p></div>
<div class="pc-tot"><span>Ваш доход за год</span><b data-o="tot">0 AED</b></div><small>Оценка: в среднем клиент платит 4 раза в год, повторная оплата около половины первой</small></div>''',
    [('20%', 'с первой сделки'), ('10%', 'со всех платежей год'), ('6 месяцев', 'клиент закреплён за вами'), ('Договор', 'официальные выплаты')], 'Калькулятор партнёра')
pt_body += section('Как узнать нашего клиента', 'Познакомьте нас, если у знакомого бизнеса есть хотя бы что-то из этого. Ничего продавать не нужно', cards([
    ('Хаос в продажах и задачах', 'Заявки и договорённости держатся в голове и в чатах'), ('CRM нет или она не работает', 'Купили Битрикс24, а им никто не пользуется'),
    ('Заявки теряются', 'Клиенты пишут в мессенджеры и ждут ответа часами'), ('Много звонков без контроля', 'Никто не знает, как менеджеры говорят с клиентами'),
    ('Ручная работа с документами', 'Счета с VAT, накладные и сверки вручную'), ('Хочет ИИ, но не знает как', 'Слышал про агентов и не понимает, с чего начать'),
], 3))
pt_body += section('От рекомендации до выплаты', 'Вы приводите клиента любым удобным способом, остальное делаем мы', steps([
    ('Делитесь контактом', 'В канале, соцсетях, на сайте или лично, как удобнее'),
    ('Лид закрепляется за вами', 'Заявка привязывается к вам, без таблиц и споров'),
    ('Мы закрываем и внедряем', 'Встречи, предложение, запуск и поддержка на нашей стороне'),
    ('Вы получаете выплату', 'Начисляем по факту оплаты клиентом'),
]), tone='tint')
pt_body += section('Отношения не в одну сторону', 'К нам регулярно приходят компании, которым нужны регистрация бизнеса, бухгалтерия, маркетинг, юристы. Когда появляется клиент по вашему профилю, мы передаём его вам', cards([
    ('Вы нам', 'Знакомство с бизнесом, которому нужен порядок в продажах, CRM или ИИ-агенты'),
    ('Мы вам', 'Процент с оплат и заявки на ваши услуги: регистрация, бухгалтерия, маркетинг, юристы'),
], 2))
pt_body += section('Как работаем с партнёрами', '', cards([
    ('Без давления', 'Не торопим, не уговариваем, не ставим планов'), ('Вам мы не продаём', 'Вы партнёр, а не клиент'),
    ('Прозрачно', 'Вы видите свои сделки и начисления'), ('Мы о вас помним', 'Появился клиент по вашему профилю, пишем'),
    ('По-белому', 'Договор и официальные выплаты'),
], 3, numbered=True))
pt_body += faq(pt_faq) + form_block('partners', 'Стать партнёром', 'Оставьте контакт: пришлём договор и расскажем, как передавать клиентов')
built.append(page('/partners', 'partners', 'Партнёрская программа MakeBiz: 20% с первой сделки и 10% год | MakeBiz',
    'Партнёрская программа MakeBiz в ОАЭ: 20% с первой оплаты клиента и 10% со всех платежей 12 месяцев за рекомендации на Битрикс24, ИИ-агентов и BI. По договору.',
    'partners', pt_body, [service_ld('Партнёрская программа MakeBiz', 'Вознаграждение за рекомендации клиентов на внедрение Битрикс24 и ИИ-агентов', '/partners')],
    [('/', 'Главная'), ('/partners', 'Партнёрам')], pt_faq))

# ---------- ЦЕНЫ
ce_faq = [
    ('Сколько стоит внедрение Битрикс24 в ОАЭ?', f'Стандартная настройка CRM Битрикс24 от 10 000 AED, базовый запуск от 14 дней. Работы сверх стандарта 200 AED в час. Лицензия Битрикс24 оплачивается отдельно: облако от {aed(49)} в месяц при оплате за год, коробка от {aed(3590)} в год.'),
    ('Сколько стоит поддержка Битрикс24?', 'Пакеты часов в месяц: 5 часов за 1 250 AED, 10 часов за 2 300 AED, 20 часов за 4 200 AED. Час сверх пакета 250 AED.'),
    ('Сколько стоят ИИ-агенты?', 'Один агент от 5 000 AED. Пакеты: Старт 5 000 AED, Бизнес 10 000 AED, Холдинг индивидуально. Обслуживание 10% от стоимости внедрения в месяц, демонстрация бесплатно.'),
    ('Сколько стоят интеграции, WhatsApp и BI?', 'Интеграция с учётной системой (Zoho Books, QuickBooks, Odoo, 1С) от 10 000 AED, подключение WhatsApp или другого мессенджера 500 AED, BI-аналитика от 1 000 AED. Смету фиксируем до старта.'),
    ('Сколько стоит речевая аналитика звонков?', '1 000 AED в месяц за 5 000 минут, 1 700 AED за 10 000 минут, от 4 000 AED от 30 000 минут.'),
    ('Как оплачивать?', 'По договору с MakeBiz Technologies FZE LLC, счёт в дирхамах, оплата на счёт компании в ОАЭ.'),
]
CE_ROWS = [
    ('Битрикс24', [('Стандартная настройка CRM', 'от 10 000 AED', 'запуск от 14 дней', '/bitrix'),
                   ('Час работы', '200 AED', 'сложные проекты, доработки', '/bitrix'),
                   ('Внедрение коробочного Битрикс24', 'по смете', 'ставка 200 AED/ч', '/bitrix-korobka'),
                   ('Подключение WhatsApp или мессенджера', '500 AED', 'подписка провайдера отдельно', '/bitrix-messengers'),
                   ('Интеграция с учётной системой', 'от 10 000 AED', 'Zoho Books, QuickBooks, Odoo, 1С', '/bitrix-integrations'),
                   ('BI-аналитика', 'от 1 000 AED', 'смета после списка показателей', '/bi-analitika')]),
    ('Поддержка Битрикс24', [('5 часов', '1 250 AED', 'в месяц', '/bitrix-support'),
                   ('10 часов', '2 300 AED', 'в месяц', '/bitrix-support'),
                   ('20 часов', '4 200 AED', 'в месяц', '/bitrix-support'),
                   ('Час сверх пакета', '250 AED', 'по факту', '/bitrix-support')]),
    (f'Лицензии Битрикс24 (цены bitrix24.ae на {PRICE_DATE})', [('Облако Basic, 5 пользователей', aed(49), 'в месяц при оплате за год ($49)', '/bitrix-licenses'),
                   ('Облако Standard, 50 пользователей', aed(99), 'в месяц при оплате за год ($99)', '/bitrix-licenses'),
                   ('Облако Professional, 100 пользователей', aed(199), 'в месяц при оплате за год ($199)', '/bitrix-licenses'),
                   ('Облако Enterprise, 250 пользователей', aed(399), 'в месяц при оплате за год ($399)', '/bitrix-licenses'),
                   ('Коробка Business, 50 пользователей', aed(3590), 'лицензия на год ($3 590)', '/bitrix-korobka'),
                   ('Коробка Enterprise, от 1 000 пользователей', aed(24990), 'лицензия на год ($24 990)', '/bitrix-korobka')]),
    ('ИИ-агенты', [('Пакет Старт, один агент', '5 000 AED', 'разово', '/ai-agents'),
                   ('Пакет Бизнес, команда агентов', '10 000 AED', 'разово', '/ai-agents'),
                   ('Пакет Холдинг', 'индивидуально', 'по смете', '/ai-agents'),
                   ('Обслуживание агентов', '10%', 'от стоимости внедрения в месяц', '/ai-agents'),
                   ('Демонстрация на вашем процессе', 'бесплатно', '30-40 минут', '/ai-agents')]),
    ('Речевая аналитика звонков', [('5 000 минут', '1 000 AED', 'в месяц', '/ai-agents/zvonki'),
                   ('10 000 минут', '1 700 AED', 'в месяц', '/ai-agents/zvonki'),
                   ('от 30 000 минут', 'от 4 000 AED', 'в месяц', '/ai-agents/zvonki')]),
]
def ce_table():
    out = ''
    for g, rows in CE_ROWS:
        tr = ''.join(f'<tr><td><a href="{U(u)}"><b>{esc(n)}</b></a></td><td class="pt-p">{esc(nb(v))}</td><td>{esc(c)}</td></tr>' for n, v, c, u in rows)
        out += f'<h3 class="ce-h">{esc(g)}</h3><div class="ptw gl"><table class="ptab"><thead><tr><th>Услуга</th><th>Цена</th><th>Условия</th></tr></thead><tbody>{tr}</tbody></table></div>'
    return out
ce_body = f'''<section class="hero hero-small"><div class="wrap"><div class="eyebrow">Цены в AED</div><h1>Цены на услуги <span>MakeBiz в ОАЭ</span></h1>
<p class="lead">Внедрение и поддержка Битрикс24, лицензии, ИИ-агенты и речевая аналитика: все цены в дирхамах на одной странице. Работаем по договору, смету фиксируем до старта</p>
<p class="answer">Стандартная настройка CRM Битрикс24 в MakeBiz Technologies от 10 000 AED, час работы 200 AED, поддержка от 1 250 AED в месяц за 5 часов, интеграция с учётом от 10 000 AED, WhatsApp 500 AED, BI-аналитика от 1 000 AED, один ИИ-агент от 5 000 AED. Лицензии Битрикс24: облако от {aed(49)} в месяц, коробка от {aed(3590)} в год. Цены на {PRICE_DATE}.</p></div></section>
<section class="sec" style="padding-top:20px"><div class="wrap">{ce_table()}<p class="note">Цены услуг без учёта лицензий и VAT, если не указано иное. Лицензии по ценам вендора с bitrix24.ae в долларах США, в дирхамах по курсу 3,6725</p></div></section>'''
ce_body += contract_block() + faq(ce_faq) + form_block('ceny', 'Посчитаем ваш проект', 'Опишите задачу, пришлём смету в дирхамах с ценой и сроком')
built.append(page('/ceny', 'ceny', 'Цены MakeBiz в ОАЭ: Битрикс24, поддержка и ИИ-агенты в AED',
    f'Цены MakeBiz в AED на {PRICE_DATE}: настройка CRM Битрикс24 от 10 000 AED, поддержка от 1 250 AED в месяц, час 200 AED, ИИ-агент от 5 000 AED, лицензии от {aed(49)}.',
    'ceny', ce_body, [{"@type": "OfferCatalog", "name": "Услуги MakeBiz в ОАЭ", "itemListElement": [
        {"@type": "Offer", "name": n, "price": re.sub(r'\D', '', v), "priceCurrency": "AED", "url": SITE + u, "seller": {"@id": SITE + "/#organization"}}
        for g, rows in CE_ROWS for n, v, c, u in rows if re.sub(r'\D', '', v) and 'AED' in v]}],
    [('/', 'Главная'), ('/ceny', 'Цены')], ce_faq))

# ---------- VPS И СЕРВЕРЫ (провайдеры как на servercalc.com, видимость и порядок из кабинета MakeBiz)
from vps_src import providers as vps_providers, price_text as vps_price
VPS = vps_providers('ru')
def vps_cards(items):
    out = ''
    for d in items:
        pt = vps_price(d['plan'], 'ru')
        pr = f'<div class="price-val" style="font-size:22px">{esc(pt[0])}</div><div class="price-unit">{esc(pt[1])}</div>' if pt else '<div class="price-unit">цена на сайте провайдера</div>'
        tags = ' · '.join(d['geos'])
        fe = ''.join(f'<li>{esc(a)}</li>' for a in (d['pros'][:2] + [f[0] for f in d['feats'][:2]]))
        out += (f'<div class="price{" is-hot" if d["pinned"] and d["rank"] == 1 else ""}"><div class="price-name">{esc(d["name"])}</div>{pr}'
                f'<p class="vps-geo">{esc(tags)}</p><p class="vps-desc">{esc(d["desc"])}</p><ul>{fe}</ul>'
                f'<a class="btn {"" if d["pinned"] else "btn-ghost"}" href="{esc(d["href"])}" rel="{d["rel"]}" target="_blank">На сайт {esc(d["name"])} →</a></div>')
    return f'<div class="grid g3 prices vps-grid">{out}</div>'
VPS_N = len(VPS)
VPS_MIN = min([d['plan'] for d in VPS if d['plan'] and d['plan']['currency'] == 'USD'], key=lambda x: x['price'], default=None)
VPS_FROM = (f'${int(VPS_MIN["price"]) if float(VPS_MIN["price"]).is_integer() else VPS_MIN["price"]}' if VPS_MIN else '')
VPS_DATE = max([d['verified'] for d in VPS if d['verified']], default='')
vps_faq = [
    ('Какой VPS выбрать для Битрикс24?', 'Для облачного Битрикс24 сервер не нужен. Для коробочной версии на 50 пользователей обычно хватает сервера с 4 vCPU, 8 ГБ памяти и NVMe-диском, для сотен пользователей больше. Конфигурацию подбираем под ваше число пользователей и нагрузку.'),
    ('Есть серверы в ОАЭ?', 'Да, часть провайдеров из списка даёт площадки в ОАЭ, у них в карточке отмечена география «ОАЭ». Если данные должны храниться в стране, начинаем с них.'),
    ('Вы сами продаёте серверы?', 'Нет. Вы покупаете сервер у провайдера напрямую, по своей учётной записи, и платите ему. Мы помогаем выбрать, разворачиваем и настраиваем систему и при желании берём сервер на поддержку.'),
    ('Сколько стоит настройка сервера?', 'Работы по ставке 200 AED в час или в рамках пакета поддержки от 1 250 AED в месяц. Перед началом называем оценку в часах.'),
    ('Почему ссылки партнёрские?', 'MakeBiz может получать вознаграждение от провайдера, для вас цена не меняется. Список и порядок те же, что в нашем каталоге servercalc.com.'),
]
vps_body = hero('Серверы и VPS', 'VPS и серверы <span>для бизнеса в ОАЭ</span>',
    'Подбираем сервер под задачу: коробочный Битрикс24, сайт, ИИ-агенты, базы данных. Разворачиваем, настраиваем и берём на поддержку',
    f'MakeBiz Technologies помогает компаниям в ОАЭ выбрать VPS у проверенных провайдеров ({VPS_N} в списке, есть площадки в ОАЭ, Европе, США и Азии), разворачивает на нём коробочный Битрикс24, сайты и ИИ-агентов и сопровождает сервер. Тарифы{(" от " + VPS_FROM + " в месяц") if VPS_FROM else ""} по данным каталога servercalc.com, работы по настройке 200 AED в час.',
    ('#form', 'Подобрать сервер'), ('#providers', 'Провайдеры'), V_BOX,
    [(f'{VPS_N}', 'провайдеров'), ((f'от {VPS_FROM}' if VPS_FROM else 'ОАЭ'), 'в месяц' if VPS_FROM else 'и другие страны'), ('200 AED/ч', 'настройка'), ('servercalc.com', 'наш каталог')], 'Серверы для Битрикс24 и ИИ-агентов')
vps_body += section('Провайдеры', f'Тот же список и порядок, что в нашем каталоге <a href="https://servercalc.com/" target="_blank" rel="noopener">servercalc.com</a>. Цена самого доступного тарифа{(", проверено " + VPS_DATE) if VPS_DATE else ""}. Ссылки партнёрские, для вас цена не меняется', vps_cards(VPS), id_='providers')
vps_body += section('Что делаем мы', 'Сервер купить легко, сложнее правильно его настроить и не потерять данные', cards([
    ('Подбор', 'Считаем пользователей и нагрузку, выбираем провайдера, страну и тариф без переплаты'),
    ('Развёртывание', 'Ставим коробочный Битрикс24, сайт, базы данных или ИИ-агентов, настраиваем SSL и почту'),
    ('Безопасность', 'Доступы, файрвол, обновления и резервные копии по расписанию'),
    ('Перенос', 'Переносим портал или сайт со старого сервера или из облака без остановки работы'),
    ('Мониторинг', 'Следим за нагрузкой, местом на диске и доступностью'),
    ('Поддержка', 'Сервер в пакете поддержки вместе с Битрикс24: от 1 250 AED в месяц'),
], 3), tone='tint')
vps_body += contract_block() + faq(vps_faq) + form_block('vps', 'Подберём сервер под вашу задачу', 'Напишите, что будет работать на сервере и сколько пользователей, предложим провайдера, тариф и смету настройки') + crosslink('ai')
built.append(page('/vps', 'vps', 'VPS и серверы для бизнеса в ОАЭ: подбор и настройка | MakeBiz',
    f'VPS для бизнеса в ОАЭ: {VPS_N} проверенных провайдеров, площадки в ОАЭ, Европе и США. Подбор, развёртывание Битрикс24 и ИИ-агентов, настройка 200 AED в час.',
    'vps', vps_body, [service_ld('Подбор и настройка VPS', 'Подбор VPS, развёртывание Битрикс24 и ИИ-агентов, сопровождение сервера', '/vps', 200),
        {"@type": "ItemList", "name": "Провайдеры VPS", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": d['name'], "url": d['href']} for i, d in enumerate(VPS)]}],
    [('/', 'Главная'), ('/vps', 'Серверы и VPS')], vps_faq))

# ---------- О КОМПАНИИ
ab_faq = [
    ('Кто стоит за MakeBiz Technologies?', 'Компанию основал Антон Чернобаев. Команда 8 лет в IT и CRM, более 150 проектов внедрения. Юрлицо MakeBiz Technologies FZE LLC, свободная экономическая зона Ajman NuVentures Centre, регистрационный номер 2624215090888.'),
    ('Где вы работаете?', 'В Дубае и по всем Эмиратам: встречи в Дубае или по видеосвязи. Работаем с компаниями в ОАЭ и с русскоязычным бизнесом по всему миру, договор и счета в дирхамах.'),
    ('На каком языке работаете?', 'На русском и английском. Систему, обучение и документы готовим на языке команды.'),
    ('Чем MakeBiz отличается от других интеграторов?', 'Мы сами управляем компанией через ИИ-агентов и BI-кабинет, которые внедряем клиентам, и делаем Битрикс24, интеграции и ИИ одной командой.'),
    ('Вы помогаете с регистрацией компании и визами?', 'Нет, мы IT-интегратор: Битрикс24, ИИ-агенты и BI. По регистрации бизнеса можем познакомить с проверенными партнёрами.'),
]
ab_body = hero('О компании', 'MakeBiz Technologies: <span>Битрикс24 и ИИ-агенты в ОАЭ</span>',
    'Внедряем Битрикс24 и ИИ-агентов, чтобы бизнес терял меньше и рос быстрее. Сами работаем на тех же агентах и дашбордах, которые ставим клиентам',
    'MakeBiz Technologies FZE LLC (Ajman NuVentures Centre, ОАЭ), официальный партнёр Битрикс24, основана Антоном Чернобаевым: 8 лет в IT и CRM, более 150 проектов внедрения Битрикс24, ИИ-агентов и BI-аналитики. Работаем с компаниями в Дубае и по всем Эмиратам на русском и английском, клиенты MakeBiz: СДЭК, Unilin, HAVAL.',
    ('#form', 'Обсудить задачу'), (U('/keysy'), 'Кейсы'), V_AGENTS,
    [('8 лет', 'в IT и CRM'), ('150+', 'проектов'), ('FZE LLC', 'компания в ОАЭ'), ('RU · EN', 'язык работы')], 'Команда MakeBiz')
ab_body += section('Что мы делаем', '', cards([
    ('Битрикс24 под ключ', f'Внедрение облачного и <a href="{U("/bitrix-korobka")}">коробочного</a> Битрикс24, поддержка, WhatsApp, интеграции с учётом, лицензии и BI'),
    ('ИИ-агенты', f'<a href="{U("/ai-agents")}">Команда агентов</a>: РОП, связной, речевая аналитика, HR, закупки, маркетинг, финансы'),
    ('Аналитика', 'BI-дашборды на данных CRM, учётных систем, банков, телефонии и рекламы'),
    ('Серверы и VPS', f'<a href="{U("/vps")}">Подбор и настройка серверов</a> у проверенных провайдеров, в том числе с площадками в ОАЭ'),
], 4))
ab_body += section('Основатель', '', f'''<div class="founder gl"><div><h3>Антон Чернобаев</h3><p class="f-role">Основатель MakeBiz, Дубай</p>
<p>Строит компанию вокруг двух направлений: Битрикс24 и ИИ-агенты. Лично разбирает процессы клиентов на старте проектов и показывает, как MakeBiz сам управляется через агентов и BI</p>
<p class="f-links"><a href="https://t.me/Anton_MakeBiz" rel="noopener">Telegram</a> · <a href="https://www.youtube.com/channel/UCyXI8U1O215HBGvOwqVjq2Q" rel="noopener">YouTube</a></p></div></div>''', tone='tint')
ab_body += section('Почему нам доверяют', '', cards([
    ('Компания в ОАЭ', 'MakeBiz Technologies FZE LLC, Ajman NuVentures Centre, рег. номер 2624215090888'),
    ('Официальный партнёр Битрикс24', 'Внедряем, поддерживаем и помогаем с лицензиями Битрикс24 в ОАЭ. Договор и счета в дирхамах'),
    ('Проекты годами', 'СДЭК второй год, Unilin третий год: остаёмся на поддержке после запуска'),
    ('Сами на своих агентах', 'Финансы, продажи, найм, закупки и маркетинг MakeBiz ведут ИИ-агенты'),
], 4))
ab_body += section('Кейсы', '', case_cards(['cdek-b2b', 'unilin-crm', 'haval-vector']))
ab_body += faq(ab_faq) + form_block('o-kompanii', 'Обсудим вашу задачу')
built.append(page('/o-kompanii', 'o-kompanii', 'О компании MakeBiz Technologies: Битрикс24 и ИИ-агенты в ОАЭ',
    'MakeBiz Technologies FZE LLC: внедрение Битрикс24, ИИ-агенты и BI для компаний в Дубае и ОАЭ. Основатель Антон Чернобаев, 8 лет в IT, более 150 проектов.',
    'o-kompanii', ab_body, [{"@type": "AboutPage", "url": SITE + "/o-kompanii", "about": {"@id": SITE + "/#organization"}},
        {"@type": "Person", "@id": SITE + "/#founder", "name": "Антон Чернобаев", "jobTitle": "Основатель", "worksFor": {"@id": SITE + "/#organization"},
         "sameAs": ["https://t.me/Anton_MakeBiz", "https://www.youtube.com/channel/UCyXI8U1O215HBGvOwqVjq2Q"]}],
    [('/', 'Главная'), ('/o-kompanii', 'О компании')], ab_faq))

# ---------- КОНТАКТЫ
ct_faq = [
    ('Как связаться с MakeBiz Technologies?', f'Телефон и WhatsApp {PHONE}, Telegram @{TG}, почта {EMAIL}. Или оставьте заявку на сайте.'),
    ('Где проходят встречи?', 'В Дубае по договорённости или по видеосвязи. Работаем с компаниями по всем Эмиратам.'),
    ('Как быстро ответите?', 'В рабочее время в течение часа в WhatsApp и Telegram, на заявку с сайта в течение рабочего дня.'),
]
ct_body = f'''<section class="hero hero-small"><div class="wrap"><div class="eyebrow">Контакты</div><h1>Свяжитесь <span>с нами</span></h1>
<p class="lead">Ответим в течение рабочего дня, разберём задачу и предложим решение</p>
<div class="grid g3 contacts">
<a class="card" href="https://wa.me/{WA}"><h3>WhatsApp</h3><p>{PHONE}, быстрый ответ</p></a>
<a class="card" href="tel:{PHONE_TEL}"><h3>Телефон</h3><p>{PHONE}</p></a>
<a class="card" href="https://t.me/{TG}"><h3>Telegram</h3><p>@{TG}</p></a>
<a class="card" href="mailto:{EMAIL}"><h3>Почта</h3><p>{EMAIL}</p></a>
<a class="card" href="https://t.me/makebizchannel"><h3>Telegram-канал</h3><p>@makebizchannel</p></a>
<div class="card"><h3>Реквизиты</h3><p>MakeBiz Technologies FZE LLC, Ajman NuVentures Centre, рег. номер 2624215090888, Amber Gem Tower, Аджман, ОАЭ</p></div>
</div></div></section>
<section class="sec"><div class="wrap"><h2>Как с нами связаться быстрее</h2><div class="grid g3">
<div class="card"><h3>Нужен ответ сегодня</h3><p>Пишите в WhatsApp или Telegram @{TG}: отвечаем в рабочее время в течение часа</p></div>
<div class="card"><h3>Нужен расчёт</h3><p>Оставьте заявку с задачей: пришлём смету в дирхамах с ценой и сроком. Цены на основные услуги на странице <a href="{U('/ceny')}">Цены</a></p></div>
<div class="card"><h3>Хотите посмотреть живую систему</h3><p>Запишитесь на демонстрацию ИИ-агентов и BI: 30-40 минут, бесплатно</p></div></div></div></section>
{faq(ct_faq)}
{form_block('contacts', 'Оставьте заявку')}'''
built.append(page('/contacts', 'contacts', 'Контакты MakeBiz Technologies: WhatsApp, телефон, Telegram',
    f'Контакты MakeBiz Technologies в Дубае: WhatsApp и телефон {PHONE}, Telegram @{TG}, почта {EMAIL}. Битрикс24 и ИИ-агенты.',
    'contacts', ct_body, [{"@type": "ContactPage", "url": SITE + "/contacts"}], [('/', 'Главная'), ('/contacts', 'Контакты')], ct_faq))

exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'landings_ae.py'), encoding='utf-8').read())

# обвязка для журнала и новостей (server.js оборачивает их в новый дизайн)
os.makedirs(os.path.join(OUT, '_chrome'), exist_ok=True)
pv = '<div class="pv">Превью нового сайта · закрыто от поисковиков · <a href="/">текущий сайт</a></div>' if PREVIEW else ''
open(os.path.join(OUT, '_chrome', 'top.html'), 'w', encoding='utf-8').write('<div class="flag" aria-hidden="true"><i></i><i></i><i></i></div>' + pv + header('news').replace('href="#form"', 'href="' + U('/contacts') + '#form"'))
open(os.path.join(OUT, '_chrome', 'bottom.html'), 'w', encoding='utf-8').write(footer().replace('href="#form"', 'href="' + U('/contacts') + '#form"') + f'<script src="{U("/assets/site.js")}?v={V}" defer></script>')
open(os.path.join(OUT, '_chrome', 'form.html'), 'w', encoding='utf-8').write(form_block('', 'Обсудим задачу', 'Оставьте контакт, ответим в течение рабочего дня. Проведём короткую диагностику и скажем, с чего начать'))
open(os.path.join(OUT, '_chrome', 'head.html'), 'w', encoding='utf-8').write(f'<link rel="preload" href="{U("/assets/onest-cyrillic.woff2")}" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="{U("/assets/site.css")}?v={V}">')
print('built:', built)

# ассеты собирает publish_ae.sh (перекрашенный css, site.js ОАЭ)
