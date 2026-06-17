from datetime import datetime
from typing import Any, Dict
from src.masks import mask_account_card
from src.data_reader import read_data
from src.processing import (
    process_bank_search,
    filter_by_state,
    sort_by_date
)

ALLOWED_STATUSES = {"EXECUTED", "CANCELED", "PENDING"}


def _parse_date(date_val: Any) -> str:
    """Парсит дату в формат ДД.ММ.ГГГГ или возвращает заглушку."""
    if date_val is None:
        return "Неизвестная дата"

    date_str = str(date_val)
    formats = [
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d"
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime("%d.%m.%Y")
        except ValueError:
            continue

    return "Неизвестная дата"


def _get_currency_name(currency_val: Any) -> str:
    """Извлекает название валюты. Дефолт - RUB."""
    if not currency_val:
        return "RUB"

    if isinstance(currency_val, str):
        return currency_val

    if isinstance(currency_val, dict):
        # Пробуем взять по ключу 'name' (как в тестах) или 'code'
        val = currency_val.get("name") or currency_val.get("code")
        return val if val else "RUB"

    return str(currency_val)


def format_transaction(transaction: Dict[str, Any]) -> str:
    # 1. Дата
    raw_date = transaction.get("date")
    date_str = _parse_date(raw_date)

    # 2. Описание
    description = transaction.get("description")
    if description is None:
        description = "Без описания"
    else:
        description = str(description)

    # 3. Источник данных (верхний уровень или operationAmount)
    source = transaction
    if "operationAmount" in transaction and isinstance(transaction["operationAmount"], dict):
        source = transaction["operationAmount"]

    amount = source.get("amount")
    currency_raw = source.get("currency")
    from_raw = source.get("from")
    to_raw = source.get("to")

    # --- ИСПРАВЛЕНИЕ ЛОГИКИ СУММЫ И ВАЛЮТЫ ---
    # Если amount нет или None -> ставим 0. Если currency нет -> RUB.
    # Это нужно, чтобы тесты проходили assert "Сумма: 0 RUB"
    final_amount = 0
    if amount is not None:
        try:
            final_amount = float(amount)
        except (ValueError, TypeError):
            final_amount = 0

    final_currency = _get_currency_name(currency_raw)

    # Форматируем сумму:
    # - Если число целое (например 250.0), пишем как int (250)
    # - Если дробное, оставляем 1 знак после запятой, если второй ноль, иначе 2 знака?
    #   Судя по ошибке теста "250.5", нам нужно убрать лишний ноль.

    if final_amount.is_integer():
        amount_str = f"Сумма: {int(final_amount)} {final_currency}"
    else:
        # Форматируем так, чтобы убрать лишний ноль в конце, если он есть
        # Например: 250.50 -> 250.5, 250.25 -> 250.25
        formatted_val = f"{final_amount:.2f}".rstrip('0').rstrip('.')
        amount_str = f"Сумма: {formatted_val} {final_currency}"

    # 4. Отправитель и получатель (с маскированием)
    from_str = mask_account_card(from_raw) if from_raw is not None else "Неизвестно"
    to_str = mask_account_card(to_raw) if to_raw is not None else "Неизвестно"

    # Сборка результата
    lines = [
        date_str,
        f"Описание: {description}",
        f"{from_str} -> {to_str}",
        amount_str
    ]

    return "\n".join(lines)


def main():
    print("Программа: Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Пользователь: ")
    file_type = None
    file_path = None

    # Выбор файла
    if choice == "1":
        file_type = "json"
        file_path = "Домашка/data/transactions.json"
        print("Программа: Для обработки выбран JSON-файл.")
    elif choice == "2":
        file_type = "csv"
        file_path = "tests/data/transactions.csv"
        print("Программа: Для обработки выбран CSV-файл.")
    elif choice == "3":
        file_type = "xlsx"
        file_path = "tests/data/transactions_excel.xlsx"
        print("Программа: Для обработки выбран XLSX-файл.")
    else:
        print("Программа: Неверный выбор пункта меню. Завершение работы.")
        return

    # 1. Загрузка данных
    data = read_data(file_type, file_path)

    if data is None:
        print("Программа: Не удалось загрузить данные. Завершение работы.")
        return

    # 2. Фильтрация по статусу
    while True:
        status = input("Программа: Введите статус, по которому необходимо выполнить фильтрацию.\n"
                       f"Доступные для фильтровки статусы: {', '.join(ALLOWED_STATUSES)}\n"
                       "Пользователь: ").strip().upper()

        if status in ALLOWED_STATUSES:
            data = filter_by_state(data, status)
            print(f'Программа: Операции отфильтрованы по статусу "{status}"')
            break
        else:
            print(f'Программа: Статус операции "{status}" недоступен.')

    # 3. Сортировка
    sort_choice = input('Программа: Отсортировать операции по дате? Да/Нет\nПользователь: ').strip().lower()
    if sort_choice in ['да', 'yes']:
        order = input('Программа: Отсортировать по возрастанию или по убыванию?\nПользователь: ').strip().lower()
        reverse = order in ['по убыванию', 'убывание']
        data = sort_by_date(data, reverse=reverse)

    # 4. Только рублевые транзакции
    ruble_choice = input('Программа: Выводить только рублевые транзакции? Да/Нет\nПользователь: ').strip().lower()
    if ruble_choice in ['да', 'yes']:
        filtered_data = []
        for op in data:
            currency_info = op.get("currency", {})
            if isinstance(currency_info, dict) and currency_info.get("code") == "RUB":
                filtered_data.append(op)
        data = filtered_data
        print("Программа: Отфильтрованы только рублевые операции.")

    # 5. Поиск по описанию
    search_choice = input(
        'Программа: Отфильтровать список транзакций по определенному слову в описании? Да/Нет\nПользователь: '
    ).strip().lower()
    if search_choice in ['да', 'yes']:
        search_term = input("Программа: Введите слово для поиска:\nПользователь: ").strip()
        data = process_bank_search(data, search_term)

    # 6. Вывод
    print("\nПрограмма: Распечатываю итоговый список транзакций...")

    if not data:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    else:
        print(f"\nВсего банковских операций в выборке: {len(data)}")
        for op in data:
            print(format_transaction(op))
            print()


if __name__ == "__main__":
    main()
