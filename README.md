# MakeBiz — сайт (RU + EN), деплой на Vercel

Премиальный B2B-сайт MakeBiz. Чистый HTML + CSS + ванильный JS, без фреймворков.
Заявки с форм уходят в Telegram через серверную функцию `api/lead.js`.

## Структура

```
/
├── index.html          → главная (RU)
├── bitrix.html         → Bitrix24 (RU)
├── openclaw.html       → OpenClaw (RU)
├── vector.html         → Vector (RU)
├── intdoc.html         → IntDoc (RU)
├── privacy.html        → Политика конфиденциальности (RU)
├── en/
│   ├── index.html      → главная (EN, готова)
│   ├── bitrix.html     → Bitrix24 (EN, готова)
│   ├── openclaw.html   → заглушка «English version is on the way»
│   ├── vector.html     → заглушка
│   ├── intdoc.html     → заглушка
│   └── privacy.html    → Privacy Policy (EN)
├── api/
│   └── lead.js         → приём формы → Telegram
├── vercel.json         → cleanUrls (адреса без .html)
└── package.json
```

URL после деплоя: `/`, `/bitrix`, `/openclaw`, `/vector`, `/intdoc`, `/privacy`, `/en/`, `/en/bitrix`, `/en/privacy` и т.д.

## Что входит в этот сайт

- Кейсы с метриками на каждой продуктовой странице (Bitrix, OpenClaw, Vector, IntDoc)
- Переключатель RU/EN в шапке всех страниц
- Рабочие формы на всех страницах → заявки падают в Telegram
- Страница политики конфиденциальности + ссылка в подвале каждой страницы + строка согласия у каждой формы (требование Google Ads)

## Деплой

1. Залить ВСЕ файлы из этой папки в репозиторий GitHub (заменив старые).
2. В Vercel проект подхватит изменения автоматически.
3. Задать переменные окружения (см. ниже) → Redeploy.

## Подключение Telegram (чтобы падали заявки)

Токен и chat_id хранятся в переменных окружения Vercel, в коде их нет.

В Vercel → Settings → Environment Variables добавить:
- `TELEGRAM_BOT_TOKEN` = токен из @BotFather
- `TELEGRAM_CHAT_ID` = chat_id (личный или id группы со знаком минус)

После добавления переменных — Redeploy.

Проверка через терминал:
```
curl -X POST https://makebiztehnologies.com/api/lead -H "Content-Type: application/json" -d '{"form":"intdoc","name":"Test","telegram":"@test"}'
```
Должно вернуть `{"ok":true}` и заявка придёт в Telegram.

## Осталось доделать (опционально)

- EN-страницы OpenClaw, Vector, IntDoc — пока заглушки, можно собрать по образцу en/bitrix.html
- В политике конфиденциальности контакт — Telegram и телефон; при желании добавить e-mail
