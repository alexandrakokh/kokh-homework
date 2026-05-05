def filter_by_currency(transactions, currency_code):
    """Фильтрует транзакции по коду валюты."""
    if transactions is None:
        return

    for transaction in transactions:
        try:
            if (transaction.get('operationAmount', {})
                    .get('currency', {})
                    .get('code') == currency_code):
                yield transaction
        except (AttributeError, TypeError):
            continue


def transaction_descriptions(transactions):
    """Генератор, который возвращает описания транзакций по очереди."""
    if transactions is None:
        return

    for transaction in transactions:
        yield transaction.get('description', '')

def card_number_generator(start, end):
    """Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX."""
    # Проверка типов
    if not isinstance(start, int) or not isinstance(end, int):
        raise TypeError("Начальное и конечное значения должны быть целыми числами")

    # Проверка корректности входных параметров
    if start < 1:
        raise ValueError("Начальное значение должно быть не меньше 1")
    if end > 9999999999999999:  # 16-значное максимальное число
        raise ValueError("Конечное значение не может превышать 9999999999999999")
    if start > end:
        raise ValueError("Начальное значение не может быть больше конечного")

    for num in range(start, end + 1):
        # Преобразуем число в строку и дополняем нулями слева до 16 цифр
        num_str = str(num).zfill(16)
        # Разбиваем строку на блоки по 4 символа и соединяем пробелами
        formatted_card = ' '.join([num_str[i:i + 4] for i in range(0, 16, 4)])
        yield formatted_card