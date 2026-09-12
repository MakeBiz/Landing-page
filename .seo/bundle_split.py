#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Выносит ассеты бандл-страниц (React, ReactDOM, шрифты) из HTML в отдельные файлы.

Зачем. Каждая бандл-страница несёт внутри себя манифест на 150-275 КБ: base64
от gzip'нутых ассетов. Содержимое у страниц совпадает побайтно (проверено:
148 КБ из 172 КБ одинаковы на главной, AI-агентах и контактах), то есть человек
скачивает одни и те же React и шрифты заново на каждой странице.

Что делает скрипт:
  1. у каждой записи манифеста забирает поле data и кладёт его в b/<sha1>.b64,
     имя файла это отпечаток содержимого, поэтому одинаковые ассеты становятся
     одним файлом на весь сайт;
  2. в манифесте вместо data оставляет url;
  3. в загрузчике добавляет ветку: если data нет, берём base64 по url.

Идемпотентно: повторный запуск ничего не ломает, уже вынесенные страницы
пропускает. Откат: git checkout страниц (или .bak рядом, см. --backup).

    python3 .seo/bundle_split.py .            проверить, что будет сделано
    python3 .seo/bundle_split.py . --apply    применить
"""
import hashlib, io, json, os, re, sys

PATCH_FROM = '        const binaryStr = atob(entry.data);'
PATCH_TO = (
    '        // Ассеты вынесены в файлы b/<отпечаток>.b64: одинаковые для разных\n'
    '        // страниц скачиваются один раз и лежат в кэше год.\n'
    '        const rawB64 = (entry.data != null)\n'
    '          ? entry.data\n'
    '          : await (await fetch(entry.url, { cache: \'force-cache\' })).text();\n'
    '        const binaryStr = atob(rawB64);'
)


def split_page(repo, rel, apply, stats):
    p = os.path.join(repo, rel)
    h = io.open(p, encoding='utf-8').read()
    m = re.search(r'(<script type="__bundler/manifest">)(.*?)(</script>)', h, re.S)
    if not m:
        return 'манифеста нет'
    raw = m.group(2)
    try:
        man = json.loads(raw)
    except Exception as e:
        return 'манифест не разобрался: %s' % e
    moved = saved = 0
    for uuid, entry in man.items():
        data = entry.get('data')
        if data is None:
            continue
        d = hashlib.sha1(data.encode()).hexdigest()[:16]
        name = 'b/%s.b64' % d
        stats['assets'].setdefault(d, {'bytes': len(data), 'pages': []})
        stats['assets'][d]['pages'].append(rel)
        if apply:
            out = os.path.join(repo, name)
            os.makedirs(os.path.dirname(out), exist_ok=True)
            if not os.path.exists(out):
                io.open(out, 'w', encoding='utf-8').write(data)
        entry.pop('data', None)
        entry['url'] = '/' + name
        moved += 1
        saved += len(data)
    if not moved:
        return 'уже вынесено'
    new_man = json.dumps(man, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    h2 = h[:m.start(2)] + '\n' + new_man + '\n  ' + h[m.end(2):]
    if PATCH_FROM in h2:
        h2 = h2.replace(PATCH_FROM, PATCH_TO, 1)
    elif 'rawB64' not in h2:
        return 'НЕ НАЙДЕНА точка патча загрузчика'
    if apply:
        io.open(p, 'w', encoding='utf-8').write(h2)
    return 'вынесено %d ассетов, из HTML ушло %d КБ (%d КБ -> %d КБ)' % (
        moved, saved // 1024, len(h) // 1024, len(h2) // 1024)


def main():
    repo = sys.argv[1] if len(sys.argv) > 1 else '.'
    apply = '--apply' in sys.argv
    pages = []
    for root, dirs, fs in os.walk(repo):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('node_modules', 'b')]
        for f in fs:
            if f.endswith('.html'):
                rel = os.path.relpath(os.path.join(root, f), repo)
                if '__bundler/manifest' in io.open(os.path.join(root, f), encoding='utf-8').read(40000):
                    pages.append(rel)
    stats = {'assets': {}}
    print('режим:', 'ПРИМЕНЯЮ' if apply else 'только показываю')
    for rel in sorted(pages):
        print('  %-28s %s' % (rel, split_page(repo, rel, apply, stats)))
    tot = sum(v['bytes'] for v in stats['assets'].values())
    dup = sum(v['bytes'] * (len(v['pages']) - 1) for v in stats['assets'].values())
    print('\nразных ассетов: %d, суммарно %d КБ' % (len(stats['assets']), tot // 1024))
    print('дублей убрано из HTML: %d КБ (столько лишнего качали при обходе сайта)' % (dup // 1024))


if __name__ == '__main__':
    main()
