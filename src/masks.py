def get_mask_card_number(card_input):
    # Проверка на пустой ввод
    if not card_input:
        raise ValueError("Номер карты должен содержать только цифры")

    # Проверка на наличие только цифр
    if not card_input.isdigit():
        raise ValueError("Номер карты должен содержать только цифры")

    # Проверка длины
    if len(card_input) != 16:
        raise ValueError("Номер карты должен содержать ровно 16 цифр")

    # Маскирование: первые 6 цифр + **** + 3-я/4-я с конца + последние 2
    first_part = card_input[:6]
    middle_part = card_input[-4:-2]  # 3-я и 4-я цифры с конца
    last_part = card_input[-2:]       # Последние 2 цифры

    return f"{first_part}****{middle_part}{last_part}"



def get_mask_account(account_number: str) -> str:
    """Маскирует номер счёта: показывает только последние 4 цифры."""
    if not account_number:
        raise ValueError("Номер счёта должен содержать только цифры")
    if not account_number.isdigit():
        raise ValueError("Номер счёта должен содержать только цифры")
    return "**" + account_number[-4:]
