#!/bin/bash
# Скрипт для конвертации AAB в APK с помощью bundletool

set -e

AAB_FILE="bin/yatuta-1.0.0-arm64-v8a_armeabi-v7a-release.aab"
KEYSTORE="yatuta.keystore"
KEYSTORE_PASS="Yatuta2024!"
KEY_ALIAS="yatuta"
KEY_PASS="Yatuta2024!"

echo "=== Конвертация AAB в APK ==="
echo ""

# Проверяем наличие AAB файла
if [ ! -f "$AAB_FILE" ]; then
    echo "Ошибка: Файл $AAB_FILE не найден!"
    exit 1
fi

# Проверяем наличие keystore
if [ ! -f "$KEYSTORE" ]; then
    echo "Ошибка: Файл $KEYSTORE не найден!"
    exit 1
fi

# Скачиваем bundletool, если его нет
BUNDLETOOL="bundletool.jar"
if [ ! -f "$BUNDLETOOL" ]; then
    echo "Скачивание bundletool..."
    wget -q https://github.com/google/bundletool/releases/download/1.15.6/bundletool-all-1.15.6.jar -O "$BUNDLETOOL"
    echo "✓ Bundletool скачан"
fi

# Конвертируем AAB в APK
echo "Конвертация AAB в APK..."
java -jar "$BUNDLETOOL" build-apks \
    --bundle="$AAB_FILE" \
    --output=bin/yatuta.apks \
    --ks="$KEYSTORE" \
    --ks-pass="pass:$KEYSTORE_PASS" \
    --ks-key-alias="$KEY_ALIAS" \
    --key-pass="pass:$KEY_PASS" \
    --mode=universal

if [ $? -eq 0 ]; then
    echo "✓ AAB конвертирован в APK"
    
    # Распаковываем APK
    echo "Распаковка APK..."
    unzip -o -q bin/yatuta.apks -d bin/
    
    # Переименовываем универсальный APK
    if [ -f "bin/universal.apk" ]; then
        mv bin/universal.apk "bin/yatuta-1.0.0-arm64-v8a_armeabi-v7a-release.apk"
        echo "✓ APK создан: bin/yatuta-1.0.0-arm64-v8a_armeabi-v7a-release.apk"
    else
        # Ищем APK в распакованных файлах
        APK_FILE=$(find bin -name "*.apk" -type f | head -1)
        if [ -n "$APK_FILE" ]; then
            mv "$APK_FILE" "bin/yatuta-1.0.0-arm64-v8a_armeabi-v7a-release.apk"
            echo "✓ APK создан: bin/yatuta-1.0.0-arm64-v8a_armeabi-v7a-release.apk"
        else
            echo "⚠ APK файл не найден в распакованных файлах"
            echo "Проверьте содержимое bin/yatuta.apks"
        fi
    fi
    
    # Очищаем временные файлы
    rm -f bin/yatuta.apks
    echo ""
    echo "=== Готово! ==="
    echo "APK файл: bin/yatuta-1.0.0-arm64-v8a_armeabi-v7a-release.apk"
else
    echo "Ошибка при конвертации AAB в APK"
    exit 1
fi

