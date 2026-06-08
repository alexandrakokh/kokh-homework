import logging
import os

def setup_logger(module_name):
    """
    Создаёт логгер для указанного модуля с записью в файл.

    Args:
        module_name (str): Название модуля

    Returns:
        logging.Logger: Настроенный логгер
    """
    # Получаем логгер с именем модуля
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)  # Записываем все уровни логирования

    # Очищаем существующие обработчики, чтобы избежать дублирования
    logger.handlers.clear()

    # Путь к файлу лога: logs/module_name.log
    log_file_path = os.path.join('logs', f'{module_name}.log')

    # Создаём обработчик для записи в файл (режим 'w' — перезапись при каждом запуске)
    file_handler = logging.FileHandler(log_file_path, mode='w', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)

    # Формат записи: время, модуль, уровень серьёзности, сообщение
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)

    # Добавляем обработчик к логгеру
    logger.addHandler(file_handler)

    return logger