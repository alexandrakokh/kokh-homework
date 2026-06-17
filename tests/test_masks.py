# tests/test_masks.py

import pytest
import re
from src.masks import get_mask_account, get_mask_card_number, mask_account_card


class TestGetMaskCardNumber:
    @pytest.mark.parametrize(
        "card_input,expected",
        [
            ("1234567890123456", "123456****3456"),
            ("0000000000000000", "000000****0000"),
            ("9999888877776666", "999988****6666"),
            ("1111222233334444", "111122****4444"),
        ],
    )
    def test_valid_card_masking(self, card_input, expected):
        """Тестирование корректного маскирования номера карты (ровно 16 цифр)."""
        result = get_mask_card_number(card_input)
        assert result == expected

    @pytest.mark.parametrize(
        "invalid_input,error_type,error_message",
        [
            ("", ValueError, "Номер карты должен быть непустой строкой"),
            (None, ValueError, "Номер карты должен быть непустой строкой"),
            ("123456789012345", ValueError, "Номер карты должен содержать ровно 16 цифр"),
            ("12345678901234567", ValueError, "Номер карты должен содержать ровно 16 цифр"),
            ("1234abcd5678efgh", ValueError, "Номер карты должен содержать только цифры"),
        ],
    )
    def test_invalid_card_inputs_raises_correct_error(self, invalid_input, error_type, error_message):
        with pytest.raises(error_type, match=error_message):
            get_mask_card_number(invalid_input)


class TestGetMaskAccount:
    @pytest.mark.parametrize(
        "account_input,expected",
        [
            ("73654108430135874305", "**4305"),
            ("1234", "**1234"),
            ("0000", "**0000"),
            ("123456789", "**6789"),
        ],
    )
    def test_valid_account_masking(self, account_input, expected):
        result = get_mask_account(account_input)
        assert result == expected

    @pytest.mark.parametrize(
        "invalid_input,error_type,error_message",
        [
            ("", ValueError, "Номер счёта должен быть непустой строкой"),
            ("123a", ValueError, "Номер счёта должен содержать только цифры"),
            (None, ValueError, "Номер счёта должен быть непустой строкой"),
        ],
    )
    def test_invalid_account_inputs_raises_correct_error(self, invalid_input, error_type, error_message):
        with pytest.raises(error_type, match=error_message):
            get_mask_account(invalid_input)


class TestMaskAccountCard:
    @pytest.mark.parametrize(
        "input_string,expected_prefix,expected_suffix_pattern",
        [
            ("Visa 4000123456789012", "Visa", r"400012\*\*\*\*9012"),
            ("Mastercard 5100123412341234", "Mastercard", r"510012\*\*\*\*1234"),
            ("4000123456789012", "", r"400012\*\*\*\*9012"),
            ("Счет 40702810000000000000", "Счет", r"\*\*0000"),
            ("Account 12345678901234567890", "Account", r"\*\*7890"),
            ("счёт 11112222333344445555", "счёт", r"\*\*5555"),
            ("ACC 98765432109876543210", "ACC", r"\*\*3210"),
        ],
    )
    def test_successful_parsing_and_masking(self, input_string, expected_prefix, expected_suffix_pattern):
        """Тест успешного парсинга строки и применения маски."""
        result = mask_account_card(input_string)

        if expected_prefix:
            assert result.startswith(f"{expected_prefix} "), f"Префикс не найден в результате: {result}"
        else:
            assert not result.startswith(" "), f"Лишний пробел в начале: {result}"

        match = re.search(expected_suffix_pattern, result)
        assert (
            match
        ), f"Неверный результат маскирования. Ожидался паттерн {expected_suffix_pattern}, получено: {result}"

    def test_empty_or_none_input(self):
        """Проверка обработки пустых значений и None."""
        assert mask_account_card("") == "Неизвестно"
        assert mask_account_card(None) == "Неизвестно"
        assert mask_account_card("   ") == "Неизвестно"

    def test_no_digits_found(self):
        """Если в строке нет цифр, функция должна вернуть исходную строку."""
        input_str = "Только текст, нет номера карты или счета"
        result = mask_account_card(input_str)
        assert result == input_str

    def test_card_length_error_handling(self):
        """Если формат номера неверен (не 16 цифр для карты), возвращается исходная строка."""
        invalid_card = "Visa 1234567890123"  # 15 цифр
        result = mask_account_card(invalid_card)
        assert result == invalid_card

        invalid_account = "Счет 123"  # Слишком короткий счет
        result_acc = mask_account_card(invalid_account)
        assert result_acc == invalid_account

    def test_mixed_format_with_spaces(self):
        """Обработка номера карты с пробелами внутри."""
        input_str = "Card 4000 1234 5678 9012"
        result = mask_account_card(input_str)

        assert "****" in result
        assert "400012" in result  # Первые 6 цифр (4000 + 12)
        assert "9012" in result  # Последние 4 цифры
        assert result.startswith("Card "), "Префикс 'Card' должен сохраниться"
        # Убедимся, что пробелы внутри номера исчезли в маске
        assert " " not in result.split()[1], "В замаскированной части не должно быть пробелов"
