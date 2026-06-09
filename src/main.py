from .search import search_transactions_by_description
from .analysis import count_transaction_categories
from .data_reader import (
    read_transactions_from_csv,
    read_transactions_from_excel,
    read_transactions_from_json
)


def main():
    print("Программа: Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Ваш выбор: ")

    if choice == '1':
        file_path = input("Введите путь к JSON-файлу: ")
        transactions = read_transactions_from_json(file_path)
    elif choice == '2':
        file_path = input("Введите путь к CSV-файлу: ")
        transactions = read_transactions_from_csv(file_path)
    elif choice == '3':
        file_path = input("Введите путь к XLSX-файлу: ")
        transactions = read_transactions_from_excel(file_path)
    else:
        print("Неверный выбор")
        return

    if not transactions:
        print("Данные не были загружены")
        return

    print("\nДанные успешно загружены. Выберите действие:")
    print("1. Поиск транзакций по описанию")
    print("2. Анализ категорий транзакций")

    action = input("Ваш выбор: ")

    if action == '1':
        search_term = input("Введите текст для поиска: ")
        results = search_transactions_by_description(transactions, search_term)
        print(f"\nНайдено {len(results)} транзакций:")
        for tx in results:
            print(f"ID: {tx.get('id')}, Описание: {tx.get('description')}, Сумма: {tx.get('amount')}")

    elif action == '2':
        categories = input("Введите категории для анализа через запятую: ").split(',')
        categories = [cat.strip() for cat in categories]
        analysis_result = count_transaction_categories(transactions, categories)
        print("\nРезультаты анализа:")
        for category, count in analysis_result.items():
            print(f"Категория '{category}': {count} транзакций")

    else:
        print("Неверный выбор действия")


if __name__ == "__main__":
    main()