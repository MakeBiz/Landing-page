# Новый makebiztechnologies.com (v2)

Генератор нового сайта: RU `build_ae.py`, EN `build_en_ae.py`, общий скрипт `build_all.sh` (режимы preview и live).

- Превью: `bash .seo/v2/build_all.sh preview` -> `v2/`, адрес https://makebiztechnologies.com/v2/
- Боевой: `bash .seo/v2/build_all.sh live` -> `site-v2/`. Сервер берёт страницы из `site-v2/` первыми, только если в корне есть файл `.v2-live`
- Старые сборщики `.seo/build_*.py` и конвейеры новостей и решений пишут в корень и `site-v2/` не трогают. `build_d.py` в конце сам вызывает `build_all.sh live`, если есть `.v2-live`: так новая страница-решение попадает в блок на /bitrix, а новость в sitemap.xml и llms.txt
- Цены, контакты, юрлицо: константы в начале `build_ae.py` и `build_en_ae.py`. Лицензии Битрикс24: цены bitrix24.ae в USD, AED по курсу 3,6725
- EN-адреса: `en_slugs.py` (/en/bitrix-on-premise, /en/bi-analytics, /en/cases, /en/pricing, /en/about)
- Без длинных тире, без слова OpenClaw, Instagram и Facebook не называем (пишем «соцсети»)
