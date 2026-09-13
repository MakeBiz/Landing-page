#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Не теряем заявку, когда сервер её не принял.

Сейчас /api/lead отвечает 500 (в Timeweb не заданы TELEGRAM_BOT_TOKEN и TELEGRAM_CHAT_ID),
и человек видит «напишите нам напрямую». Имя, телефон и задача, которые он уже ввёл,
при этом просто пропадают.

Скрипт заменяет этот текст на готовую ссылку в WhatsApp с подставленным сообщением:
одно касание, и заявка приходит целиком. Русская и английская версии.

Идемпотентно. Вставка проверяется на то, что она не попадает внутрь шаблона бандла.

    python3 .seo/uae/form_fallback.py .
"""
import io, os, re, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
os.chdir(ROOT)

TPL_RE = re.compile(r'<script type="__bundler/template">.*?</script>', re.S)

OLD_RU = ("$('mbcf-oktext').innerHTML = 'Заявку не удалось отправить автоматически. Напишите нам напрямую: "
          '<a href="https://t.me/Anton_MakeBiz" style="color:#16C15A">Telegram @Anton_MakeBiz</a> или '
          '<a href="https://wa.me/971502620927" style="color:#16C15A">WhatsApp +971 50 262 0927</a>\';')
OLD_EN = ("$('mbcf-oktext').innerHTML = 'We could not send your request automatically. Please write to us directly: "
          '<a href="https://t.me/Anton_MakeBiz" style="color:#16C15A">Telegram @Anton_MakeBiz</a> or '
          '<a href="https://wa.me/971502620927" style="color:#16C15A">WhatsApp +971 50 262 0927</a>\';')

NEW = "$('mbcf-oktext').innerHTML = mbcfHelp(payload);"

ANCHOR = '  function submitForm(){'

HELP_RU = (
    "  /* Сервер заявку не принял: собираем за человека готовое сообщение в WhatsApp, чтобы он не вводил всё заново */\n"
    "  function mbcfHelp(p){ var NL=String.fromCharCode(10); var t='Заявка с сайта'+NL+'Имя: '+(p.name||'')+NL+'Телефон: '+(p.phone||'');"
    " if(p.company) t+=NL+'Компания: '+p.company; if(p.telegram) t+=NL+'Telegram: '+p.telegram;"
    " if(p.automate) t+=NL+'Задача: '+p.automate; t+=NL+'Страница: '+(p.page||'');"
    " var w='https://wa.me/971502620927?text='+encodeURIComponent(t);"
    " return 'Заявку не удалось отправить автоматически. Отправьте её одним касанием: '"
    "+'<a href=\"'+w+'\" target=\"_blank\" rel=\"noopener\" style=\"color:#16C15A\">WhatsApp +971 50 262 0927</a>'"
    "+' или напишите в <a href=\"https://t.me/Anton_MakeBiz\" target=\"_blank\" rel=\"noopener\" style=\"color:#16C15A\">Telegram @Anton_MakeBiz</a>'; }\n"
)

HELP_EN = (
    "  /* The server did not take the request: we build a ready WhatsApp message so nothing has to be typed again */\n"
    "  function mbcfHelp(p){ var NL=String.fromCharCode(10); var t='Website request'+NL+'Name: '+(p.name||'')+NL+'Phone: '+(p.phone||'');"
    " if(p.company) t+=NL+'Company: '+p.company; if(p.telegram) t+=NL+'Telegram: '+p.telegram;"
    " if(p.automate) t+=NL+'Task: '+p.automate; t+=NL+'Page: '+(p.page||'');"
    " var w='https://wa.me/971502620927?text='+encodeURIComponent(t);"
    " return 'We could not send your request automatically. Send it in one tap: '"
    "+'<a href=\"'+w+'\" target=\"_blank\" rel=\"noopener\" style=\"color:#16C15A\">WhatsApp +971 50 262 0927</a>'"
    "+' or write to <a href=\"https://t.me/Anton_MakeBiz\" target=\"_blank\" rel=\"noopener\" style=\"color:#16C15A\">Telegram @Anton_MakeBiz</a>'; }\n"
)


def in_template(h, pos):
    for m in TPL_RE.finditer(h):
        if m.start() <= pos <= m.end():
            return True
    return False


def patch(f):
    h = io.open(f, encoding='utf-8').read()
    old, help_src = (OLD_EN, HELP_EN) if f.startswith('en/') else (OLD_RU, HELP_RU)
    if 'function mbcfHelp' in h and old not in h:
        return 'уже сделано'
    n = h.count(old)
    if n == 0:
        return 'формы нет'
    i = h.find(ANCHOR)
    if i < 0:
        return 'НЕ НАЙДЕНА точка вставки'
    if in_template(h, i):
        return 'точка вставки внутри шаблона бандла, пропускаю'
    h = h.replace(old, NEW)
    h = h[:i] + help_src + h[i:]
    io.open(f, 'w', encoding='utf-8').write(h)
    return 'заменено %d, помощник вставлен' % n


def main():
    files = []
    for root, dirs, fs in os.walk('.'):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('node_modules', 'b')]
        for x in fs:
            if x.endswith('.html'):
                files.append(os.path.relpath(os.path.join(root, x), '.'))
    for f in sorted(files):
        h = io.open(f, encoding='utf-8').read()
        if 'mbcf-oktext' not in h:
            continue
        print('%-28s %s' % (f, patch(f)))


if __name__ == '__main__':
    main()
