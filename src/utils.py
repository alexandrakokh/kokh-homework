import json
import os
from typing import Any, Dict, List

from logging_config import setup_logger

# Создаём логгер для этого модуля
logger = setup_logger("utils")


def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает JSON-файл и возвращает список словарей с данными о транзакциях.

    Args:
        file_path (str): Путь к JSON-файлу.

    Returns:
        List[Dict]: Список словарей с транзакциями или пустой список в случае ошибки.
    """
    logger.info(f"Начинаем чтение JSON-файла: {file_path}")

    # Проверяем существование файла
    if not os.path.exists(file_path):
        logger.error(f"Файл не найден: {file_path}")
        return []

    try:
        # Открываем файл и загружаем данные
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Проверяем, что данные — это список
        if isinstance(data, list):
            logger.info(f"Успешно прочитан файл {file_path}. Найдено {len(data)} записей.")
            return data
        else:
            logger.warning(f"Данные в файле {file_path} не являются списком. Возвращаем пустой результат.")
            return []

    except (json.JSONDecodeError, IOError, OSError) as e:
        logger.error(f"Ошибка при чтении или парсинге файла {file_path}: {str(e)}")
        return []
