from datetime import datetime

def mask_card_number(card_number: str) -> str:
    """Маскирует номер карты, оставляя видимыми первые 6 и последние 4 цифры."""
    if not card_number.isdigit():
        raise ValueError("Номер карты должен содержать только цифры")
    if len(card_number) < 13 or len(card_number) > 19:
        raise ValueError("Номер карты должен иметь длину от 13 до 19 цифр")

    # Оставляем первые 6 цифр и последние 4, остальное маскируем
    visible_start = card_number[:6]
    visible_end = card_number[-4:]
    masked_middle = '*' * (len(card_number) - 10)

    return f"{visible_start}{masked_middle}{visible_end}"

def mask_account_number(account_number: str) -> str:
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

    # Выделяем тип (название) и номер
    type_part = input_string[:first_digit_index].strip()
    number_part = input_string[first_digit_index:].strip()

    # Определяем тип и применяем соответствующую маскировку
    # Проверяем различные варианты написания «счёт»
    account_keywords = {'счёт', 'счет', 'account', 'account number'}
    if any(keyword in type_part.lower() for keyword in account_keywords):
        masked_number = mask_account_number(number_part)
    else:
        # Предполагаем, что всё остальное — это карты
        masked_number = mask_card_number(number_part)

    return f"{type_part} {masked_number}"

def get_date(date_string: str) -> str:
    """Преобразует строку с датой из формата ISO в формат ДД.ММ.ГГГГ."""
    try:
        # Парсим входную строку как дату в формате ISO 8601
        parsed_date = datetime.fromisoformat(date_string)
        # Форматируем дату в нужный формат (ДД.ММ.ГГГГ)
        formatted_date = parsed_date.strftime("%d.%m.%Y")
        return formatted_date
    except ValueError as e:
        raise ValueError(
            f"Неверный формат даты: '{date_string}'. Ожидаемый формат: 'ГГГГ-ММ-ДДТЧЧ:ММ:СС.ffffff'") from e

# Проверка работы функций на примерах
if __name__ == "__main__":
    print("Результаты тестирования функции mask_account_card:")
    print("-" * 50)
    test_cases = [
        "Maestro 1596837868705199",
        "Счет 64686473678894779589",
        "MasterCard 7158300734726758",
        "Счёт 35383033474447895560",
        "Visa Classic 6831982476737658",
        "Visa Platinum 8990922113665229",
        "Visa Gold 5999414228426353",
        "Account 73654108430135874305"
    ]

    for case in test_cases:
        try:
            result = mask_account_card(case)
            print(f"Вход:  {case}")
            print(f"Выход: {result}")
        except ValueError as e:
            print(f"Ошибка для '{case}': {e}")
        print()

    print("\nРезультаты тестирования функции get_date:")
    print("-" * 40)
    date_test_cases = [
        "2024-03-11T02:26:18.671407",
        "2023-12-25T15:30:45.123456",
        "2020-01-01T00:00:00.000000",
        "2025-07-15T18:45:30.999999"
    ]

    for date_input in date_test_cases:
        try:
            result = get_date(date_input)
            print(f"Вход:  {date_input}")
            print(f"Выход: {result}")
        except ValueError as e:
            print(f"Ошибка для '{date_input}': {e}")
        print()