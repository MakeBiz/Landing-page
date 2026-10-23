"""Провайдеры VPS для страницы /vps: данные каталога servercalc.com.
- data/vps-providers.json и data/vps-plans.json: снимок из репозитория vps-catalog-en (servercalc.com)
- кого показывать, закреп и приоритет: кабинет MakeBiz (Маркетинг · Провайдеры на сайтах, сайт servercalc-com),
  перед сборкой build_all.sh скачивает его в data/vps-catalog.json. Кабинет не ответил: берём прошлый файл
- цена тарифа показывается, только если её проверяли не дольше 30 дней назад (то же правило, что на servercalc.com)
"""
import os, json, datetime
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode
HERE = os.path.dirname(os.path.abspath(__file__))
STALE_DAYS = 30
GEO = {'ru': ('Россия', 'Russia'), 'eu': ('Европа', 'Europe'), 'us': ('США', 'USA'), 'uae': ('ОАЭ', 'UAE'),
       'asia': ('Азия', 'Asia'), 'global': ('по всему миру', 'worldwide'), 'kz': ('Казахстан', 'Kazakhstan')}
CUR = {'USD': '$', 'EUR': '€', 'AED': 'AED ', 'RUB': '₽'}

def _load(n, default):
    try:
        return json.load(open(os.path.join(HERE, 'data', n), encoding='utf-8'))
    except Exception:
        return default

def link(p, lang):
    """партнёрская ссылка с меткой (метка до якоря), без метки у noUtm, обычный сайт без партнёрки"""
    if not (p.get('affiliateStatus') == 'active' and p.get('url')):
        return p.get('site'), 'nofollow noopener'
    if p.get('noUtm'):
        return p['url'], 'sponsored nofollow noopener'
    u = urlsplit(p['url'])
    q = [(k, v) for k, v in parse_qsl(u.query, keep_blank_values=True) if not k.startswith('utm_')]
    q += [('utm_source', 'makebiztechnologies'), ('utm_medium', 'eng' if lang == 'en' else 'ru'), ('utm_campaign', 'vps'), ('utm_content', p['slug'])]
    return urlunsplit((u.scheme, u.netloc, u.path, urlencode(q), u.fragment)), 'sponsored nofollow noopener'

def providers(lang='ru', today=None):
    today = today or datetime.date.today()
    P = _load('vps-providers.json', []); L = _load('vps-plans.json', []); C = _load('vps-catalog.json', {})
    hidden = set(C.get('hidden') or []); rank = C.get('rank') or {}; pinned = C.get('pinned') or []
    out = []
    for p in P:
        if p['slug'] in hidden: continue
        if lang == 'en' and not p.get('descriptionEn'): continue
        fresh = [x for x in L if x.get('providerSlug') == p['slug'] and x.get('verifiedAt')
                 and (today - datetime.date.fromisoformat(x['verifiedAt'])).days <= STALE_DAYS and x.get('currency') in ('USD', 'EUR', 'AED')]
        cheap = min(fresh, key=lambda x: x['price'] * (1 if x['currency'] == 'USD' else 1.1 if x['currency'] == 'EUR' else 0.27)) if fresh else None
        href, rel = link(p, lang)
        feats = p.get('features') or {}
        out.append(dict(
            slug=p['slug'], name=p['name'], href=href, rel=rel,
            desc=(p.get('descriptionEn') if lang == 'en' else p.get('description')) or '',
            pros=(p.get('prosEn') if lang == 'en' else p.get('pros')) or [],
            geos=[GEO.get(g, (g, g))[1 if lang == 'en' else 0] for g in p.get('geos', [])],
            uae='uae' in p.get('geos', []),
            feats=[(n_ru, n_en) for k, n_ru, n_en in (('ddos', 'защита от DDoS', 'DDoS protection'), ('backup', 'бэкапы', 'backups'), ('hourly', 'почасовая оплата', 'hourly billing'), ('panel', 'панель управления', 'control panel')) if feats.get(k)],
            plan=cheap, pinned=p['slug'] in pinned, rank=rank.get(p['slug'], 99),
            verified=max([x['verifiedAt'] for x in fresh], default=''),
        ))
    out.sort(key=lambda d: (d['rank'], (d['plan']['price'] if d['plan'] else 9999), d['name']))
    return out

def price_text(plan, lang):
    if not plan: return ''
    v = plan['price']; v = int(v) if float(v).is_integer() else v
    s = f"{CUR.get(plan['currency'], plan['currency'] + ' ')}{v}"
    spec = f"{plan['cpu']} vCPU · {plan['ram']} GB · {plan['disk']} GB"
    return (f'from {s} a month', spec) if lang == 'en' else (f'от {s} в месяц', spec.replace('GB', 'ГБ'))
