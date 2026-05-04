import pytest
from src.widget import mask_account_card, get_date

@pytest.fixture
def date_strings():
    return {
        'valid_iso': '2024-03-11T02:26:18.123456',
        'valid_no_microseconds': '2023-12-25T10:30:45',
        'future_date': '2030-12-31T23:59:59'
    }

class TestMaskAccountCard:
    @pytest.mark.parametrize("input_string,expected_card", [
        ("Maestro 1234567890123456", "Maestro 123456******3456"),
        ("Visa 1234567890123", "Visa 123456*****123"),
    ])
    def test_card_masking(self, input_string, expected_card):
        """Тестирование маскирования номеров карт."""
        result = mask_account_card(input_string)
        assert result == expected_card


    @pytest.mark.parametrize("input_string,expected_account", [
        ("Счёт 12345678901234567890", "Счёт **7890"),
        ("Account 1234", "Account **1234"),
        ("счет 123", "счет **123"),
    ])
    def test_account_masking(self, input_string, expected_account):
        """Тестирование маскирования номеров счетов."""
        result = mask_account_card(input_string)
        assert result == expected_account

    def test_no_number_in_string(self):
        """Тестирование строки без номера."""
        with pytest.raises(ValueError, match="В строке не найден номер карты или счёта"):
            mask_account_card("Без номера")


    @pytest.mark.parametrize("keyword", ['счёт', 'счет', 'account', 'account number'])
    def test_different_account_keywords(self, keyword):
        """Тестирование различных вариантов написания «счёт»."""
        input_string = f"{keyword} 12345678901234567890"
        result = mask_account_card(input_string)
        assert "**7890" in result


class TestGetDate:
    def test_valid_iso_date(self, date_strings):
        """Тестирование корректного преобразования даты ISO."""
        result = get_date(date_strings['valid_iso'])
        assert result == "11.03.2024"

    def test_date_without_microseconds(self, date_strings):
        """Тестирование даты без микросекунд."""
        result = get_date(date_strings['valid_no_microseconds'])
        assert result == "25.12.2023"

    @pytest.mark.parametrize("invalid_date", [
        "11-03-2024 02:26:18",  # неверный формат
        "",  # пустая строка
    ])
    def test_invalid_date_formats(self, invalid_date):
        """Тестирование некорректных форматов дат."""
        with pytest.raises(ValueError):
            get_date(invalid_date)

    def test_future_date(self, date_strings):
        """Тестирование будущей даты."""
        result = get_date(date_strings['future_date'])
        assert result == "31.12.2030"