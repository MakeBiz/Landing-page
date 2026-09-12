#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Английская версия /ai-agents: разводим с makebiz.life (совпадало 40 строк из 50).
Тексты кнопок не трогаем, их ловит модуль призывов в mb-attr.js.

    python3 .seo/uae/diverge_ai_agents_en.py .
"""
import io, json, os, re, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
os.chdir(ROOT)
F = 'en/ai-agents.html'

PAIRS = [
    ('We start with the core and add new agents month by month for your tasks. This is not a deploy-it-and-forget-it system; it matures right alongside your business',
     'We start with the core and add roles month by month for your tasks. This is not a set-it-and-forget-it system: it grows together with the company'),
    ('The Conductor understands the request and brings in the right specialists. Permissions are granted precisely, and data is isolated between domains',
     'The Conductor understands the request and brings in the right specialists. Permissions are granted precisely, and data from your free zone and mainland entities never mixes'),
    ('The agent does the work itself: it launches the process, runs it, and reports back. It brings in a human only for contentious or high-stakes calls',
     'The agent does the work itself: it launches the process, runs it and reports back. It calls a human in only for contentious matters and large amounts'),
    ('Nothing to learn from scratch: people write the way they always have, and right beside them in Telegram lives an app with a dashboard and tasks',
     'There is nothing to relearn: people write the way they always have, and right beside them in Telegram lives an app with a dashboard and tasks'),
    ('A chat waits for a question and replies with text. An agent drives the process to a result on its own',
     'A chat waits to be asked and replies with text. An agent takes the process all the way to a result on its own'),
    ('Not slides, but working agents. We will map out your process, pick the roles, and calculate the cost',
     'Not slides, but working agents. We will map the process, pick the roles and price it in dirhams'),
    ('A dashboard by domain: finance, tasks, sales. Numbers from one database, not from gut feel',
     'A dashboard by area: finance, tasks, sales. Numbers from one database, not from gut feel'),
    ('Tasks with filters and statuses; tapping a task leads to actions via the Dispatcher',
     'Tasks with filters and statuses; a tap on a task leads to actions via the Dispatcher'),
    ('The agent team runs operations across eight areas, all connected to your CRM',
     'The agent team runs operations across eight areas and is wired into your Bitrix24'),
    ('A separate domain for family, with data isolated from business',
     'A separate domain for family, with data that never touches the business'),
    ('A big screen for standups shows the same data as your phone',
     'The standup screen shows exactly the same data as your phone'),
    ('a map of your business network, data as of today', 'a map of your business contacts, data as of today'),
    ('Hands over text, the rest is on the human', 'Hands over text, everything after that is on the human'),
    ('An AI staff department for your business,', 'An AI staff department for a company in the UAE,'),
    ('Takes facts only from a verified database', 'Takes facts only from your verified database'),
    ('Starts on its own by event and schedule', 'Starts by itself on an event or a schedule'),
    ('Makes things up when it does not know', 'Makes things up if it does not know'),
    ('AI-Agents · your AI staff department', 'AI-Agents · an AI staff department in the UAE'),
    ('Drives to a result and reports back', 'Takes it to a result and reports back'),
    ('on your phone and on the big screen', 'on your phone and on the standup screen'),
    ('domains: business, personal, family', 'domains: company, personal, family'),
    ('All the numbers from one database,', 'Every number from one database,'),
    ('from first touch to client support', 'from the first enquiry to client support'),
    ('This is not GPT in a window, it is', 'This is not GPT in a window, this is'),
    ('A live system, not a presentation', 'A live system, not a slide deck'),
    ('App and dashboard · already live', 'App and dashboard · live right now'),
    ('We will show you a live system', 'We will show a live system'),
    ('an employee who does the work', 'an employee that gets the work done'),
    ('How this differs from a chat', 'How an agent differs from a chat'),
    ('eight agents run the funnel', 'eight agents run the entire funnel'),
    ('Roles tailored to your task', 'Roles picked for your task'),
    ('single sign-in via Telegram', 'one sign-in for the whole team'),
    ('They do not make things up', 'They never make things up'),
    ('deployment on your server', 'deployed on your own server in the UAE'),
    ('Agent team · how it works', 'Agent team · how it is built'),
    ('This is the sales domain:', 'The sales domain:'),
    ('You do not configure it,', 'You do not set it up,'),
]

TPL_RE = re.compile(r'<script type="__bundler/template">(.*?)</script>', re.S)


def templates_ok(h):
    n = 0
    for m in TPL_RE.finditer(h):
        json.loads(m.group(1)); n += 1
    return n


def main():
    h = io.open(F, encoding='utf-8').read()
    n_tpl = templates_ok(h)
    before = h
    done = skipped = 0
    for old, new in PAIRS:
        assert old not in new, 'новая строка не должна содержать старую: %s' % old[:50]
        if old not in h:
            skipped += 1
            continue
        h = h.replace(old, new)
        done += 1
    assert templates_ok(h) == n_tpl, 'шаблон бандла перестал разбираться'
    if h != before:
        io.open(F, 'w', encoding='utf-8').write(h)
    print('%s: заменено %d, уже было %d, шаблонов разобрано %d' % (F, done, skipped, n_tpl))


if __name__ == '__main__':
    main()
