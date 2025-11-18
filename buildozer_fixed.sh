#!/bin/bash
# Обертка для buildozer с автоматическим исправлением проблемы Cython/pyjnius

echo "=== Сборка APK с автоматическим исправлением ==="
echo ""

# Устанавливаем правильную версию Cython
echo "1. Установка Cython 0.29.36..."
if [ -n "$VIRTUAL_ENV" ]; then
    # В виртуальном окружении
    pip install "cython==0.29.36" --quiet
else
    # В системном Python
    pip install "cython==0.29.36" --user --quiet
fi
/usr/bin/python3 -m pip install "cython==0.29.36" --user --quiet 2>/dev/null || true

# Функция для исправления pyjnius
fix_pyjnius() {
    echo "2. Поиск и исправление jnius_utils.pxi..."
    
    # Ищем файл в разных местах
    FOUND_FILE=""
    for path in ~/.buildozer .buildozer; do
        if [ -d "$path" ]; then
            FILE=$(find "$path" -name "jnius_utils.pxi" 2>/dev/null | head -1)
            if [ -n "$FILE" ] && [ -f "$FILE" ]; then
                FOUND_FILE="$FILE"
                break
            fi
        fi
    done
    
    if [ -n "$FOUND_FILE" ]; then
        echo "   Найден файл: $FOUND_FILE"
        # Исправляем файл
        sed -i 's/isinstance(arg, long)/isinstance(arg, int)/g' "$FOUND_FILE"
        sed -i 's/(isinstance(arg, long)/(isinstance(arg, int)/g' "$FOUND_FILE"
        echo "   ✓ Файл исправлен"
        return 0
    else
        echo "   Файл не найден (будет создан во время сборки)"
        return 1
    fi
}

# Запускаем сборку в фоне
echo "3. Запуск сборки..."
buildozer android release &
BUILDOZER_PID=$!

# Ждем немного, чтобы python-for-android начал работу
sleep 10

# Пытаемся исправить файл несколько раз
for i in {1..10}; do
    if fix_pyjnius; then
        echo "   ✓ Исправление применено"
        break
    fi
    sleep 5
done

# Ждем завершения сборки
echo "4. Ожидание завершения сборки..."
wait $BUILDOZER_PID
EXIT_CODE=$?

# Если была ошибка, пытаемся исправить и пересобрать
if [ $EXIT_CODE -ne 0 ]; then
    echo ""
    echo "5. Обнаружена ошибка, пытаемся исправить..."
    fix_pyjnius
    
    echo "6. Повторная попытка сборки..."
    buildozer android release
fi

echo ""
echo "=== Готово ==="

