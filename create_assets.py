#!/usr/bin/env python3
"""
Скрипт для создания иконки и presplash экрана для приложения
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    import os
except ImportError:
    print("Установите Pillow: pip install Pillow")
    exit(1)

def create_icon():
    """Создает иконку приложения 512x512"""
    size = 512
    img = Image.new('RGB', (size, size), color='#4A90E2')
    draw = ImageDraw.Draw(img)
    
    # Рисуем простой логотип "Я"
    margin = 100
    # Фон для буквы
    draw.ellipse([margin, margin, size-margin, size-margin], fill='white', outline='white', width=5)
    
    # Текст "Я" (если есть шрифт)
    try:
        # Пытаемся использовать системный шрифт
        font_size = 200
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", font_size)
            except:
                font = ImageFont.load_default()
        
        # Центрируем текст
        text = "Я"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        position = ((size - text_width) // 2, (size - text_height) // 2 - 20)
        draw.text(position, text, fill='#4A90E2', font=font)
    except:
        # Если не получилось с текстом, рисуем простую геометрическую фигуру
        center = size // 2
        radius = 80
        draw.ellipse([center-radius, center-radius, center+radius, center+radius], 
                    fill='#4A90E2', outline='white', width=10)
    
    img.save('icon.png')
    print("✓ Создана иконка: icon.png (512x512)")

def create_presplash():
    """Создает presplash экран 2048x2048"""
    size = 2048
    img = Image.new('RGB', (size, size), color='#4A90E2')
    draw = ImageDraw.Draw(img)
    
    # Рисуем логотип в центре
    margin = 400
    draw.ellipse([margin, margin, size-margin, size-margin], fill='white', outline='white', width=20)
    
    # Текст "Ятута"
    try:
        font_size = 400
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", font_size)
            except:
                font = ImageFont.load_default()
        
        text = "Ятута"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        position = ((size - text_width) // 2, (size - text_height) // 2 - 50)
        draw.text(position, text, fill='#4A90E2', font=font)
    except:
        # Простая геометрическая фигура
        center = size // 2
        radius = 200
        draw.ellipse([center-radius, center-radius, center+radius, center+radius], 
                    fill='#4A90E2', outline='white', width=30)
    
    img.save('presplash.png')
    print("✓ Создан presplash: presplash.png (2048x2048)")

if __name__ == '__main__':
    print("Создание ресурсов для приложения...")
    create_icon()
    create_presplash()
    print("\nГотово! Теперь можно собрать APK.")


