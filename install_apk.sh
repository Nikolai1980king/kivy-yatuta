#!/bin/bash

# Скрипт для установки APK на подключенное Android устройство

APK_FILE="bin/yatuta-1.0.0-arm64-v8a_armeabi-v7a-release.apk"

echo "=== Установка APK на Android устройство ==="
echo ""

# Проверяем наличие APK
if [ ! -f "$APK_FILE" ]; then
    echo "❌ APK файл не найден: $APK_FILE"
    echo ""
    echo "Сначала соберите APK:"
    echo "  buildozer android release"
    echo "  ./convert_aab_to_apk.sh"
    exit 1
fi

# Проверяем подключение устройства
echo "Проверка подключения устройства..."
DEVICES=$(adb devices | grep -v "List" | grep "device$" | wc -l)

if [ "$DEVICES" -eq 0 ]; then
    echo "❌ Устройство не подключено!"
    echo ""
    echo "Что нужно сделать:"
    echo "1. Подключите телефон к компьютеру через USB"
    echo "2. На телефоне включите 'Отладка по USB':"
    echo "   Настройки → О телефоне → Нажмите 7 раз на 'Номер сборки'"
    echo "   Затем: Настройки → Для разработчиков → Отладка по USB"
    echo "3. На телефоне разрешите отладку (появится запрос)"
    echo ""
    echo "Проверка подключения:"
    adb devices
    exit 1
fi

echo "✓ Устройство подключено"
echo ""

# Показываем информацию о APK
APK_SIZE=$(ls -lh "$APK_FILE" | awk '{print $5}')
echo "APK файл: $APK_FILE"
echo "Размер: $APK_SIZE"
echo ""

# Устанавливаем APK
echo "Установка APK..."
adb install -r "$APK_FILE"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ APK успешно установлен!"
    echo ""
    echo "Запуск приложения..."
    adb shell am start -n ru.yatuta.yatuta/org.kivy.android.YatutaActivity
    echo ""
    echo "Приложение запущено на устройстве!"
else
    echo ""
    echo "❌ Ошибка установки APK"
    echo ""
    echo "Возможные причины:"
    echo "1. На устройстве не разрешена установка из неизвестных источников"
    echo "2. APK уже установлен с другим ключом подписи"
    echo "3. Недостаточно места на устройстве"
    echo ""
    echo "Попробуйте:"
    echo "1. Удалить старое приложение: adb uninstall ru.yatuta.yatuta"
    echo "2. Или установить вручную, скопировав APK на телефон"
fi

