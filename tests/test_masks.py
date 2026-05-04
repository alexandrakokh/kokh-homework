import pytest
from src.masks import get_mask_card_number, get_mask_account


class TestGetMaskCardNumber:
    @pytest.mark.parametrize("card_input,expected", [
        ("1234567890123456", "123456****3456"),
        ("0000000000000000", "000000****0000"),
        ("9999888877776666", "999988****7766"),
        ("1111222233334444", "111122****3344"),
    ])
    def test_valid_card_masking(self, card_input, expected):
        """Тестирование корректного маскирования номера карты."""
        result = get_mask_card_number(card_input)
        assert result == expected

    @pytest.mark.parametrize("invalid_input,error_type,error_message", [
        ("", ValueError, "Номер карты должен содержать только цифры"),
        ("123456789012345", ValueError, "Номер карты должен содержать ровно 16 цифр"),
        ("12345678901234567", ValueError, "Номер карты должен содержать ровно 16 цифр"),
        ("1234abcd5678efgh", ValueError, "Номер карты должен содержать только цифры"),
    ])
    def test_invalid_card_inputs_raises_correct_error(self, invalid_input, error_type, error_message):
        """
        Тестирование, что функция выбрасывает правильные ошибки
        для некорректных входных данных.
        """
        with pytest.raises(error_type, match=error_message):
            get_mask_card_number(invalid_input)



class TestGetMaskAccount:
    @pytest.mark.parametrize("account_input,expected", [
        ("73654108430135874305", "**4305"),
        ("1234", "**1234"),
        ("0000", "**0000"),
    ])
    def test_valid_account_masking(self, account_input, expected):
        """Тестирование корректного маскирования номера счёта."""
        result = get_mask_account(account_input)
        assert result == expected

    @pytest.mark.parametrize("invalid_input,error_type,error_message", [
        ("", ValueError, "Номер счёта должен содержать только цифры"),
        ("123a", ValueError, "Номер счёта должен содержать только цифры"),
    ])
    def test_invalid_account_inputs_raises_correct_error(self, invalid_input, error_type, error_message):
        """Тестирование обработки некорректных входных данных для счёта."""
        with pytest.raises(error_type, match=error_message):
            get_mask_account(invalid_input)