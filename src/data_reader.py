import json
from pathlib import Path

from typing import Any, Dict, List

import pandas as pd

from src.logging_config import setup_logger as create_module_logger

logger = create_module_logger("data_reader")


def read_transactions_from_csv(file_path: str) -> List[Dict[str, Any]]:
    logger.info(f"Начинаем чтение CSV-файла: {file_path}")
    try:
        # 1. Читаем файл с явным указанием кодировки (часто спасает от ошибок)
        df = pd.read_csv(file_path, encoding="utf-8", sep=";")

        # 2. Очистка данных
        # Удаляем полностью пустые строки (где все значения NaN)
        df = df.dropna(how="all")
        # Заменяем NaN (пустые значения) на пустые строки '' для удобства
        df = df.fillna("")

        # 3. Преобразуем в список словарей
        data: List[Dict[str, Any]] = df.to_dict(orient="records")

        logger.info(f"Успешно прочитан CSV-файл. Найдено {len(data)} записей.")
        return data

    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}")
        return []
    except UnicodeDecodeError:
        logger.error(f"Ошибка кодировки при чтении файла {file_path}. Попробуйте encoding='cp1251'.")
        return []
    except Exception as e:
        logger.error(f"Ошибка при чтении CSV файла '{file_path}': {e}")
        return []


def read_transactions_from_excel(file_path: str) -> List[Dict[str, Any]]:
    logger.info(f"Начинаем чтение Excel-файла: {file_path}")
    try:
        df = pd.read_excel(file_path, engine="openpyxl")
        data: List[Dict[str, Any]] = df.to_dict(orient="records")
        logger.info(f"Успешно прочитан Excel-файл. Найдено {len(data)} записей.")
        return data
    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}")
        return []
    except Exception as e:
        logger.error(f"Ошибка при чтении Excel файла '{file_path}': {e}")
        return []


def read_transactions_from_json(file_path: str) -> List[Dict[str, Any]]:
    logger.info(f"Начинаем чтение JSON-файла: {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data: List[Dict[str, Any]] = json.load(file)
            logger.info(f"Успешно прочитан JSON-файл. Найдено {len(data)} записей.")
            return data
    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка декодирования JSON файла '{file_path}': {e}")
        return []
    except Exception as e:
        logger.error(f"Ошибка при чтении JSON файла '{file_path}': {e}")
        return []


def read_data(file_type: str, file_name: str) -> List[Dict[str, Any]]:
    """
    Универсальная функция для чтения данных.
    file_type: 'json', 'csv', 'xlsx'
    file_name: имя файла (например, 'transactions.json')
    """
    # Строим путь относительно папки src
    current_dir = Path(__file__).parent  # Папка, где лежит data_reader.py (src)
    data_dir = current_dir.parent / "data"  # Поднимаемся в корень и идем в data
    file_path = data_dir / file_name  # Собираем полный путь

    handlers = {
        "json": read_transactions_from_json,
        "csv": read_transactions_from_csv,
        "xlsx": read_transactions_from_excel,
    }

    if file_type not in handlers:
        logger.error(f"Неподдерживаемый формат файла: {file_type}")
        return []

    return handlers[file_type](str(file_path))  # Передаем строковый путь в обработчики
