# MakeBiz: сайт makebiztechnologies.com (RU + EN)

Статический сайт (HTML, CSS, JS без сборщика) и функции `api/*.js`. Русская версия лежит в корне (цены в AED), английская в `en/`.

## Хостинг и публикация
- Timeweb App Platform: Backend, Express, Node.js 24, Франкфурт. Деплой автоматически из ветки `main` этого репозитория, команда запуска `npm start`
- `timeweb-server.js`: чистые адреса (`/bitrix` отдаёт `bitrix.html`), 301 со старых адресов и со старого домена makebiztehnologies.com, шаблон кейсов `/keysy/<slug>`, заголовки безопасности и кэша, функции `/api/<имя>`
- Рабочая папка на Маке `Landing/makebiztehnologies`, публикатор `com.makebiztehnologies.autopublish` (скилл makebiz-github-setup): Claude кладёт файлы в папку и ставит сигнал `.publish-request`

## Функции и переменные окружения
- `api/lead.js`: заявки с форм в Telegram. `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`
- `api/post-to-channel.js`: посты в Telegram-канал. `TELEGRAM_CHANNEL_BOT_TOKEN`, `TELEGRAM_CHANNEL_ID`, `CHANNEL_POST_SECRET`

Секреты только в переменных окружения Timeweb, в код и в этот репозиторий их не пишем: он публичный
