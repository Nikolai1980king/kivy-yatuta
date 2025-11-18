#!/bin/bash
# Скрипт для ожидания завершения сборки и автоматической конвертации в APK

echo "Ожидание завершения сборки..."
echo ""

# Ждем завершения процесса buildozer
while pgrep -f "buildozer android release" > /dev/null; do
    echo -n "."
    sleep 5
done

echo ""
echo "✓ Сборка завершена!"
echo ""

# Ждем немного, чтобы файлы записались
sleep 2

# Проверяем наличие AAB файла
if [ -f "bin/yatuta-1.0.0-arm64-v8a_armeabi-v7a-release.aab" ]; then
    echo "Найден AAB файл, конвертирую в APK..."
    ./convert_aab_to_apk.sh
elif [ -f "bin/yatuta-1.0.0-arm64-v8a_armeabi-v7a-release.apk" ]; then
    echo "✓ APK файл уже готов: bin/yatuta-1.0.0-arm64-v8a_armeabi-v7a-release.apk"
    ls -lh bin/yatuta-1.0.0-arm64-v8a_armeabi-v7a-release.apk
else
    echo "⚠ Файлы не найдены. Проверьте логи сборки:"
    tail -30 build.log
fi


