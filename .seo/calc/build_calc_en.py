#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Вшивает английский словарь агентов в данные калькулятора и включает выбор языка по адресу.

Приложение уже умеет английский: метод tag(a,f) берёт перевод из I18N[lang].agent[имя][поле]
и откатывается на русское значение, если перевода нет. Нам остаётся положить туда словарь.

Переводы лежат рядом: en_01..en_04.json (по агентам), en_arch.json (архетипы и инструменты).
Шаги и момент включения у агентов зависят от архетипа, поэтому собираются из en_arch.

    python3 .seo/calc/build_calc_en.py .
"""
import base64, gzip, hashlib, io, json, os, re, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
PAGE = os.path.join(ROOT, 'calculator-agents-app.html')
CALC = os.path.join(ROOT, '.seo/calc')


def rd(p):
    return io.open(p, encoding='utf-8').read()


def main():
    html = rd(PAGE)
    man = json.loads(re.search(r'<script type="__bundler/manifest">(.*?)</script>', html, re.S).group(1))

    # 1. находим ассет с данными витрины
    uid = None
    for k, e in man.items():
        if not e.get('url'):
            continue
        raw = base64.b64decode(rd(os.path.join(ROOT, e['url'].lstrip('/'))))
        if e.get('compressed'):
            raw = gzip.decompress(raw)
        if raw[:80].decode('utf-8', 'ignore').startswith('// Данные витрины MakeBiz'):
            uid, src, ent = k, raw.decode('utf-8'), e
            break
    if not uid:
        raise SystemExit('НЕ НАЙДЕН ассет с данными витрины')

    # 2. собираем словарь
    agents = {}
    for f in sorted(os.listdir(CALC)):
        if re.match(r'^en_\d+\.json$', f):
            agents.update(json.load(io.open(os.path.join(CALC, f), encoding='utf-8')))
    arch = json.load(io.open(os.path.join(CALC, 'en_arch.json'), encoding='utf-8'))

    i = src.find('var SHOP = ') + len('var SHOP = ')
    j = src.find('\nvar I18N')
    shop = json.loads(src[i:j].rstrip().rstrip(';'))
    missing = [a['n'] for a in shop['agents'] if a['n'] not in agents]
    if missing:
        raise SystemExit('НЕТ ПЕРЕВОДА для %d агентов: %s' % (len(missing), ', '.join(missing[:5])))

    dic = {}
    for a in shop['agents']:
        en = dict(agents[a['n']])
        ar = arch['arch'].get(a['arch'])
        if ar:
            en['when'] = ar['when']
            en['steps'] = ar['steps']
            en['archru'] = ar['archru']
        if a.get('tools'):
            en['tools'] = [arch['tools'].get(t, t) for t in a['tools']]
        dic[a['n']] = en

    # 3. вписываем agent: в I18N.en (идемпотентно: старый блок сначала убираем)
    src = re.sub(r'\n  agent:\{.*?\n  \},\n(?=  ui:)', '\n', src, flags=re.S)
    anchor = 'var I18N = {\nen:{\n'
    if anchor not in src:
        raise SystemExit('НЕ НАЙДЕН блок I18N.en')
    block = '  agent:' + json.dumps(dic, ensure_ascii=False, separators=(',', ':')) + ',\n'
    src = src.replace(anchor, anchor + block, 1)

    # 4. пакуем обратно
    packed = gzip.compress(src.encode('utf-8'), 9)
    b64 = base64.b64encode(packed).decode()
    d = hashlib.sha1(b64.encode()).hexdigest()[:16]
    new_rel = 'b/%s.b64' % d
    io.open(os.path.join(ROOT, new_rel), 'w', encoding='utf-8').write(b64)
    old = ent['url']
    ent['url'] = '/' + new_rel
    new_man = json.dumps(man, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    m = re.search(r'(<script type="__bundler/manifest">)(.*?)(</script>)', html, re.S)
    html = html[:m.start(2)] + '\n' + new_man + '\n  ' + html[m.end(2):]

    # 5. язык из адреса: /calculator-agents-app?lang=en открывает английскую версию
    before = "state = {ready:false,lang:'ru',"
    after = ("state = {ready:false,lang:(typeof location!=='undefined'&&/[?&]lang=en/.test(location.search))?'en':'ru',")
    if before in html:
        html = html.replace(before, after, 1)
        lang = 'включён выбор языка по адресу'
    elif 'lang=en/.test' in html:
        lang = 'выбор языка уже был включён'
    else:
        raise SystemExit('НЕ НАЙДЕНО начальное состояние lang')

    io.open(PAGE, 'w', encoding='utf-8').write(html)
    print('словарь на %d агентов вшит' % len(dic))
    print('данные витрины: %s -> %s (%d КБ base64)' % (old, ent['url'], len(b64) // 1024))
    print(lang)
    print('ВАЖНО: старый файл %s больше не используется, удалить вручную при уборке' % old)


if __name__ == '__main__':
    main()
