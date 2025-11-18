#!/bin/bash
# Патч для исправления версии Cython в python-for-android

echo "Поиск виртуального окружения python-for-android..."

# Возможные пути к виртуальному окружению
VENV_PATHS=(
    "$HOME/.buildozer/android/platform/python-for-android/.venv"
    "$HOME/.buildozer/android/platform/python-for-android/venv"
    ".buildozer/android/platform/python-for-android/.venv"
    ".buildozer/android/platform/python-for-android/venv"
)

VENV_FOUND=""

for path in "${VENV_PATHS[@]}"; do
    if [ -d "$path" ] && [ -f "$path/bin/pip" ]; then
        VENV_FOUND="$path"
        echo "Найдено виртуальное окружение: $path"
        break
    fi
done

if [ -z "$VENV_FOUND" ]; then
    echo "Виртуальное окружение не найдено. Оно будет создано при первой сборке."
    echo "Запустите этот скрипт после начала сборки (когда появится ошибка)."
    exit 0
fi

echo "Установка Cython 0.29.36 в виртуальное окружение..."
"$VENV_FOUND/bin/pip" install --force-reinstall "cython==0.29.36"

echo "Проверка версии Cython..."
"$VENV_FOUND/bin/python" -c "import Cython; print('Cython версия:', Cython.__version__)"

echo "✓ Готово! Теперь можно продолжить сборку."


