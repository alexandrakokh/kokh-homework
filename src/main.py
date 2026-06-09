from .search import search_transactions_by_description
from .analysis import count_transaction_categories
from .data_reader import (
    read_transactions_from_csv,
    read_transactions_from_excel,
    read_transactions_from_json
)
import re


def get_valid_status(transactions):
    """
    Запрашивает статус у пользователя и проверяет его наличие в данных.
    Цикл продолжается, пока не будет введен существующий статус или 'отмена'.
    """
    # Получаем уникальные статусы из загруженных данных
    available_statuses = set(tx.get('status') for tx in transactions if tx.get('status'))

    if not available_statuses:
        print("⚠️ В загруженных данных нет статусов транзакций.")
        return None

    print("\n--- Доступные статусы в файле ---")
    print(", ".join(available_statuses))
    print("---------------------------------")

    while True:
        status_filter = input("Введите статус для фильтрации (или 'отмена' для выхода): ").strip()

        if status_filter.lower() == 'отмена':
            return None

        if status_filter in available_statuses:
            return status_filter
        else:
            print(f"❌ Статус '{status_filter}' не найден в данных. Пожалуйста, выберите один из списка выше.")


def filter_by_amount(transactions):
    """
    Интерактивная фильтрация по сумме.
    Возвращает отфильтрованный список. При ошибке ввода возвращает текущий список.
    """
    try:
        min_input = input("Введите минимальную сумму (оставьте пустым для пропуска): ").strip()
        max_input = input("Введите максимальную сумму (оставьте пустым для пропуска): ").strip()

        amount_min = float(min_input) if min_input else 0
        amount_max = float(max_input) if max_input else float('inf')

        filtered = [
            tx for tx in transactions
            if amount_min <= tx.get('amount', 0) <= amount_max
        ]

        print(f"✅ Отфильтровано по сумме [{amount_min}, {amount_max}]. Осталось записей: {len(filtered)}")
        return filtered
    except ValueError:
        print("❌ Ошибка: Некорректный формат суммы. Фильтрация по сумме пропущена.")
        return transactions


def print_transactions(transactions):
    """Красивый вывод таблицы транзакций"""
    if not transactions:
        print("📭 Список транзакций пуст.")
        return

    # Заголовки таблицы
    header = f"{'ID':<10} | {'Дата':<12} | {'Категория':<15} | {'Статус':<10} | {'Сумма':>10}"
    separator = "-" * 75

    print(header)
    print(separator)

    for tx in transactions:
        tx_id = str(tx.get('id', 'N/A'))[:9]
        date = str(tx.get('date', 'N/A'))[:11]
        category = str(tx.get('category', 'N/A'))[:14]
        status = str(tx.get('status', 'N/A'))[:9]
        amount = tx.get('amount', 0)

        print(f"{tx_id:<10} | {date:<12} | {category:<15} | {status:<10} | ${amount:>9,.2f}")

    print(separator)
    print(f"Всего отображено записей: {len(transactions)}")


def main():
    print("=" * 60)
    print("Программа: Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("=" * 60)

    # 1. Выбор источника данных (Приветственное сообщение и выбор файла)
    print("\nВыберите источник данных:")
    print("1. JSON-файл")
    print("2. CSV-файл")
    print("3. Excel (.xlsx) файл")

    choice = input("Ваш выбор (1-3): ").strip()
    transactions = []

    if choice == '1':
        file_path = input("Введите путь к JSON-файлу: ").strip()
        transactions = read_transactions_from_json(file_path)
    elif choice == '2':
        file_path = input("Введите путь к CSV-файлу: ").strip()
        transactions = read_transactions_from_csv(file_path)
    elif choice == '3':
        file_path = input("Введите путь к Excel-файлу: ").strip()
        transactions = read_transactions_from_excel(file_path)
    else:
        print("Неверный выбор пункта меню.")
        return

    if not transactions:
        print("Данные не были загружены или файл пуст. Проверьте путь и формат файла.")
        return

    print(f"\n✅ Данные успешно загружены. Всего транзакций: {len(transactions)}")

    # 2. Выбор действия
    print("\nВыберите действие:")
    print("1. Поиск транзакций по описанию (регулярные выражения)")
    print("2. Анализ категорий транзакций (Counter)")
    print("3. Расширенная фильтрация (статус + доп. параметры)")

    action = input("Ваш выбор (1-3): ").strip()

    if action == '1':
        keyword = input("Введите текст для поиска в описании: ").strip()
        if keyword:
            results = search_transactions_by_description(transactions, keyword)
            print_transactions(results)
        else:
            print("Текст поиска не введен.")

    elif action == '2':
        # Вызов функции анализа, которая использует Counter внутри analysis.py
        categories_data, total_amount = count_transaction_categories(transactions)

        print("\n--- Отчет по категориям ---")
        print(f"{'Категория':<20} | {'Количество':<10} | {'Сумма':>12}")
        print("-" * 55)

        # Сортируем по сумме для наглядности
        sorted_cats = sorted(categories_data.items(), key=lambda x: x[1]['total_amount'], reverse=True)

        for cat, data in sorted_cats:
            print(f"{cat:<20} | {data['count']:<10} | ${data['total_amount']:>11,.2f}")

        print("-" * 55)
        total_count = sum(d['count'] for d in categories_data.values())
        print(f"{'ИТОГО':<20} | {total_count:<10} | ${total_amount:>11,.2f}")

    elif action == '3':
        # 3. Обработка фильтрации по статусам и дальнейшие вопросы

        # Шаг А: Валидация и выбор статуса
        selected_status = get_valid_status(transactions)

        if selected_status is None:
            print("Фильтрация отменена пользователем.")
            return

        # Фильтруем по статусу
        current_results = [tx for tx in transactions if tx.get('status') == selected_status]
        print(f"\n✅ Найдено {len(current_results)} транзакций со статусом '{selected_status}'.")

        # Шаг Б: Вопрос про сумму
        apply_amount = input("Хотите дополнительно отфильтровать по сумме? (да/нет): ").strip().lower()
        if apply_amount == 'да':
            current_results = filter_by_amount(current_results)

        # Шаг В: Вопрос про описание
        apply_desc = input("Хотите дополнительно отфильтровать по описанию? (да/нет): ").strip().lower()
        if apply_desc == 'да':
            keyword = input("Введите текст для поиска: ").strip()
            if keyword:
                # Используем функцию поиска с re из search.py
                current_results = search_transactions_by_description(current_results, keyword)
                print(f"✅ После поиска по описанию осталось {len(current_results)} записей.")

        # Вывод финального результата
        print_transactions(current_results)

    else:
        print("Неверный выбор действия.")


if __name__ == "__main__":
    main()