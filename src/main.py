from datetime import datetime
from src.masks import get_mask_card_number
from src.data_reader import read_data
from src.processing import (
    process_bank_search,
    filter_by_state,
    sort_by_date
)
from typing import List, Dict

ALLOWED_STATUSES = {"EXECUTED", "CANCELED", "PENDING"}


def format_transaction(op: Dict) -> str:
    """Форматирует одну транзакцию для вывода (с маской и датой)."""

    # 1. Формируем дату
    date_iso = op.get("date")
    try:
        parsed_date = datetime.fromisoformat(date_iso)
        date_formatted = parsed_date.strftime("%d.%m.%Y")
    except (ValueError, TypeError):
        date_formatted = "Неизвестная дата"

    # 2. Описание
    desc = op.get("description", "Неизвестно")

    # 3. Маскируем номера
    from_number = op.get("from")
    to_number = op.get("to")

    from_masked = get_mask_card_number(from_number) if from_number else "Неизвестно"
    to_masked = get_mask_card_number(to_number) if to_number else "Неизвестно"

    # 4. Сумма и валюта
    amount = op.get("amount", 0)
    currency = op.get("currency", {}).get("name", "RUB")

    # 5. Собираем итоговую строку
    result = (
        f"{date_formatted} {desc}\n"
        f"{from_masked} -> {to_masked}\n"
        f"Сумма: {amount} {currency}"
    )
    return result


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
        file_path = "data/transactions.json"
        print("Программа: Для обработки выбран JSON-файл.")
    elif choice == "2":
        file_type = "csv"
        file_path = "data/transactions.csv"
        print("Программа: Для обработки выбран CSV-файл.")
    elif choice == "3":
        file_type = "xlsx"
        file_path = "data/transactions_excel.xlsx"
        print("Программа: Для обработки выбран XLSX-файл.")
    else:
        print("Программа: Неверный выбор пункта меню. Завершение работы.")
        return

    # 1. Загрузка данных (используем ваш data_reader)
    data = read_data(file_type, file_path)

    # ПРОВЕРКА НА ОШИБКУ ЗАГРУЗКИ (None)
    # Если read_data вернула None — печатаем ошибку и завершаем работу
    if data is None:
        print("Программа: Не удалось загрузить данные. Завершение работы.")
        return

    # 2. Фильтрация по статусу (используем filter_by_state из processing.py)
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

    # 3. Сортировка (используем sort_by_date из processing.py)
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
            # Проверяем, есть ли ключ 'code' и равен ли он 'RUB'
            if isinstance(currency_info, dict) and currency_info.get("code") == "RUB":
                filtered_data.append(op)
        data = filtered_data
        print("Программа: Отфильтрованы только рублевые операции.")

    # 5. Поиск по описанию (используем process_bank_search из processing.py)
    search_choice = input(
        'Программа: Отфильтровать список транзакций по определенному слову в описании? Да/Нет\nПользователь: '
    ).strip().lower()
    if search_choice in ['да', 'yes']:
        search_term = input("Программа: Введите слово для поиска:\nПользователь: ").strip()
        data = process_bank_search(data, search_term)

    # 6. Вывод
    print("\nПрограмма: Распечатываю итоговый список транзакций...")

    # ПРОВЕРКА НА ПУСТОЙ СПИСОК (данные загружены успешно, но список пуст)
    if not data:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    else:
        print(f"\nВсего банковских операций в выборке: {len(data)}")
        for op in data:
            print(format_transaction(op))
            print()  # Пустая строка между операциями


if __name__ == "__main__":
    main()
