from typing import List, Dict, Any
from datetime import datetime


def filter_by_state(
    transactions: List[Dict[str, Any]],
    state: str = 'EXECUTED'
) -> List[Dict[str, Any]]:
    """Фильтрует список словарей с данными о банковских операциях по значению ключа 'state'."""
    return [transaction for transaction in transactions if transaction.get('state') == state]


def sort_by_date(
    transactions: List[Dict[str, Any]],
    reverse: bool = True
) -> List[Dict[str, Any]]:
    """Сортирует список словарей с данными о банковских операциях по дате."""


    def parse_date(transaction: Dict[str, Any]) -> datetime:
        date_str = transaction['date']
        try:
            return datetime.fromisoformat(date_str)
        except ValueError as e:
            raise ValueError(f"Неверный формат даты '{date_str}' в транзакции {transaction['id']}") from e

    return sorted(transactions, key=parse_date, reverse=reverse)


# Примеры использования функций
if __name__ == "__main__":
    # Пример данных для тестирования
    sample_data = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]

    print("Тестирование filter_by_state:")
    print("По умолчанию (EXECUTED):")
    print(filter_by_state(sample_data))
    print("\nCANCELED:")
    print(filter_by_state(sample_data, 'CANCELED'))

    print("\nТестирование sort_by_date:")
    print("Сортировка по убыванию:")
    print(sort_by_date(sample_data))
    print("\nСортировка по возрастанию:")
    print(sort_by_date(sample_data, reverse=False))