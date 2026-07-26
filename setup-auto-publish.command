#!/bin/bash
# MakeBiz — установка публикатора «по запросу» (запустить ОДИН раз, двойным кликом).
# Само ничего не выкладывает: публикует только когда ассистент ставит сигнал по твоей команде.
set -euo pipefail

STAGE="/Users/anton/Мой диск/AXE NEW/MakeBizTehnologies/MakeBizTehnologies (1)/_upload-to-github"
AUTO="$HOME/makebiz-auto"
PLIST="$HOME/Library/LaunchAgents/com.makebiz.autopublish.plist"
mkdir -p "$AUTO" "$HOME/Library/LaunchAgents"

echo "=================================================="
echo "  MakeBiz — публикация по запросу"
echo "=================================================="

command -v git >/dev/null 2>&1 || { echo "Нет git. Установите: xcode-select --install"; read -r -p "Enter..."; exit 1; }

{ printf 'STAGE="'; printf '%s' "$STAGE"; printf '"\n'; } > "$AUTO/config"

cat > "$AUTO/autopublish.sh" <<'WORKER'
#!/bin/bash
# MakeBiz — публикатор «по запросу». launchd дёргает его часто, но он ПУБЛИКУЕТ
# только когда в папке есть файл-сигнал .publish-request (его ставит ассистент по твоей команде).
set -uo pipefail
AUTO="$HOME/makebiz-auto"
[ -f "$AUTO/config" ] && source "$AUTO/config"
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
REPO_DIR="$HOME/makebiz-landing-repo"
REPO_URL="https://github.com/MakeBiz/Landing-page.git"
LOG="$AUTO/autopublish.log"
LOCK="$AUTO/.lock"
log(){ echo "$(date '+%F %T') $*" >> "$LOG"; }

[ -n "${STAGE:-}" ] || exit 1
[ -d "$STAGE" ] || exit 0
TRIGGER="$STAGE/.publish-request"
STATUS="$STAGE/.publish-status"
FAILS="$AUTO/fails.count"

# публикуем ТОЛЬКО по сигналу
[ -e "$TRIGGER" ] || exit 0

if ! mkdir "$LOCK" 2>/dev/null; then exit 0; fi
trap 'rmdir "$LOCK" 2>/dev/null' EXIT

command -v git >/dev/null 2>&1 || { log "git не найден"; exit 1; }
if [ ! -d "$REPO_DIR/.git" ]; then
  git clone "$REPO_URL" "$REPO_DIR" >>"$LOG" 2>&1 || { log "clone не удался"; exit 1; }
fi
cd "$REPO_DIR" || exit 1
git fetch origin main --quiet >>"$LOG" 2>&1
git checkout -q main >>"$LOG" 2>&1
git reset --hard origin/main --quiet >>"$LOG" 2>&1
rsync -a --exclude='.git' --exclude='*.command' --exclude='.DS_Store' --exclude='.publish-request' --exclude='.publish-status' --exclude='PUBLISH-FAILED.txt' "$STAGE"/ "$REPO_DIR"/ >>"$LOG" 2>&1
git add -A
if git diff --staged --quiet; then
  rm -f "$TRIGGER"; echo "OK (без изменений) $(date '+%F %H:%M')" > "$STATUS"; log "запрос: изменений нет"; exit 0
fi
git commit -q -m "Публикация по запросу $(date '+%F %H:%M')" >>"$LOG" 2>&1
if git push -q origin main >>"$LOG" 2>&1; then
  rm -f "$TRIGGER" "$FAILS" "$STAGE/PUBLISH-FAILED.txt" 2>/dev/null
  echo "OK опубликовано $(date '+%F %H:%M')" > "$STATUS"
  log "OK опубликовано по запросу"
else
  n=$(( $(cat "$FAILS" 2>/dev/null || echo 0) + 1 )); echo "$n" > "$FAILS"
  log "push не прошёл (попытка $n)"
  if [ "$n" -ge 5 ]; then
    rm -f "$TRIGGER"; echo "0" > "$FAILS"
    echo "Публикация не удалась $(date '+%F %H:%M'). Нужен вход: gh auth login, затем повтори запрос." > "$STAGE/PUBLISH-FAILED.txt"
    log "сдаюсь после 5 попыток — нужен gh auth login"
  fi
fi
WORKER
chmod +x "$AUTO/autopublish.sh"

cat > "$PLIST" <<PL
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.makebiz.autopublish</string>
  <key>ProgramArguments</key>
  <array><string>/bin/bash</string><string>$AUTO/autopublish.sh</string></array>
  <key>StartInterval</key><integer>30</integer>
  <key>WatchPaths</key><array><string>$STAGE</string></array>
  <key>RunAtLoad</key><false/>
  <key>StandardOutPath</key><string>$AUTO/launchd.out.log</string>
  <key>StandardErrorPath</key><string>$AUTO/launchd.err.log</string>
</dict>
</plist>
PL

launchctl unload "$PLIST" 2>/dev/null || true
launchctl load "$PLIST"

# Проверка доступа к GitHub БЕЗ публикации
echo "→ Проверяю вход в GitHub (ничего не публикую)..."
OKAUTH=0
if command -v gh >/dev/null 2>&1; then
  if gh auth status >/dev/null 2>&1; then OKAUTH=1; fi
fi
echo ""
if [ "$OKAUTH" = "1" ]; then
  echo "✅ Готово. Вход в GitHub есть, публикатор установлен."
  echo "   Само ничего не уходит — публикация только когда ты просишь."
else
  echo "⚠️  Публикатор установлен, но вход в GitHub не найден."
  echo "   Один раз выполни:  gh auth login   (GitHub.com → HTTPS → браузер)"
  echo "   После этого больше сюда заходить не нужно."
fi
echo ""
echo "Выключить: launchctl unload \"$PLIST\""
echo "Журнал: $AUTO/autopublish.log"
read -r -p "Нажмите Enter, чтобы закрыть окно."
