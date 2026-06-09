import logging
import os
from pathlib import Path


def setup_logger(module_name: str) -> logging.Logger:
    # Создаем путь к директории логов
    log_dir = Path("logs")
    log_file_path = log_dir / f"{module_name}.log"

    # Создаем директорию, если её не существует
    if not log_dir.exists():
        log_dir.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)

    # Создаем обработчик файла
    file_handler = logging.FileHandler(log_file_path, mode="w", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)

    # Форматируем сообщения
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Добавляем обработчик к логгеру
    logger.addHandler(file_handler)

    return logger
