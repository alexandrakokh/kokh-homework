import re
from logging_config import setup_logger

# Создаём логгер для этого модуля
logger = setup_logger("masks")


def get_mask_card_number(card: str) -> str:
    """
    Маскирует номер карты.
    Формат: первые 6 цифр + **** + последние 4 цифры.

    Args:
        card: Строка с номером карты (должна содержать ровно 16 цифр).

    Returns:
        Замаскированный номер карты.

    Raises:
        ValueError: Если номер не состоит из 16 цифр.
    """
    logger.info("Начинаем маскирование номера карты")

    if not card or not isinstance(card, str):
        raise ValueError("Номер карты должен быть непустой строкой")

    clean_card = card.replace(" ", "")

    if not clean_card.isdigit():
        raise ValueError("Номер карты должен содержать только цифры")

    if len(clean_card) != 16:
        raise ValueError(f"Номер карты должен содержать ровно 16 цифр, получено: {len(clean_card)}")

    result = f"{clean_card[:6]}****{clean_card[-4:]}"

    logger.debug(f"Исходный номер прошел валидацию: {clean_card}")
    logger.info(f"Успешно замаскировали номер. Результат: {result}")
    return result


def get_mask_account(account: str) -> str:
    """
    Маскирует номер счета.
    Формат: ** + последние 4 цифры.

    Args:
        account: Строка с номером счета.

    Returns:
        Замаскированный номер счета.

    Raises:
        ValueError: Если счет не является непустой строкой или содержит не только цифры.
    """
    # --- ИСПРАВЛЕНИЕ ЗДЕСЬ ---
    # Теперь функция строго проверяет входные данные и выбрасывает ошибки,
    # чтобы тесты test_invalid_account_inputs_raises_correct_error проходили.

    if account is None or not isinstance(account, str) or account.strip() == "":
        raise ValueError("Номер счёта должен быть непустой строкой")

    clean_account = account.replace(" ", "").strip()

    if not clean_account.isdigit():
        raise ValueError("Номер счёта должен содержать только цифры")

    # Для счета мы не требуем конкретную длину (как 16 для карты),
    # но если цифр нет вообще, isdigit() это уже отловил.
    # Берем последние 4 цифры
    suffix = clean_account[-4:] if len(clean_account) >= 4 else clean_account

    return f"**{suffix}"


def mask_account_card(value: str) -> str:
    """
    Универсальная функция. Принимает строку вида:
    "Visa 1234...", "Счет 1234...", просто "1234..." или "Card 12 34 56 78".

    Возвращает:
    - Отформатированную строку с маской и префиксом (если был).
    - "Неизвестно", если вход пустой/None.
    - Исходную строку, если формат номера не соответствует ожидаемым стандартам.
    """
    if value is None:
        logger.warning("Пустой или неверный тип ввода для mask_account_card (None)")
        return "Неизвестно"

    if not isinstance(value, str):
        logger.warning(f"Пустой или неверный тип ввода для mask_account_card: {type(value)}")
        return "Неизвестно"

    original_input = value.strip()
    if not original_input:
        logger.warning("Пустая строка для mask_account_card")
        return "Неизвестно"

    parts = original_input.split()
    prefix = ""
    digits_only = ""

    # Логика парсинга (без изменений, она рабочая)
    if len(parts) == 1:
        candidate = parts[0]
        if candidate.isdigit():
            digits_only = candidate
        else:
            found = re.search(r"\d+", original_input)
            digits_only = found.group() if found else ""
    elif len(parts) >= 2:
        prefix = parts[0]
        potential = "".join(parts[1:])
        if potential.isdigit():
            digits_only = potential
        else:
            found = re.search(r"\d+", potential)
            if found:
                digits_only = found.group()
                if not re.match(r"^[A-Za-zA-Яа-я]+$", prefix):
                    prefix = ""
            else:
                return original_input

    if not digits_only:
        return original_input

    digit_len = len(digits_only)
    prefix_lower = prefix.lower() if prefix else ""

    try:
        is_card_prefix = prefix_lower in ["visa", "mastercard", "card", "amex", "discover"]

        # Логика карт: если есть префикс карты ИЛИ просто 16 цифр
        if is_card_prefix or digit_len == 16:
            if digit_len != 16:
                # Неверная длина для карты -> возвращаем оригинал
                logger.warning(f"Обнаружен префикс карты, но неверная длина ({digit_len}). Возврат оригинала.")
                return original_input

            masked = get_mask_card_number(digits_only)
            return f"{prefix} {masked}" if prefix else masked

        # Логика счетов
        MIN_ACCOUNT_LEN = 10  # Минимальная длина для валидного счета

        if digit_len >= MIN_ACCOUNT_LEN:
            is_account_prefix = prefix_lower in ["счет", "account", "acc", "счёт", "bank account"]
            masked = get_mask_account(digits_only)
            return f"{prefix} {masked}" if is_account_prefix else masked

        # Если длина не подходит ни под карту, ни под счет
        logger.warning(f"Длина номера {digit_len} не подходит ни под карту, ни под валидный счет.")
        return original_input

    except ValueError:
        # Если внутренняя функция выбросила ошибку валидации, возвращаем оригинал,
        # чтобы интерфейс mask_account_card не падал с исключением
        return original_input
