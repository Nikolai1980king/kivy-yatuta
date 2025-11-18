[app]

# (str) Название приложения
title = Знакомства в заведениях

# (str) Имя пакета (должно быть уникальным)
package.name = yatuta

# (str) Домен пакета
package.domain = ru.yatuta

# (str) Источник кода приложения
source.dir = .

# (list) Список исходных файлов
source.include_exts = py,png,jpg,kv,atlas,json

# (str) Главный файл приложения
source.main = main.py

# (str) Версия приложения
version = 1.0.0

# (list) Список требований
requirements = python3,kivy,pyjnius,android,cython==0.29.36

# (str) Иконка приложения (путь к файлу)
icon.filename = %(source.dir)s/icon.png

# (str) Имя автора
author = Ятута

# (str) Presplash экран (заставка при запуске)
presplash.filename = %(source.dir)s/presplash.png

# (str) Описание приложения для магазина
# android.meta_data.description = Приложение для доступа к сайту Ятута

# (str) Версия Android API
android.api = 33

# (int) Минимальная версия Android API
android.minapi = 21

# (str) Версия Android NDK
android.ndk = 25b

# (int) Версия Android SDK
android.sdk = 33

# (bool) Использовать AndroidX
android.gradle_dependencies = androidx.appcompat:appcompat:1.6.1

# (list) Разрешения Android
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,READ_EXTERNAL_STORAGE,READ_MEDIA_IMAGES

# (str) Activity entry point
android.entrypoint = org.kivy.android.YatutaActivity

# (list) Additional Java source directories
android.add_src = src/main/java

# (str) Ориентация экрана
orientation = portrait

# (bool) Полноэкранный режим
fullscreen = 0

# (list) Разрешения для Google Play
android.allow_backup = False

# (str) Архитектура (можно указать несколько через запятую)
# android.archs = arm64-v8a, armeabi-v7a

# (str) Ключ для подписи (для релиза)
android.keystore = yatuta.keystore

# (str) Пароль для keystore
android.keystore_password = Yatuta2024!

# (str) Алиас для ключа
android.keystore_alias = yatuta

# (str) Пароль для алиаса
android.keystore_alias_password = Yatuta2024!

# (bool) Собирать AAB вместо APK (False = APK, True = AAB)
# Для RuStore нужен APK, для Google Play - AAB
android.aab = False

[buildozer]

# (int) Логирование (0 = ошибки только, 1 = info, 2 = debug)
log_level = 2

# (int) Отображать предупреждения
warn_on_root = 1

