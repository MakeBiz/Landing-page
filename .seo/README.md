# SEO/GEO-инструменты сайта (папка скрыта от посетителей: сервер не отдаёт файлы с точкой)

Что здесь и зачем. Часть страниц рисуется скриптом (бандлы Claude Design: главная, AI-агенты, контакты RU/EN; кейсы из cases-data.js; калькулятор в iframe). Яндекс и AI-боты (ChatGPT, Perplexity, Claude) скрипты почти не исполняют, поэтому в исходный HTML кладём тот же текст статикой:

- `#mb-ssr` в начале body бандл-страниц: текст страницы для краулеров. Бандл при загрузке подменяет документ, посетитель блок не видит
- `#mb-ssr` на калькуляторе и `#mb-ssr-nav` на vector/vps: блок и тут же скрипт, который его удаляет
- `keysy/<slug>.html` и `en/keysy/<slug>.html`: снимок страницы кейса, движок кейсов перерисовывает его тем же содержимым. `keysy/case.html` стал запасным шаблоном с noindex
- `llms.txt`: визитка сайта для AI; `robots.txt`: AI-боты разрешены, `/api/` закрыт, Clean-param для Яндекса
- JSON-LD на каждой странице: Organization, WebSite, WebPage, BreadcrumbList, Service с ценами в AED, NewsArticle, CollectionPage, Article для кейсов

## Когда перегенерировать
- поменяли текст бандл-страницы или калькулятора: поправить `ssr_content.py`, запустить `build_c2.py`
- добавили кейс в `keysy/cases-data.js` (и EN): снимок кейсов (шаги 1-2), затем `build_b.py` и `build_d.py`
- новая страница или новость: `build_b.py` (разметка) и `build_d.py` (sitemap, llms.txt)
- поменяли title/description: `meta_config.py`, затем `build_a.py`
- цены и факты в разметке (`build_b.py`: SVC), `llms.txt` (`build_d.py`) и `ssr_content.py` должны совпадать со страницами

## Порядок (из корня репозитория, нужен Playwright с Chromium)
```
node .seo/serve.mjs . 8766 &                       # локальный сервер с маршрутизацией как у timeweb-server.js
node .seo/snap_cases.mjs /tmp/cases.json /keysy /en/keysy /keysy/<slug> /en/keysy/<slug> ...
python3 .seo/build_c1.py . /tmp/cases.json         # статические кейсы + предзаполненный список
python3 .seo/build_a.py .                          # title, description, og, заголовки EN
python3 .seo/build_b.py .                          # JSON-LD
python3 .seo/build_c2.py .                         # SSR-блоки
python3 .seo/build_d.py . $(date +%F)              # robots.txt, llms.txt, sitemap.xml
node .seo/validate.mjs sitemap.xml                 # все адреса: 200, есть H1, SSR не виден, нет ошибок и горизонтального скролла на 390px
```
Правка шаблона бандла идёт через `seo_lib.tpl_patch`/запись head с проверкой `json.loads`, строковой заменой вслепую бандл не трогать (белый экран).

## Блок «Частые вопросы» (добавлен 12 сен 2026)
- Вопросы и ответы лежат в `.seo/faq_data.py`, по одному списку на страницу
- `python3 .seo/build_faq.py` кладёт разметку FAQPage в блок `<!--mb-ld-->` и подключает `/mb-faq.js`
- `/mb-faq.js` рисует аккордеон из этой же разметки, поэтому видимый текст и текст для поисковиков совпадают всегда
- Порядок важен: если пересобираете страницы «О компании» через `.seo/company/build_company.py`, сразу после этого запускайте `build_faq.py`, иначе на них пропадёт FAQ
