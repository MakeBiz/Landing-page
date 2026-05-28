# MakeBiz — сайт

Премиальный B2B-сайт MakeBiz: внедрение ИИ, CRM, BI-аналитики и автоматизации.

## Структура

```
.
├── index.html        # Главная + вкладки: О компании, Партнёрам, Контакты
├── openclaw.html     # Страница продукта OpenClaw
├── vector.html       # Страница продукта Vector
├── intdoc.html       # Страница продукта IntDoc
├── bitrix.html       # Страница продукта Bitrix
├── api/
│   └── lead.js       # Serverless-функция: приём заявок и отправка в Telegram
├── vercel.json       # Настройки маршрутов (чистые URL)
├── package.json
└── .gitignore
```

## Адреса страниц

| URL | Страница |
|-----|----------|
| `/`          | Главная |
| `/company`   | О компании |
| `/openclaw`  | OpenClaw |
| `/vector`    | Vector |
| `/intdoc`    | IntDoc |
| `/bitrix`    | Bitrix |
| `/partners`  | Партнёрам |
| `/contacts`  | Контакты |

Каждая страница — отдельный HTML-файл. Благодаря `cleanUrls` в `vercel.json`
файлы открываются по чистым адресам без расширения `.html`.
Между вкладками также работает мгновенная JS-навигация (без перезагрузки).

## Деплой на Vercel

1. Залить этот репозиторий на GitHub.
2. На vercel.com → **Add New → Project** → импортировать репозиторий с GitHub.
3. Framework Preset: **Other** (статический сайт). Build Command и Output — оставить пустыми.
4. **Обязательно** добавить переменные окружения (Settings → Environment Variables):
   - `TELEGRAM_BOT_TOKEN` — токен бота от @BotFather
   - `TELEGRAM_CHAT_ID` — ID группы/чата для заявок (например `-100xxxxxxxxxx`)
5. Deploy. После добавления переменных — сделать **Redeploy**.

## Формы заявок

Все три формы (Обсудить проект / Стать партнёром / Контакты) отправляют данные
на `/api/lead`, откуда они уходят в Telegram.

⚠️ **Безопасность:** токен бота в коде НЕ хранится — только в переменных окружения Vercel.
Если ваш токен уже был где-то засвечен (например, в переписке) — перевыпустите его
в @BotFather командой `/revoke` и впишите новый в переменную `TELEGRAM_BOT_TOKEN`.

## Как получить TELEGRAM_CHAT_ID группы

1. Добавьте бота в группу.
2. Отправьте в группу любое сообщение.
3. Откройте `https://api.telegram.org/bot<ВАШ_ТОКЕН>/getUpdates`
4. Найдите `"chat":{"id":-100...}` — это и есть chat_id.
