from unittest.mock import patch
import pytest
from src.main import main, format_transaction


class TestFormatTransaction:
    """Тесты для функции format_transaction с учетом новой логики маскирования."""

    def test_format_transaction_normal_case_flat_data(self):
        """
        Классический случай: данные лежат на верхнем уровне.
        Номера карт передаются как чистые цифры (старый формат),
        новая функция mask_account_card должна это корректно обработать.
        """
        op = {
            "date": "2023-01-01T00:00:00",
            "description": "Покупка в магазине",
            "from": "1234567812345678",  # 16 цифр
            "to": "9876543298765432",  # 16 цифр
            "amount": 1000,
            "currency": {"name": "RUB"}
        }
        result = format_transaction(op)

        assert "01.01.2023" in result
        assert "Покупка в магазине" in result
        assert "Сумма: 1000 RUB" in result
        # Проверка маскирования (формат зависит от логики get_mask_card_number)
        assert "****" in result

    def test_format_transaction_nested_data_operation_amount(self):
        """
        Случай: данные о счетах и суммах лежат внутри operationAmount.
        Это самый важный тест после рефакторинга.
        """
        op = {
            "date": "2023-05-20T14:30:00",
            "description": "Перевод другу",
            # Поля from/to отсутствуют на верхнем уровне
            "operationAmount": {
                "from": "Visa 4000123456789012",  # Строка с названием и номером
                "to": "Счет 40702810000000000000",  # Строка с названием и номером
                "amount": 5000,
                "currency": {"name": "RUB"}
            }
        }
        result = format_transaction(op)

        assert "20.05.2023" in result
        assert "Перевод другу" in result
        assert "Сумма: 5000 RUB" in result

        # Проверяем, что универсальная маска сработала:
        # 1. Она распознала "Visa" и применила маску карты.
        assert "Visa" in result
        assert "****" in result  # Звездочки должны быть

        # 2. Она распознала "Счет" и применила маску счета (**0000)
        assert "Счет" in result
        assert "**0000" in result or "**0000" in result  # Маска счета

    def test_format_transaction_invalid_date_and_mixed_inputs(self):
        """Дата неверная, входные данные смешанные (строки с текстом)."""
        op = {
            "date": "invalid-date",
            "description": "Тест смешанных данных",
            "operationAmount": {
                "from": "Mastercard 5100123412341234",
                "to": "Account 11112222333344445555",
                "amount": 250.50,
                "currency": "EUR"  # Валюта может быть строкой
            }
        }
        result = format_transaction(op)

        assert "Неизвестная дата" in result
        assert "Тест смешанных данных" in result
        assert "Сумма: 250.5 EUR" in result
        assert "Mastercard" in result
        assert "Account" in result

    def test_format_transaction_missing_fields_fallback(self):
        """Проверка обработки отсутствующих полей и значений по умолчанию."""
        op = {
            "date": "2023-10-10T10:10:10",
            "description": "Тест отсутствия данных",
            # from, to, amount, currency отсутствуют полностью
        }
        result = format_transaction(op)

        assert "10.10.2023" in result
        assert "Тест отсутствия данных" in result
        assert "Неизвестно" in result  # Для from и to
        assert "Сумма: 0 RUB" in result  # amount=0, currency=RUB по дефолту

    def test_format_transaction_none_values_handling(self):
        """Явная передача None в поля."""
        op = {
            "date": None,
            "description": None,
            "from": None,
            "to": None,
            "amount": None,
            "currency": None
        }
        result = format_transaction(op)

        assert "Неизвестная дата" in result
        assert "Без описания" in result  # Дефолт для description
        assert "Неизвестно" in result  # Для счетов
        assert "Сумма: 0 RUB" in result


class TestMainFunction:
    """Тесты для точки входа main(). Логика маскирования здесь тестируется косвенно."""

    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_success_json_sort(self, mock_print, mock_input):
        # Эмулируем ввод пользователя
        mock_input.side_effect = ["1", "EXECUTED", "да", "по возрастанию", "нет", "нет"]

        # Возвращаем данные, которые точно пройдут через format_transaction
        sample_data = [
            {
                "date": "2023-01-01T00:00:00",
                "description": "Test Op",
                "from": "1111222233334444",
                "to": "5555666677778888",
                "amount": 100,
                "currency": {"name": "RUB"}
            }
        ]

        with patch('src.main.read_data', return_value=sample_data):
            main()

        assert mock_print.call_count > 0

    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_invalid_file_choice(self, mock_print, mock_input):
        mock_input.side_effect = ["4"]  # Неверный выбор пункта меню
        main()
        expected_msg = "Программа: Неверный выбор пункта меню. Завершение работы."
        mock_print.assert_any_call(expected_msg)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_failed_data_loading(self, mock_print, mock_input):
        mock_input.side_effect = ["1"]  # Выбор файла
        with patch('src.main.read_data', return_value=None):
            main()
        expected_msg = "Программа: Не удалось загрузить данные. Завершение работы."
        mock_print.assert_any_call(expected_msg)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_empty_result(self, mock_print, mock_input):
        # Увеличиваем запас ответов на случай изменений в меню
        mock_input.side_effect = [
            "1", "EXECUTED", "нет", "нет", "нет",
            "нет", "нет", "нет", "нет", "нет"
        ]

        with patch('src.main.read_data', return_value=[]):
            main()

        expected_substring = "Не найдено ни одной транзакции"

        found = False
        for call_args in mock_print.call_args_list:
            text = call_args[0][0]
            if expected_substring in text:
                found = True
                break

        assert found, f"Сообщение не найдено. Вывод программы: {[c[0][0] for c in mock_print.call_print_args_list]}"

    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_ruble_filter_enabled(self, mock_print, mock_input):
        mock_input.side_effect = ["1", "EXECUTED", "нет", "да", "нет"]
        sample_data = [
            {"currency": {"code": "RUB"}, "date": "2023-01-01"},
            {"currency": {"code": "USD"}, "date": "2023-01-02"}
        ]
        with patch('src.main.read_data', return_value=sample_data):
            main()

        mock_print.assert_any_call("Программа: Отфильтрованы только рублевые операции.")
