#!/bin/bash
# Скрипт для проверки подключения устройства и просмотра логов

echo "=== Проверка подключения устройства ==="
echo ""

# Проверяем подключение
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
    echo ""
    echo "Если устройство все еще не видно, попробуйте:"
    echo "  sudo adb kill-server"
    echo "  sudo adb start-server"
    echo "  adb devices"
else
    echo "✓ Устройство подключено!"
    echo ""
    echo "=== Просмотр логов приложения ==="
    echo "Запустите приложение на телефоне, затем нажмите Ctrl+C для остановки"
    echo ""
    adb logcat -c  # Очищаем старые логи
    adb logcat | grep -i "yatuta\|error\|exception\|fatal\|python\|kivy"
fi


