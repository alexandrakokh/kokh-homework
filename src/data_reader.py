from typing import Any, Dict, List

import pandas as pd

from logging_config import setup_logger as create_module_logger

logger = create_module_logger("data_reader")


def read_transactions_from_csv(file_path: str) -> List[Dict[str, Any]]:
    logger.info(f"Начинаем чтение CSV-файла: {file_path}")
    try:
        df = pd.read_csv(file_path)
        data: List[Dict[str, Any]] = df.to_dict(orient="records")
        logger.info(f"Успешно прочитан CSV-файл. Найдено {len(data)} записей.")
        return data
    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}")
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
