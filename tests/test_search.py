from src.search import process_bank_search  # Импортируем функцию под её рабочим именем


def test_search_finds_exact_match():
    """Тест: поиск находит точное совпадение."""
    transactions = [
        {"description": "Покупка в магазине"},
        {"description": "Оплата услуг"},
        {"description": "Перевод другу"},
    ]
    result = process_bank_search(transactions, "покупка")
    assert len(result) == 1
    assert result[0]["description"] == "Покупка в магазине"


def test_search_case_insensitive():
    """Тест: поиск нечувствителен к регистру (благодаря re.IGNORECASE)."""
    transactions = [{"description": "ПОКУПКА В МАГАЗИНЕ"}, {"description": "оплата услуг"}]
    # Ищем маленькими буквами, но находим заглавные
    result = process_bank_search(transactions, "покупка")
    assert len(result) == 1


def test_search_handles_special_characters():
    """Тест: поиск корректно обрабатывает спецсимволы (благодаря re.escape)."""
    transactions = [{"description": "Оплата счета №123?"}, {"description": "Обычный перевод"}]
    # В строке поиска есть спецсимвол '?', который re.escape экранирует
    result = process_bank_search(transactions, "№123?")
    assert len(result) == 1


def test_search_empty_string_returns_all():
    """Тест: если строка поиска пустая, возвращаются все транзакции."""
    transactions = [{"description": "Покупка"}, {"description": "Перевод"}]
    result = process_bank_search(transactions, "")
    assert len(result) == 2


def test_search_no_matches():
    """Тест: если совпадений нет, возвращается пустой список."""
    transactions = [{"description": "Покупка в магазине"}]
    result = process_bank_search(transactions, "такси")
    assert len(result) == 0
