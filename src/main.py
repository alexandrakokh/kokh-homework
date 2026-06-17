from datetime import datetime
from typing import Any, Dict
from pathlib import Path

from src.masks import mask_account_card
from src.data_reader import read_data
from src.processing import process_bank_search, filter_by_state, sort_by_date

ALLOWED_STATUSES = {"EXECUTED", "CANCELED", "PENDING"}


def _parse_date(date_val: Any) -> str:
    """Парсит дату в формат ДД.ММ.ГГГГ или возвращает заглушку."""
    if date_val is None or date_val == "":
        return "Неизвестная дата"

    date_str = str(date_val).strip()
    if date_str.endswith("Z"):
        date_str = date_str[:-1]

    formats = ["%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]

    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime("%d.%m.%Y")
        except ValueError:
            continue
    return "Неизвестная дата"


def _get_currency_name(currency_val: Any) -> str:
    """Извлекает код валюты (например, EUR, CNY). Если данных нет — пишет 'Не указана'."""
    if not currency_val:
        return "Не указана"

    if isinstance(currency_val, dict):
        # Сначала пробуем взять code (код), если пусто — fallback на name
        return currency_val.get("code", currency_val.get("name", "Не указана"))

    # Для Excel: если это просто строка "Peso" или число 643, возвращаем как есть (или можно добавить маппинг)
    return str(currency_val).strip()


def format_transaction(transaction: Dict[str, Any]) -> str:
    raw_date = transaction.get("date")
    date_str = _parse_date(raw_date)

    description = transaction.get("description", "Без описания")
    description = str(description)

    # Извлечение суммы и валюты
    source = transaction.get("operationAmount") or transaction
    amount = source.get("amount")
    currency_raw = source.get("currency")

    if not currency_raw:
        currency_raw = transaction.get("currency_code") or transaction.get("currency_name")

    from_raw = transaction.get("from")
    to_raw = transaction.get("to")

    final_amount = 0
    if amount is not None:
        try:
            final_amount = float(amount)
        except ValueError, TypeError:
            final_amount = 0

    # ВАЖНЫЙ МОМЕНТ: берем код валюты, а не название
    final_currency_code = _get_currency_name(currency_raw)

    if final_amount.is_integer():
        amount_str = f"Сумма: {int(final_amount)} {final_currency_code}"
    else:
        formatted_val = f"{final_amount:.2f}".rstrip("0").rstrip(".")
        amount_str = f"Сумма: {formatted_val} {final_currency_code}"

    from_str = mask_account_card(from_raw) if from_raw else "Неизвестно"
    to_str = mask_account_card(to_raw) if to_raw else "Неизвестно"

    lines = [date_str, f"Описание: {description}", f"{from_str} -> {to_str}", amount_str]

    return "\n".join(lines)


def main():
    base_dir = Path(__file__).resolve().parent

    print("Программа: Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Пользователь: ")
    file_type = None
    file_path = None

    if choice == "1":
        file_type = "json"
        file_path = base_dir.parent / "data" / "transactions.json"
        print("Программа: Для обработки выбран JSON-файл.")
    elif choice == "2":
        file_type = "csv"
        file_path = base_dir.parent / "tests" / "data" / "transactions.csv"
        print("Программа: Для обработки выбран CSV-файл.")
    elif choice == "3":
        file_type = "xlsx"
        file_path = base_dir.parent / "tests" / "data" / "transactions_excel.xlsx"
        print("Программа: Для обработки выбран XLSX-файл.")
    else:
        print("Программа: Неверный выбор пункта меню. Завершение работы.")
        return

    if file_path and not file_path.exists():
        print(f"Программа: Ошибка! Файл не найден по пути: {file_path}")
        return

    data = read_data(file_type, str(file_path))
    if data is None:
        print("Программа: Не удалось загрузить данные. Завершение работы.")
        return

    while True:
        status = (
            input(
                "Программа: Введите статус, по которому необходимо выполнить фильтрацию.\n"
                f"Доступные для фильтровки статусы: {', '.join(ALLOWED_STATUSES)}\n"
                "Пользователь: "
            )
            .strip()
            .upper()
        )

        if status in ALLOWED_STATUSES:
            data = filter_by_state(data, status)
            print(f'Программа: Операции отфильтрованы по статусу "{status}"')
            break
        else:
            print(f'Программа: Статус операции "{status}" недоступен.')

    sort_choice = input("Программа: Отсортировать операции по дате? Да/Нет\nПользователь: ").strip().lower()
    if sort_choice in ["да", "yes"]:
        order = input("Программа: Отсортировать по возрастанию или по убыванию?\nПользователь: ").strip().lower()
        reverse = order in ["по убыванию", "убывание"]
        data = sort_by_date(data, reverse=reverse)

    ruble_choice = input("Программа: Выводить только рублевые транзакции? Да/Нет\nПользователь: ").strip().lower()

    if ruble_choice in ["да", "yes"]:
        filtered_data = []
        for op in data:
            currency_code = None

            # 1. Проверяем вложенный объект
            op_amount = op.get("operationAmount")
            if op_amount and isinstance(op_amount, dict):
                curr_info = op_amount.get("currency")
                if curr_info and isinstance(curr_info, dict):
                    currency_code = curr_info.get("code")
                elif isinstance(curr_info, str):  # Если просто строка
                    currency_code = curr_info

            # 2. Если не нашли — берем из корневых полей (Excel)
            if not currency_code:
                currency_code = op.get("currency_code") or op.get("currency_name")

            # 3. Сравниваем (приводим к строке на всякий случай)
            if str(currency_code).upper() == "RUB":
                filtered_data.append(op)

        data = filtered_data
        print("Программа: Отфильтрованы только рублевые операции.")
    else:
        print("Программа: Фильтр по валюте не применен.")

    search_choice = (
        input("Программа: Отфильтровать список транзакций по определенному слову в описании? Да/Нет\nПользователь: ")
        .strip()
        .lower()
    )
    if search_choice in ["да", "yes"]:
        search_term = input("Программа: Введите слово для поиска:\nПользователь: ").strip()
        data = process_bank_search(data, search_term)

    print("\nПрограмма: Распечатываю итоговый список транзакций...")

    if not data:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    else:
        print(f"\nВсего банковских операций в выборке: {len(data)}")
        for op in data:
            print(format_transaction(op))
            print()  # Пустая строка между транзакциями для читаемости

    print("Программа: Завершение работы.")


if __name__ == "__main__":
    main()
