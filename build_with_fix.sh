#!/bin/bash
# Скрипт для сборки с исправлением проблемы Cython

echo "Установка Cython 0.29.36..."
pip install "cython==0.29.36" --user
/usr/bin/python3 -m pip install "cython==0.29.36" --user

echo "Очистка кеша..."
buildozer android clean > /dev/null 2>&1

echo "Запуск сборки release APK..."
export P4A_CYTHON_VERSION="0.29.36"
buildozer android release


