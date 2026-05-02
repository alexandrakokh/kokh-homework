import pytest
from masks import get_mask_card_number, get_mask_account


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
        ('12345678901234567890', '**7890'),
        ('1234', '**1234'),
        ('123', '**123'),  # короткий номер
    ])


    def test_valid_account_numbers(self, account_input, expected):
        """Тестирование корректного маскирования номеров счетов."""
        result = get_mask_account(account_input)
        assert result == expected


    def test_non_digit_account(self, account_numbers):
        """Тестирование обработки номеров счетов с нечисловыми символами."""
        with pytest.raises(ValueError):
            get_mask_account(account_numbers['non_digits'])

    def test_empty_account(self, account_numbers):
        """Тестирование пустого номера счёта."""
        with pytest.raises(ValueError):
            get_mask_account(account_numbers['empty'])