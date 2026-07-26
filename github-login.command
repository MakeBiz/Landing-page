#!/bin/bash
# MakeBiz — вход в GitHub (делается ОДИН раз, двойным кликом).
# Никакого токена вводить не нужно: авторизация через сам GitHub в браузере.
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

echo "=================================================="
echo "  MakeBiz — подключение GitHub (один раз)"
echo "=================================================="
echo ""

# 1) есть ли утилита gh
if ! command -v gh >/dev/null 2>&1; then
  echo "→ Утилита GitHub CLI (gh) не найдена. Ставлю через Homebrew..."
  if command -v brew >/dev/null 2>&1; then
    brew install gh || { echo "❌ Не удалось поставить gh. Напишите ассистенту в чат."; read -r -p "Enter, чтобы закрыть..."; exit 1; }
  else
    echo "❌ Homebrew не установлен. Установите его (одна строка), потом снова запустите этот файл:"
    echo ""
    echo '   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
    echo ""
    read -r -p "Enter, чтобы закрыть..."; exit 1
  fi
fi

# 2) уже авторизованы?
if gh auth status >/dev/null 2>&1; then
  echo "✅ Вход в GitHub уже есть — доступ на месте."
else
  echo "→ Сейчас откроется браузер."
  echo "  1) Терминал покажет короткий код (8 символов) — скопируйте его."
  echo "  2) Нажмите Enter, откроется страница GitHub."
  echo "  3) Вставьте код и подтвердите доступ."
  echo ""
  gh auth login --hostname github.com --git-protocol https --web || {
    echo "❌ Вход не завершён. Просто запустите этот файл ещё раз."; read -r -p "Enter, чтобы закрыть..."; exit 1; }
fi

# 3) привязать git к этим данным (чтобы публикация шла без вопросов)
gh auth setup-git 2>/dev/null || true

# 4) проверить доступ к репозиторию (без публикации)
echo ""
echo "→ Проверяю доступ к репозиторию Landing-page..."
if git ls-remote https://github.com/MakeBiz/Landing-page.git HEAD >/dev/null 2>&1; then
  echo ""
  echo "✅ ГОТОВО. GitHub подключён, публикация будет работать."
  echo "   Вернитесь в чат и напишите:  опубликуй"
else
  echo "⚠️  Доступ пока не подтверждён. Напишите ассистенту — разберёмся вместе."
fi
echo ""
read -r -p "Нажмите Enter, чтобы закрыть окно."
