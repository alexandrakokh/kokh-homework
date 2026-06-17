from unittest.mock import patch
from src.main import main, format_transaction


class TestFormatTransaction:
    """Тесты для функции format_transaction."""

    def test_format_transaction_normal_case_flat_data(self):
        """
        Классический случай: данные лежат на верхнем уровне.
        Номера карт передаются как чистые цифры (старый формат).
        """
        op = {
            "date": "2023-01-01T00:00:00",
            "description": "Покупка в магазине",
            "from": "1234567812345678",  # 16 цифр
            "to": "9876543298765432",  # 16 цифр
            "amount": 1000,
            "currency": {"name": "RUB"},
        }
        result = format_transaction(op)

        assert "01.01.2023" in result
        assert "Покупка в магазине" in result
        assert "Сумма: 1000 RUB" in result

        # Проверяем, что маска применилась (должны быть звездочки)
        assert "****" in result

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
        # from/to должны стать "Неизвестно"
        assert "Неизвестно -> Неизвестно" in result
        assert "Сумма: 0 Не указана" in result


class TestMainFunction:
    """Тесты для точки входа main()."""

    @patch("builtins.input")
    @patch("builtins.print")
    def test_main_success_json_sort(self, mock_print, mock_input):
        # Эмулируем ввод пользователя
        # 1: выбор файла, EXECUTED: статус, да: сортировка, по возрастанию, нет: другие вопросы
        mock_input.side_effect = ["1", "EXECUTED", "да", "по возрастанию", "нет", "нет"]

        sample_data = [
            {
                "date": "2023-01-01T00:00:00",
                "description": "Test Op",
                "from": "1111222233334444",
                "to": "5555666677778888",
                "amount": 100,
                "currency": {"name": "RUB"},
            }
        ]

        with patch("src.main.read_data", return_value=sample_data):
            main()

        # Программа должна что-то вывести (хотя бы одну транзакцию)
        assert mock_print.call_count > 0

    @patch("builtins.input")
    @patch("builtins.print")
    def test_main_invalid_file_choice(self, mock_print, mock_input):
        mock_input.side_effect = ["4"]  # Неверный выбор пункта меню
        main()
        expected_msg = "Программа: Неверный выбор пункта меню. Завершение работы."
        mock_print.assert_any_call(expected_msg)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_main_failed_data_loading(self, mock_print, mock_input):
        mock_input.side_effect = ["1"]  # Выбор файла
        # read_data возвращает None (ошибка загрузки)
        with patch("src.main.read_data", return_value=None):
            main()

        expected_msg = "Программа: Не удалось загрузить данные. Завершение работы."
        mock_print.assert_any_call(expected_msg)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_main_empty_result(self, mock_print, mock_input):
        # Увеличиваем запас ответов на случай изменений в меню
        mock_input.side_effect = ["1", "EXECUTED", "нет", "нет", "нет", "нет", "нет", "нет", "нет", "нет"]

        # Пустой список транзакций
        with patch("src.main.read_data", return_value=[]):
            main()

        expected_substring = "Не найдено ни одной транзакции"

        found = False
        for call_args in mock_print.call_args_list:
            # call_args[0] - это кортеж аргументов, [0] - первый аргумент (текст)
            text = call_args[0][0]
            if expected_substring in text:
                found = True
                break

        assert found, f"Сообщение не найдено. Вывод программы: {[c[0][0] for c in mock_print.call_args_list]}"

    @patch("builtins.input")
    @patch("builtins.print")
    def test_main_ruble_filter_enabled(self, mock_print, mock_input):
        # Ввод: 1 (файл), EXECUTED (статус), нет (сортировка), да (фильтр RUB), нет (остальное)
        mock_input.side_effect = ["1", "EXECUTED", "нет", "да", "нет"]

        sample_data = [
            {"currency": {"code": "RUB"}, "date": "2023-01-01"},
            {"currency": {"code": "USD"}, "date": "2023-01-02"},
        ]

        with patch("src.main.read_data", return_value=sample_data):
            main()

        mock_print.assert_any_call("Программа: Отфильтрованы только рублевые операции.")
