from src.masks import get_mask_card_number, get_mask_account
from datetime import datetime


def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер карты, оставляя видимыми первые 6 и последние 4 цифры."""
    if not card_number.isdigit():
        raise ValueError("Номер карты должен содержать только цифры")
    if len(card_number) < 13 or len(card_number) > 19:
        raise ValueError("Номер карты должен иметь длину от 13 до 19 цифр")

    visible_start = card_number[:6]

    # Для карт короче 16 цифр берём последние 3 цифры, а не 4
    if len(card_number) < 16:
        visible_end = card_number[-3:]  # последние 3 цифры
        masked_middle = '*' * 5
    else:
        # Для стандартных 16‑значных карт — последние 4 цифры и (длина − 10) звёздочек
        visible_end = card_number[-4:]
        masked_middle = '*' * (len(card_number) - 10)

    return f"{visible_start}{masked_middle}{visible_end}"

def get_mask_account(account_number: str) -> str:
    """Маскирует номер счёта, оставляя только последние 4 цифры."""
    if not account_number.isdigit():
        raise ValueError("Номер счёта должен содержать только цифры")

    return f"**{account_number[-4:]}"

def mask_account_card(input_string: str) -> str:
    """Маскирует номер карты или счёта в строке."""
    first_digit_index = None
    for i, char in enumerate(input_string):
        if char.isdigit():
            first_digit_index = i
            break

    if first_digit_index is None:
        raise ValueError("В строке не найден номер карты или счёта")

    type_part = input_string[:first_digit_index].strip()
    number_part = input_string[first_digit_index:].strip()

    account_keywords = {'счёт', 'счет', 'account', 'account number'}

    if any(keyword in type_part.lower() for keyword in account_keywords):
        masked_number = get_mask_account(number_part)
    else:
        masked_number = get_mask_card_number(number_part)


    return f"{type_part} {masked_number}"

def get_date(date_string: str) -> str:
    """Преобразует строку с датой из формата ISO в формат ДД.ММ.ГГГГ."""
    if not date_string:
        raise ValueError(f"Неверный формат даты: '{date_string}'. Ожидаемый формат: 'ГГГГ-ММ-ДДТЧЧ:ММ:СС.ffffff'")

    try:
        parsed_date = datetime.fromisoformat(date_string)
        formatted_date = parsed_date.strftime("%d.%m.%Y")
        return formatted_date
    except ValueError as e:
        raise ValueError(
            f"Неверный формат даты: '{date_string}'. Ожидаемый формат: 'ГГГГ-ММ-ДДТЧЧ:ММ:СС.ffffff'") from e
