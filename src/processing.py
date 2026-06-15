import re
from datetime import datetime
from typing import Any, Dict, List


def filter_by_state(data: List[Dict[str, Any]], state: str) -> List[Dict[str, Any]]:
    """Фильтрует операции по статусу."""
    return [op for op in data if op.get("state") == state]


def sort_by_date(transactions: List[Dict[str, Any]], reverse: bool = False) -> List[Dict[str, Any]]:
    """
    Сортирует транзакции по дате.
    ВАЖНО: Если формат даты неверен, функция должна выбрасывать ValueError.
    """
    if not isinstance(transactions, list):
        return []

    def get_sort_key(transaction: Dict[str, Any]):
        date_str = transaction.get("date")

        if not date_str:
            return None

        try:
            return datetime.fromisoformat(date_str)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Неверный формат даты: '{date_str}'") from e

    return sorted(transactions, key=get_sort_key, reverse=reverse)


def process_bank_operations(data: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество транзакций для каждой категории.
    Учитывает падежи (множественное число) за счет усечения окончания.
    """
    result = {cat: 0 for cat in categories}  # Инициализируем счетчики

    for transaction in data:
        desc = transaction.get("description", "")
        if not desc:
            continue
        desc_lower = desc.lower()

        matched = False
        for category in categories:
            cat_lower = category.lower()

            # Проверяем 3 варианта: полное слово -> -2 буквы -> -1 буква
            for test_word in [cat_lower, cat_lower[:-2], cat_lower[:-1]]:
                if not test_word:
                    continue
                # Ищем корень в любом месте описания (игнорируя регистр)
                if re.search(re.escape(test_word), desc_lower):
                    result[category] += 1
                    matched = True
                    break  # Нашли категорию, переходим к следующей транзакции
            if matched:
                break

    return result


def process_bank_search(data: list, search_term: str) -> list:
    """
    Фильтрует транзакции по ключевому слову в описании.
    Ищет подстроку search_term в поле description (регистронезависимо).
    """
    if not search_term:
        return data

    term = search_term.lower()
    result = []

    for op in data:
        desc = op.get("description", "")
        if term in desc.lower():
            result.append(op)

    return result
