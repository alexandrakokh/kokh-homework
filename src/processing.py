from typing import List, Dict, Any
from datetime import datetime


def filter_by_state(
    transactions: List[Dict[str, Any]],
    state: str = 'EXECUTED'
) -> List[Dict[str, Any]]:
    """Фильтрует список словарей с данными о банковских операциях по значению ключа 'state'."""
    if not isinstance(transactions, list):
        raise TypeError("transactions должен быть списком")

    filtered = []
    for transaction in transactions:
        if isinstance(transaction, dict) and 'state' in transaction:
            if transaction['state'] == state:
                filtered.append(transaction)
    return filtered


def sort_by_date(
    transactions: List[Dict[str, Any]],
    reverse: bool = False
) -> List[Dict[str, Any]]:
    """Сортирует список словарей с данными о банковских операциях по дате."""
    if not isinstance(transactions, list):
        raise TypeError("transactions должен быть списком")

    if not transactions:
        return []

    def parse_date(transaction: Dict[str, Any]) -> datetime:
        date_str = transaction.get('date')
        if date_str is None:
            raise ValueError(f"Отсутствует поле 'date' в транзакции с id={transaction.get('id', 'unknown')}")
        try:
            return datetime.fromisoformat(date_str)
        except ValueError as e:
            raise ValueError(
                f"Неверный формат даты '{date_str}' в транзакции с id={transaction.get('id', 'unknown')}"
            ) from e

    # Добавляем индекс исходного положения для сохранения порядка при одинаковых датах
    indexed_transactions = [(i, transaction) for i, transaction in enumerate(transactions)]

    # Сортируем только по дате — стабильность сортировки гарантирует сохранение порядка для равных дат
    sorted_indexed = sorted(
        indexed_transactions,
        key=lambda x: parse_date(x[1]),
        reverse=reverse
    )

    # Извлекаем только транзакции, отбрасывая индексы
    return [transaction for _, transaction in sorted_indexed]