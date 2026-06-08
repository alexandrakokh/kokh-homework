import os
from typing import Dict

import requests
from dotenv import load_dotenv

load_dotenv()

# Загрузка переменных окружения
API_KEY = os.environ.get("EXCHANGE_API_KEY")
BASE_URL = "https://api.apilayer.com/exchangerates_data/convert"


def convert_to_rubles(transaction: Dict) -> float:
    """
    Конвертирует сумму транзакции в рубли.
    Args:
        transaction (Dict): Словарь с данными о транзакции, должен содержать ключи
            'amount' и 'currency'.
    Returns:
        float: Сумма в рублях.
    """
    amount = transaction.get("amount", 0.0)
    currency = transaction.get("currency", "RUB").upper()

    # Проверка корректности суммы
    if not isinstance(amount, (int, float)) or amount < 0:
        raise ValueError(f"Некорректная сумма транзакции: {amount}")

    if currency == "RUB":
        return float(amount)

    if currency not in ["USD", "EUR"]:
        raise ValueError(f"Неподдерживаемая валюта: {currency}")

    try:
        rate = _get_exchange_rate(currency)
        converted_amount = float(amount * rate)
        return converted_amount
    except ConnectionError as e:
        raise ConnectionError(f"Ошибка сети при конвертации {amount} {currency} в RUB: {e}")
    except ValueError as e:
        if "API key not found" in str(e):
            raise ValueError("Не установлен API-ключ для конвертации валют")
        else:
            raise ValueError(f"Ошибка данных при конвертации {amount} {currency}: {e}")


def _get_exchange_rate(base_currency: str) -> float:
    """Получает актуальный курс конвертации из API."""
    # Считываем API‑ключ при каждом вызове
    api_key = os.environ.get("EXCHANGE_API_KEY")
    if not api_key:
        raise ValueError("API key not found. Set environment variable 'EXCHANGE_API_KEY'.")

    params = {"from": base_currency, "to": "RUB", "amount": 1}
    headers = {"apikey": api_key}  # Используем локальную переменную

    try:
        response = requests.get(BASE_URL, params=params, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()
        if data.get("success"):
            return float(data["result"])
        else:
            error_info = data.get("error", {}).get("info", "Unknown error")
            raise ValueError(f"API error: {error_info}")
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Ошибка сети при запросе курса: {e}")
    except (KeyError, TypeError) as e:
        raise ValueError(f"Ошибка парсинга ответа API: {e}")
