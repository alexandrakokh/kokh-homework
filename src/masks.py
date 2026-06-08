from logging_config import setup_logger

# Создаём логгер для этого модуля
logger = setup_logger("masks")


def get_mask_card_number(card_input):
    """
    Маскирует номер карты: первые 6 цифр + **** + 3-я/4-я с конца + последние 2.
    """
    # Логируем начало обработки
    logger.info("Начинаем маскирование номера карты")

    # Проверка на пустой ввод
    if not card_input:
        logger.error("Получен пустой ввод для маскирования карты")
        raise ValueError("Номер карты должен содержать только цифры")

    # Проверка на наличие только цифр
    if not card_input.isdigit():
        logger.error(f"Некорректный формат номера карты: {card_input}")
        raise ValueError("Номер карты должен содержать только цифры")

    # Проверка длины
    if len(card_input) != 16:
        logger.error(f"Неверная длина номера карты: {len(card_input)} цифр")
        raise ValueError("Номер карты должен содержать ровно 16 цифр")

    # Логируем успешное прохождение валидации
    logger.debug(f"Исходный номер прошел валидацию: {card_input}")

    # Маскирование: первые 6 цифр + **** + 3-я/4-я с конца + последние 2
    first_part = card_input[:6]
    middle_part = card_input[-4:-2]  # 3-я и 4-я цифры с конца
    last_part = card_input[-2:]  # Последние 2 цифры

    result = f"{first_part}****{middle_part}{last_part}"
    logger.info(f"Успешно замаскировали номер. Результат: {result}")
    return result


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер счёта: показывает только последние 4 цифры.
    """
    logger.info("Начинаем маскирование номера счёта")

    if not account_number:
        logger.error("Получен пустой ввод для маскирования счёта")
        raise ValueError("Номер счёта должен содержать только цифры")

    if not account_number.isdigit():
        logger.error(f"Некорректный формат номера счёта: {account_number}")
        raise ValueError("Номер счёта должен содержать только цифры")

    result = "**" + account_number[-4:]
    logger.info(f"Успешно замаскировали номер счёта. Результат: {result}")
    return result
