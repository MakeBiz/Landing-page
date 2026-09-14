#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Собирает самодостаточную копию страницы: один файл, который открывается с диска
и выглядит как живой сайт. Нужен, когда страницу отдают на переработку дизайна.

Что делает:
  1. возвращает в манифест бандлера сами ассеты (React, шрифты, рантайм),
     которые вынесены в b/<отпечаток>.b64;
  2. вшивает наши общие скрипты (mb-attr, mb-faq, движок кейсов) прямо в страницу;
  3. иконки и картинки оставляет ссылками: на вёрстку они не влияют.

    python3 .seo/uae/export_standalone.py . index.html ~/mnt/Landing/_inbox/makebiz-index.html
"""
import io, json, os, re, sys

ROOT = sys.argv[1]
PAGE = sys.argv[2]
OUT = os.path.expanduser(sys.argv[3])
os.chdir(ROOT)

INLINE = ['/mb-attr.js', '/mb-faq.js', '/keysy/cases-data.js', '/keysy/cases-engine.js']


def main():
    h = io.open(PAGE, encoding='utf-8').read()
    notes = []

    # 1. ассеты бандлера обратно в манифест
    m = re.search(r'(<script type="__bundler/manifest">)(.*?)(</script>)', h, re.S)
    if m:
        man = json.loads(m.group(2))
        back = 0
        for uid, e in man.items():
            if e.get('data') is None and e.get('url'):
                p = e['url'].lstrip('/')
                if os.path.exists(p):
                    e['data'] = io.open(p, encoding='utf-8').read()
                    e.pop('url', None)
                    back += 1
        new_man = json.dumps(man, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
        h = h[:m.start(2)] + '\n' + new_man + '\n  ' + h[m.end(2):]
        notes.append('ассетов вшито обратно: %d' % back)

    # 2. наши общие скрипты внутрь файла
    for ref in INLINE:
        path = ref.lstrip('/')
        if not os.path.exists(path):
            continue
        src = io.open(path, encoding='utf-8').read()
        pat = re.compile(r'<script[^>]*src="' + re.escape(ref) + r'(\?v=[0-9a-f]+)?"[^>]*>\s*</script>')
        if pat.search(h):
            h = pat.sub(lambda _: '<script>\n' + src + '\n</script>', h, count=1)
            notes.append('вшит %s' % ref)

    # 3. шрифты: на статичных страницах они тянутся с Google Fonts, а в офлайне это пустое место.
    #    Берём те же woff2 из бандла главной и вшиваем их прямо в файл.
    if 'fonts.googleapis.com' in h:
        import base64 as _b64, gzip as _gz
        src_page = io.open('index.html', encoding='utf-8').read()
        m2 = re.search(r'<script type="__bundler/manifest">(.*?)</script>', src_page, re.S)
        faces = []
        if m2:
            weights = {}
            for uid, e in json.loads(m2.group(1)).items():
                if e.get('mime') != 'font/woff2':
                    continue
                p2 = (e.get('url') or '').lstrip('/')
                raw = None
                if p2 and os.path.exists(p2):
                    raw = _b64.b64decode(io.open(p2, encoding='utf-8').read())
                elif e.get('data'):
                    raw = _b64.b64decode(e['data'])
                if raw is None:
                    continue
                if e.get('compressed'):
                    raw = _gz.decompress(raw)
                weights.setdefault(len(raw), []).append(raw)
            # в бандле по два файла на начертание (latin и latin-ext); берём тот, что больше
            picked = sorted(weights.items(), key=lambda kv: -kv[0])[:6]
            for i, (size, blobs) in enumerate(picked):
                w = [300, 400, 700][i % 3]
                b = _b64.b64encode(blobs[0]).decode()
                faces.append("@font-face{font-family:'Oxygen';font-style:normal;font-weight:%d;"
                             "font-display:swap;src:url(data:font/woff2;base64,%s) format('woff2');}" % (w, b))
        if faces:
            h = h.replace('</head>', '<style>' + ''.join(faces) + '</style>\n</head>', 1)
            notes.append('вшито начертаний Oxygen: %d' % len(faces))

    d = os.path.dirname(OUT)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    io.open(OUT, 'w', encoding='utf-8').write(h)
    left = sorted(set(re.findall(r'(?:src|href)="(/[^"]+\.(?:js|css))"', h)))
    print('\n'.join(notes))
    print('готово: %s (%d КБ)' % (OUT, len(h.encode('utf-8')) // 1024))
    print('осталось ссылок на внешние скрипты и стили: %s' % (', '.join(left) if left else 'нет'))


if __name__ == '__main__':
    main()
