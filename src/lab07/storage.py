# lab07/storage.py
"""Сохранение и загрузка данных в JSON-файл."""

import json
from typing import Any, Dict, List


def save(data: List[Dict[str, Any]], filepath: str) -> None:
    """Сохранить коллекцию в JSON-файл.
    
    Args:
        data: список словарей, представляющих объекты.
        filepath: путь к файлу.
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load(filepath: str) -> List[Dict[str, Any]]:
    """Загрузить объекты из JSON-файла.
    
    Args:
        filepath: путь к файлу.
    
    Returns:
        Список словарей. Если файл не найден, возвращается пустой список.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []