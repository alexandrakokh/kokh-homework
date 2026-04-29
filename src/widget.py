def mask_account_card(input_string: str) -> str:
    """Маскирует номер карты или счёта в строке."""


    def mask_card_number(card_number: str) -> str:
        """Маскирует номер карты по шаблону XXXX XX** **** XXXX."""
        if len(card_number) != 16 or not card_number.isdigit():
            raise ValueError("Номер карты должен состоять из 16 цифр")

        return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"

    def mask_account_number(account_number: str) -> str:
        """Маскирует номер счёта, оставляя только последние 4 цифры."""
        if not account_number.isdigit():
            raise ValueError("Номер счёта должен содержать только цифры")

        return f"**{account_number[-4:]}"

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
    if type_part.lower() == "счёт":
        masked_number = mask_account_number(number_part)
    else:
        # Предполагаем, что всё остальное — это карты
        masked_number = mask_card_number(number_part)

    return f"{type_part} {masked_number}"



# Проверка работы функции на примерах
test_cases = [
    "Maestro 1596837868705199",
    "Счет 64686473678894779589",
    "MasterCard 7158300734726758",
    "Счет 35383033474447895560",
    "Visa Classic 6831982476737658",
    "Visa Platinum 8990922113665229",
    "Visa Gold 5999414228426353",
    "Счет 73654108430135874305"
]

print("Результаты тестирования:")
print("-" * 50)
for case in test_cases:
    result = mask_account_card(case)
    print(f"Вход:  {case}")
    print(f"Выход: {result}")
    print()

    from datetime import datetime


    def get_date(date_string: str) -> str:
        """Преобразует строку с датой из формата ISO в формат ДД.ММ.ГГГГ."""

        try:
            # Просим входную строку как дату в формате ISO 8601
            parsed_date = datetime.fromisoformat(date_string)
            # Форматируем дату в нужный формат (ДД.ММ.ГГГГ)
            formatted_date = parsed_date.strftime("%d.%m.%Y")
            return formatted_date
        except ValueError as e:
            raise ValueError(
                f"Неверный формат даты: '{date_string}'. Ожидаемый формат: 'ГГГГ-ММ-ДДТЧЧ:ММ:СС.ffffff'") from e


    # Примеры использования и тестирования функции
    if __name__ == "__main__":
        test_cases = [
            "2024-03-11T02:26:18.671407",
            "2023-12-25T15:30:45.123456",
            "2020-01-01T00:00:00.000000",
            "2025-07-15T18:45:30.999999"
        ]

        print("Результаты тестирования функции get_date:")
        print("-" * 40)
        for date_input in test_cases:
            try:
                result = get_date(date_input)
                print(f"Вход:  {date_input}")
                print(f"Выход: {result}")
            except ValueError as e:
                print(f"Ошибка для '{date_input}': {e}")
            print()