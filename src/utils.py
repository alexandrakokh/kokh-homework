import json
import os
from typing import List, Dict, Any

def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает JSON‑файл и возвращает список словарей с данными о транзакциях.

    Args:
        file_path (str): Путь к JSON‑файлу.

    Returns:
        List[Dict]: Список словарей с транзакциями или пустой список в случае ошибки.
    """
    # Проверяем существование файла
    if not os.path.exists(file_path):
        return []

    try:
        # Открываем файл и загружаем данные
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Проверяем, что данные — это список
        if isinstance(data, list):
            return data
        else:
            # Если данные не список, возвращаем пустой список
            return []
    except (json.JSONDecodeError, IOError, OSError):
        # Обрабатываем ошибки чтения, парсинга и системные ошибки
        return []