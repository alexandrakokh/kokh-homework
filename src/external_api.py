import os
from typing import Dict
import requests
from dotenv import load_dotenv


load_dotenv()


API_KEY = os.getenv('EXCHANGE_API_KEY')
BASE_URL = 'https://api.apilayer.com/exchangerates_data/latest'  # исправляем протокол

def convert_to_rubles(transaction: Dict) -> float:
    """
    Конвертирует сумму транзакции в рубли.
    Args:
        transaction (Dict): Словарь с данными о транзакции, должен содержать ключи
            'amount' и 'currency'.
    Returns:
        float: Сумма в рублях.
    """
    amount = transaction.get('amount', 0.0)
    currency = transaction.get('currency', 'RUB')

    if currency == 'RUB':
        return float(amount)

    if currency not in ['USD', 'EUR']:
        raise ValueError(f"Неподдерживаемая валюта: {currency}")

    rate = _get_exchange_rate(currency)
    if rate is None:
        raise ConnectionError("Не удалось получить курс валюты")

    return float(amount * rate)


def _get_exchange_rate(base_currency: str) -> float | None:
    params = {'base': base_currency, 'symbols': 'RUB'}
    # Исправляем заголовок: используем 'apikey' и подставляем реальный ключ
    headers = {'apikey': API_KEY}

    try:
        response = requests.get(BASE_URL, params=params, headers=headers, timeout=10)
        response.raise_for_status()  # Выбросит ошибку, если HTTP статус 4xx или 5xx
        data = response.json()
        return float(data['rates']['RUB'])
    except (requests.RequestException, KeyError, ValueError) as e:
        # Дополнительно логируем ошибку для отладки
        print(f"Ошибка получения курса для {base_currency}: {e}")
        return None