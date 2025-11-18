#!/bin/bash
# Скрипт для создания keystore для подписи APK

echo "Создание keystore для подписи APK..."
echo "Вам будет предложено ввести пароль и информацию о сертификате"
echo ""

keytool -genkey -v -keystore yatuta.keystore -alias yatuta -keyalg RSA -keysize 2048 -validity 10000

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Keystore создан: yatuta.keystore"
    echo ""
    echo "Теперь добавьте в buildozer.spec следующие строки (раскомментируйте и укажите пароль):"
    echo "android.keystore = yatuta.keystore"
    echo "android.keystore_password = ваш_пароль"
    echo "android.keystore_alias = yatuta"
    echo "android.keystore_alias_password = ваш_пароль"
    echo ""
    echo "⚠️  ВАЖНО: Сохраните пароль в безопасном месте! Без него вы не сможете обновлять приложение!"
else
    echo "Ошибка при создании keystore"
    exit 1
fi


