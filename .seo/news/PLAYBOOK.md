# Лента makebiztechnologies.com: как выпускается новость (v2, с 23.10.2026)

Две новости в неделю, понедельник и четверг, сразу на русском и английском.
Одна статья за запуск. Всё делается в папке STAGE на Маке Антона через мост,
публикация файлом `.publish-request`, проверка живого сайта через WebFetch из облака.

## Куда что кладётся

| Что | Где |
|---|---|
| План тем | `.seo/news/topics.json` |
| Данные статьи | `.seo/news/articles/<slug>.json` |
| Сборщик страниц | `.seo/news/build_news.py` |
| Обложка | `.seo/news/make_cover.py` → `news/<cover>.webp` и `.jpg` |
| Готовые страницы | `news/<slug>.html`, `en/news/<slug>.html` |
| Лента | `news.html`, `en/news.html` (лид + сетка) |

## Порядок

1. **Тема.** Из `topics.json` берём первую со `status: planned`. Рубрику не повторяем
   два выпуска подряд: если у предыдущей опубликованной темы та же `cat`, берём следующую.
2. **Факты.** Всё, что уходит в текст, должно быть правдой и совпадать с сайтом.
   Цены только со страницы /ceny (на 23.10.2026): настройка CRM Битрикс24 от 10 000 AED, час работы 200 AED,
   поддержка 1 250 / 2 300 / 4 200 AED в месяц (5 / 10 / 20 часов, час сверх пакета 250 AED),
   интеграция с учётной системой от 10 000 AED, WhatsApp или мессенджер 500 AED, BI-аналитика от 1 000 AED,
   один ИИ-агент от 5 000 AED (пакет «Бизнес» 10 000 AED, обслуживание 10% в месяц),
   речевая аналитика звонков 1 000 / 1 700 / от 4 000 AED в месяц. Лицензии как на /bitrix-licenses.
   Свежие внешние факты проверяем поиском по первоисточнику, регуляторику ОАЭ (VAT, PDPL, free zone)
   только с источником и датой. Никаких выдуманных цифр, кейсов и клиентов.
3. **Статья.** Файл `.seo/news/articles/<slug>.json` по образцу
   `vnedrenie-bitrix24-v-oae-otlichiya.json`: `date`, `read`, `cat`, `cover`,
   `cover_alt_ru`, `cover_alt_en`, блоки `ru` и `en` с полями
   `title`, `desc`, `cta_b`, `cta_p`, `body`.
   - `body` это HTML: `<p>` и `<h2>`, 350-700 слов, первый абзац сразу отвечает на вопрос заголовка
     (2-3 предложения с цифрой: это цитируют нейросети)
   - **денежный вывод обязателен**: отдельный `<h2>` «Что это значит для бюджета» / "What it means for your budget":
     что меняется в деньгах, сроках или выручке читателя. Без него новость не выпускаем
   - в конце `body` блок «Коротко» из 2-4 вопросов и ответов: `<h2>Коротко</h2>` и пары `<p><b>Вопрос?</b> Ответ</p>`
     (EN: `<h2>Quick answers</h2>`)
   - 2-4 внутренние ссылки только на страницы сайта v2: `/bitrix`, `/bitrix-support`, `/bitrix-messengers`,
     `/bitrix-integrations`, `/bitrix-licenses`, `/bitrix-korobka`, `/bi-analitika`, `/ai-agents`, `/ai-agents/rop`,
     `/ai-agents/zvonki`, `/ai-agents/hr`, `/ai-agents/zakupki`, `/ai-agents/marketing`, `/ai-agents/finansy`,
     `/ai-agents/svyaznoy`, `/keysy`, `/ceny`, `/o-kompanii`, `/contacts`, страницы-решения `/bitrix-real-estate`,
     `/bitrix-vat-einvoicing`, `/bitrix-telephony`, `/bitrix-vs-zoho`, `/bitrix-distribution`, `/bitrix-clinics`,
     `/bitrix-migration`, `/bitrix-business-setup` и соседние `/news/<slug>`.
     В английской версии префикс `/en`, но слаги EN другие: `/en/bitrix-on-premise`, `/en/bi-analytics`,
     `/en/cases`, `/en/pricing`, `/en/about`. Перед публикацией проверь, что файл страницы есть в `site-v2/` или в корне
   - НЕ ссылаться на `/vector`, `/intdoc`, `/calculator-agents`, `/bitrix-whatsapp`, `/bitrix-accounting`, `/bitrix-1c` (это 301)
   - бренд Vector не называем, пишем «речевая аналитика»; слово OpenClaw не используем; Instagram и Facebook не называем
   - UTM: внутренние ссылки без меток. Ссылка на makebiz.life:
     `?utm_source=makebiztechnologies&utm_medium=news&utm_campaign=<slug>&utm_content=<место>`. Внешние только на первоисточник
   - `cta_b` и `cta_p`: предложение под тему новости («Посчитаем VAT-счета в вашем Битрикс24»), не общее «оставьте заявку».
     Форму заявки сервер ставит сам при отдаче страницы (`form=site-ae-news...`)
   - `desc` до 160 знаков, `title` до 65 знаков вместе с ` · MakeBiz`
   - длинные тире не используем нигде, кавычки « »
   - slug латиницей, только строчные буквы, цифры и дефис
4. **Обложка.** `python3 .seo/news/make_cover.py "<цвет рубрики из topics.json>" <cover> news`
5. **Сборка.** Из корня репозитория:
   ```
   python3 .seo/news/build_news.py . <slug> --lead
   python3 .seo/build_a.py .
   python3 .seo/build_b.py .
   python3 .seo/build_d.py . $(date +%F)
   python3 .seo/build_faq.py
   ```
   `--lead` делает новость крупной карточкой сверху ленты, прежний лид уезжает в сетку.
   Сборщик идемпотентный: повторный запуск не плодит дубли.
6. **Публикация.** `printf '<сообщение коммита>\n' > .publish-request`, затем ждать.
   Деплой Timeweb занимает от двух до восьми минут. Статус в `.publish-status`.
7. **Проверка живого сайта.** Только через WebFetch из облака (Мак наружу не ходит):
   `https://makebiztechnologies.com/news/<slug>` и `/en/news/<slug>` должны вернуть заголовок
   статьи, `sitemap.xml` должен содержать оба адреса. Без этой проверки писать «опубликовано» нельзя.
8. **Состояние.** В `topics.json` теме ставим `status: used`, `used_slug`, `used_date`.
9. **IndexNow.** Сервер после деплоя сам отправляет адреса из sitemap, вручную ничего слать не нужно.

## Чего не делаем

- Не трогаем `timeweb-server.js`, `mb-attr.js`, `mb-chrome.js`, бандл-страницы и шаблоны кейсов
- Не выдумываем клиентов, цифры и результаты, не называем компании, которых нет в кейсах
- Не публикуем больше одной статьи за запуск
- Не пишем «опубликовано», пока WebFetch не показал живую страницу
