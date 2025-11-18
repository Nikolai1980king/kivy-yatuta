#!/bin/bash
# Скрипт для исправления проблемы с Cython в python-for-android

echo "Установка правильной версии Cython в виртуальное окружение python-for-android..."

# Находим виртуальное окружение python-for-android
VENV_PATH="$HOME/.buildozer/android/platform/python-for-android/.venv"

if [ -d "$VENV_PATH" ]; then
    echo "Найдено виртуальное окружение: $VENV_PATH"
    "$VENV_PATH/bin/pip" install "Cython<3.0" --upgrade
    echo "✓ Cython установлен"
else
    echo "Виртуальное окружение еще не создано. Будет создано при первой сборке."
fi


