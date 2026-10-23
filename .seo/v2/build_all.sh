#!/bin/bash
# Сборка нового makebiztechnologies.com (дизайн в цветах флага ОАЭ).
#   bash .seo/v2/build_all.sh preview   -> папка v2/ (превью https://makebiztechnologies.com/v2/, noindex, без счётчиков)
#   bash .seo/v2/build_all.sh live      -> папка site-v2/ (боевой сайт, работает, когда в корне есть файл .v2-live)
# Собирает только HTML, css и js. Картинки (img/, media/) и шрифты лежат в папке результата и не трогаются.
# Страницы-решения берутся из .seo/uae/link_solutions.py, новости из news/ и en/news/: их файлы не меняются,
# timeweb-server.js оборачивает их в шапку и подвал нового сайта при отдаче
set -e
V2="$(cd "$(dirname "$0")" && pwd)"; SITE="$(cd "$V2/../.." && pwd)"
MODE=${1:-live}
if [ "$MODE" = preview ]; then OUTD=v2; B=/v2; PV=1; else OUTD=site-v2; B=; PV=0; fi
VER=${MB_V:-$(cat "$V2/site-base.css" "$V2/dark_uae.css" "$V2/site-src.js" "$V2/bg_beams.js" "$V2/make_site_ae.py" "$V2/make_site_en_ae.py" | cksum | cut -c1-8)}
export MB_V=$VER MB_BASE=$B MB_OUT=$OUTD MB_PREVIEW=$PV MB_SITE="$SITE"
# каталог провайдеров VPS из кабинета MakeBiz (как у servercalc.com): кабинет не ответил, остаётся прошлый файл
if curl -s -m 15 -f "https://makebiz-makebiz-platform-3628.twc1.net/catalog/servercalc-com.json" -o "$V2/data/.vps-catalog.tmp" && grep -q '"hidden"' "$V2/data/.vps-catalog.tmp"; then cat "$V2/data/.vps-catalog.tmp" > "$V2/data/vps-catalog.json"; fi
python3 "$V2/build_ae.py" "$SITE" >/dev/null
python3 "$V2/build_en_ae.py" "$SITE" >/dev/null
D="$SITE/$OUTD"; mkdir -p "$D/assets"
T=$(mktemp -d)
python3 "$V2/make_site_ae.py" "$V2/site-src.js" "$T/ru.js" >/dev/null
python3 "$V2/make_site_en_ae.py" "$T/ru.js" "$T/en.js" >/dev/null
cat "$V2/site-base.css" "$V2/dark_uae.css" > "$D/assets/site.css"
cat "$T/ru.js" "$V2/bg_beams.js" > "$D/assets/site.js"
cat "$T/en.js" "$V2/bg_beams.js" > "$D/assets/site-en.js"
if [ "$MODE" = live ]; then python3 "$V2/make_seo_ae.py" "$SITE" "$D"; fi
echo "$MODE: $OUTD, v=$VER, страниц $(find "$D" -name '*.html' -not -path '*/_chrome/*' | wc -l | tr -d ' ')"
