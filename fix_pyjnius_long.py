#!/usr/bin/env python3
"""
Скрипт для исправления ошибки 'long' в pyjnius
Заменяет isinstance(arg, long) на isinstance(arg, int) в jnius_utils.pxi
"""

import os
import sys
import glob

def fix_pyjnius_long():
    """Ищет и исправляет файл jnius_utils.pxi"""
    
    # Возможные пути к файлу
    search_paths = [
        os.path.expanduser("~/.buildozer"),
        ".buildozer",
        os.path.expanduser("~/.local/lib/python3.*/site-packages/pyjnius"),
    ]
    
    found_files = []
    
    # Ищем файл
    for path in search_paths:
        if os.path.exists(path):
            for root, dirs, files in os.walk(path):
                if "jnius_utils.pxi" in files:
                    filepath = os.path.join(root, "jnius_utils.pxi")
                    found_files.append(filepath)
    
    if not found_files:
        print("Файл jnius_utils.pxi не найден.")
        print("Он будет создан python-for-android во время сборки.")
        print("Запустите этот скрипт после начала сборки (когда появится ошибка).")
        return False
    
    fixed = False
    for filepath in found_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Проверяем, нужно ли исправлять
            if 'isinstance(arg, long)' in content:
                # Заменяем long на int
                new_content = content.replace('isinstance(arg, long)', 'isinstance(arg, int)')
                
                # Также заменяем другие варианты
                new_content = new_content.replace('(isinstance(arg, long)', '(isinstance(arg, int)')
                
                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"✓ Исправлен файл: {filepath}")
                    fixed = True
                else:
                    print(f"Файл уже исправлен: {filepath}")
            else:
                print(f"Файл не требует исправления: {filepath}")
        except Exception as e:
            print(f"Ошибка при обработке {filepath}: {e}")
    
    return fixed

if __name__ == '__main__':
    print("Поиск и исправление файла jnius_utils.pxi...")
    if fix_pyjnius_long():
        print("\n✓ Готово! Теперь можно продолжить сборку.")
    else:
        print("\n⚠ Файл не найден. Запустите сборку, и когда появится ошибка,")
        print("  запустите этот скрипт снова в другом терминале.")


