import requests
from dotenv import load_dotenv
import os
from typing import Dict

load_dotenv()

API_KEY = os.environ.get('EXCHANGE_API_KEY')
BASE_URL = 'https://api.apilayer.com/exchangerates_data/latest'

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
    headers = {'apikey': API_KEY}

    try:
        response = requests.get(BASE_URL, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return float(data['rates']['RUB'])
    except Exception as e:  # Перехватываем ВСЕ исключения
        print(f"Ошибка получения курса для {base_currency}: {e}")
        return None