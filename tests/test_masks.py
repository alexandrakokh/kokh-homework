import pytest
from src.masks import get_mask_card_number, get_mask_account


class TestGetMaskCardNumber:
    @pytest.mark.parametrize("card_input,expected", [
        ('1234567890123456', '123456******3456'),
        ('1234567890123', '123456*****123'),
        ('1234567890123456789', '123456*********789'),
    ])
    def test_valid_card_numbers(self, card_input, expected):
        """Тестирование корректного маскирования номеров карт разной длины."""
        result = get_mask_card_number(card_input)
        assert result == expected

    @pytest.mark.parametrize("invalid_input", [
        '123456789012',  # слишком короткий
        '12345678901234567890',  # слишком длинный
        '123abc456def',  # содержит буквы
        '',  # пустая строка
    ])
    def test_invalid_card_numbers(self, invalid_input):
        """Тестирование обработки некорректных номеров карт."""
        with pytest.raises(ValueError):
            get_mask_card_number(invalid_input)


class TestGetMaskAccount:
    @pytest.mark.parametrize("account_input,expected", [
        ('12345678901234567890', '**7890'),  # длинный номер счёта
        ('1234', '**1234'),  # короткий номер (4 цифры)
        ('123', '**123'),  # очень короткий номер (3 цифры)
        ('001234', '**1234'),  # номер с ведущими нулями
        ('1', '**1'),  # минимальный номер (1 цифра)
        ('12', '**12'),  # номер из 2 цифр
    ])
    def test_valid_account_numbers(self, account_input, expected):
        """Тестирование корректного маскирования номеров счетов (включая граничные случаи)."""
        result = get_mask_account(account_input)
        assert result == expected

    @pytest.mark.parametrize("non_digit_input", [
        '123abc',
        'abc123',
        '12a34',
        '!@#$%',
    ])
    def test_non_digit_account(self, non_digit_input):
        """Тестирование обработки номеров счетов с нечисловыми символами."""
        with pytest.raises(ValueError):
            get_mask_account(non_digit_input)

    @pytest.mark.parametrize("empty_input", [
        '',
        None,
    ])
    def test_empty_account(self, empty_input):
        """Тестирование пустого или None номера счёта."""
        with pytest.raises(ValueError):
            get_mask_account(empty_input)