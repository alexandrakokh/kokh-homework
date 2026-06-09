from .search import search_transactions_by_description
from .analysis import count_transaction_categories
from .data_reader import (
    read_transactions_from_csv,
    read_transactions_from_excel,
    read_transactions_from_json
)


def filter_by_status(transactions, status):
    """Фильтрация транзакций по статусу"""
    return [tx for tx in transactions if tx.get('status') == status]


def get_valid_status(transactions):
    """
    Запрашивает у пользователя статус и проверяет его наличие в данных.
    Возвращает корректный статус или None, если пользователь хочет отменить.
    """
    available_statuses = set(tx.get('status') for tx in transactions if tx.get('status'))

    print("\nДоступные статусы транзакций:")
    print(", ".join(available_statuses))

    while True:
        status_filter = input("Введите статус для фильтрации (или 'отмена' для выхода): ").strip()

        if status_filter.lower() == 'отмена':
            return None

        if status_filter in available_statuses:
            return status_filter
        else:
            print(f"⚠️ Статус '{status_filter}' не найден в данных. Пожалуйста, выберите один из доступных выше.")


def filter_by_amount(transactions):
    """Дополнительная фильтрация по сумме"""
    try:
        min_input = input("Введите минимальную сумму (оставьте пустым, чтобы не фильтровать): ").strip()
        max_input = input("Введите максимальную сумму (оставьте пустым, чтобы не фильтровать): ").strip()

        amount_min = float(min_input) if min_input else 0
        amount_max = float(max_input) if max_input else float('inf')

        filtered = [tx for tx in transactions
                    if amount_min <= tx.get('amount', 0) <= amount_max]

        print(f"✅ Отфильтровано по сумме [{amount_min}, {amount_max}]. Осталось записей: {len(filtered)}")
        return filtered
    except ValueError:
        print("❌ Ошибка ввода суммы. Фильтрация по сумме пропущена.")
        return transactions


def print_transactions(transactions):
    """Красивый вывод списка транзакций"""
    if not transactions:
        print("📭 Список транзакций пуст.")
        return

    print(f"\n{'ID':<10} | {'Дата':<12} | {'Категория':<15} | {'Статус':<10} | {'Сумма':>10}")
    print("-" * 75)

    for tx in transactions:
        tx_id = str(tx.get('id', 'N/A'))[:9]
        date = str(tx.get('date', 'N/A'))[:11]
        category = str(tx.get('category', 'N/A'))[:14]
        status = str(tx.get('status', 'N/A'))[:9]
        amount = tx.get('amount', 0)

        print(f"{tx_id:<10} | {date:<12} | {category:<15} | {status:<10} | ${amount:>9,.2f}")

    print("-" * 75)
    print(f"Всего отображено записей: {len(transactions)}")


def main():
    print("Программа: Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию из XLSX-файла")

    choice = input("Ваш выбор: ").strip()

    transactions = []
    if choice == '1':
        file_path = input("Введите путь к JSON-файлу: ").strip()
        transactions = read_transactions_from_json(file_path)
    elif choice == '2':
        file_path = input("Введите путь к CSV-файлу: ").strip()
        transactions = read_transactions_from_csv(file_path)
    elif choice == '3':
        file_path = input("Введите путь к XLSX-файлу: ").strip()
        transactions = read_transactions_from_excel(file_path)
    else:
        print("Неверный выбор")
        return

    if not transactions:
        print("Данные не были загружены или файл пуст.")
        return

    print("\nДанные успешно загружены. Выберите действие:")
    print("1. Поиск транзакций по описанию")
    print("2. Анализ категорий транзакций")
    print("3. Расширенная фильтрация (статус + дополнительные параметры)")

    action = input("Ваш выбор: ").strip()

    if action == '1':
        search_term = input("Введите текст для поиска в описании: ").strip()
        if search_term:
            results = search_transactions_by_description(transactions, search_term)
            print_transactions(results)
        else:
            print("Текст поиска не введен.")

    elif action == '2':
        # Исправление логики анализа: функция count_transaction_categories в исходном коде
        # вероятно, ожидает просто список транзакций, а не список категорий.
        # Предполагаем, что она сама считает все категории. Если нужна фильтрация - меняем логику.
        categories_data, total_amount = count_transaction_categories(transactions)

        print("\n--- Отчет по категориям ---")
        print(f"{'Категория':<20} | {'Количество':<10} | {'Сумма':>12}")
        print("-" * 55)
        for cat, data in categories_data.items():
            print(f"{cat:<20} | {data['count']:<10} | ${data['total_amount']:>11,.2f}")
        print("-" * 55)
        print(f"{'ИТОГО':<20} | {sum(d['count'] for d in categories_data.values()):<10} | ${total_amount:>11,.2f}")

    elif action == '3':
        # 1. Фильтрация по статусу с валидацией
        selected_status = get_valid_status(transactions)

        if selected_status is None:
            print("Фильтрация отменена пользователем.")
            return

        filtered_by_status = filter_by_status(transactions, selected_status)
        print(f"\n✅ Найдено {len(filtered_by_status)} транзакций со статусом '{selected_status}'.")

        # 2. Дополнительная фильтрация по сумме
        apply_amount_filter = input("Хотите дополнительно отфильтровать по сумме? (да/нет): ").strip().lower()
        current_results = filtered_by_status

        if apply_amount_filter == 'да':
            current_results = filter_by_amount(current_results)

        # 3. Дополнительная фильтрация по описанию
        apply_desc_filter = input("Хотите дополнительно отфильтровать по описанию? (да/нет): ").strip().lower()

        if apply_desc_filter == 'да':
            search_term = input("Введите текст для поиска: ").strip()
            if search_term:
                current_results = search_transactions_by_description(current_results, search_term)
                print(f"✅ После поиска по описанию осталось {len(current_results)} записей.")

        # Вывод финального результата
        print_transactions(current_results)

    else:
        print("Неверный выбор действия")


if __name__ == "__main__":
    main()