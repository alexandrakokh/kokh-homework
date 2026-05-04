import pytest
from datetime import datetime

@pytest.fixture
def sample_transactions():
    """Фикстура с тестовыми данными для транзакций."""
    return [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]

@pytest.fixture
def card_numbers():
    """Фикстура с номерами карт для тестирования."""
    return {
        'valid_16_digit': '1234567890123456',
        'valid_13_digit': '1234567890123',
        'valid_19_digit': '1234567890123456789',
        'invalid_short': '123456789012',
        'invalid_long': '12345678901234567890',
        'with_spaces': '1234 5678 9012 3456',
        'non_digits': '123abc456def',
        'empty': '',
    }

@pytest.fixture
def account_numbers():
    """Фикстура с номерами счетов для тестирования."""
    return {
        'valid_20_digit': '12345678901234567890',
        'short_4_digit': '1234',
        'short_3_digit': '123',
        'non_digits': 'abc123def456',
        'empty': '',
    }

@pytest.fixture
def date_strings():
    """Фикстура со строками дат для тестирования."""
    return {
        'valid_iso': '2024-03-11T02:26:18.671407',
        'valid_no_microseconds': '2023-12-25T15:30:45',
        'invalid_format': '11-03-2024 02:26:18',
        'empty': '',
        'none': None,
    }