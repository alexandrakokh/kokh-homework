import requests
import os
from typing import Dict

# Загрузка переменных окружения
os.environ.get('EXCHANGE_API_KEY')

# URL для конвертации
BASE_URL = 'https://api.apilayer.com/exchangerates_data/convert'

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
    currency = transaction.get('currency', 'RUB').upper()  # Приводим к верхнему регистру

    if currency == 'RUB':
        return float(amount)

    if currency not in ['USD', 'EUR']:
        raise ValueError(f"Неподдерживаемая валюта: {currency}")

    try:
        rate = _get_exchange_rate(currency)
        return float(amount * rate)
    except Exception as e:
        raise ConnectionError(f"Ошибка при конвертации {amount} {currency} в RUB: {e}")


def _get_exchange_rate(base_currency: str) -> float:
    """
    Получает актуальный курс конвертации из API.
    """
    # Получаем ключ из окружения
    api_key = os.getenv('EXCHANGE_API_KEY')
    if not api_key:
        raise ValueError("API key not found. Set environment variable 'EXCHANGE_API_KEY'.")

    params = {
        'from': base_currency,
        'to': 'RUB',
        'amount': 1  # Берём 1 единицу, чтобы получить чистый курс
    }
    headers = {'apikey': api_key}

    try:
        response = requests.get(
            BASE_URL,
            params=params,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()  # Бросает исключение при 4xx/5xx ошибках

        data = response.json()
        if data.get('success'):
            return float(data['result'])  # Результат уже в рублях
        else:
            raise Exception(f"API error: {data.get('error', {}).get('info')}")

    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Ошибка сети при запросе курса: {e}")
    except (KeyError, TypeError) as e:
        raise ValueError(f"Ошибка парсинга ответа API: {e}")