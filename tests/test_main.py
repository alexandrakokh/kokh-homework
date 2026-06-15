from unittest.mock import patch
import pytest
from src.main import main, format_transaction


def test_format_transaction_normal_case():
    op = {
        "date": "2023-01-01T00:00:00",
        "description": "Покупка в магазине",
        "from": "1234567812345678",  # 16 цифр!
        "to": "9876543298765432",  # 16 цифр!
        "amount": 1000,
        "currency": {"name": "RUB"}
    }
    result = format_transaction(op)
    assert "01.01.2023" in result
    assert "Покупка в магазине" in result
    assert "Сумма: 1000 RUB" in result


def test_format_transaction_invalid_date():
    """Дата неверная, но номера карт валидные (чтобы mask не упал)"""
    op = {
        "date": "invalid-date",
        "description": "Тест",
        "from": "1111222233334444",  # 16 цифр
        "to": "5555666677778888",  # 16 цифр
        "amount": 500,
        "currency": {"name": "RUB"}
    }
    result = format_transaction(op)
    assert "Неизвестная дата" in result
    assert "RUB" in result


def test_format_transaction_missing_fields():
    op = {
        "date": "2023-01-01T00:00:00",
        "description": "Тест",
        "amount": 100
        # from, to, currency отсутствуют
    }
    result = format_transaction(op)
    assert "Неизвестно" in result  # для from и to
    assert "RUB" in result  # дефолт


@patch('builtins.input')
@patch('builtins.print')
def test_main_success_json_sort(mock_print, mock_input):
    mock_input.side_effect = ["1", "EXECUTED", "да", "по возрастанию", "нет", "нет"]
    with patch('src.main.read_data', return_value=[{"date": "2023-01-01", "description": "Test"}]):
        main()
    assert mock_print.call_count > 0


@patch('builtins.input')
@patch('builtins.print')
def test_main_invalid_file_choice(mock_print, mock_input):
    mock_input.side_effect = ["4"]
    main()
    expected_msg = "Программа: Неверный выбор пункта меню. Завершение работы."
    mock_print.assert_any_call(expected_msg)


@patch('builtins.input')
@patch('builtins.print')
def test_main_failed_data_loading(mock_print, mock_input):
    mock_input.side_effect = ["1"]
    with patch('src.main.read_data', return_value=None):
        main()
    expected_msg = "Программа: Не удалось загрузить данные. Завершение работы."
    mock_print.assert_any_call(expected_msg)


@patch('builtins.input')
@patch('builtins.print')
def test_main_empty_result(mock_print, mock_input):
    # ВАЖНО: Добавь много "нет", чтобы покрыть любые лишние вопросы в коде
    # Если в коде 7 вопросов, а тут 5 - будет висеть. Сделай 10 штук "нет".
    mock_input.side_effect = [
        "1",  # Выбор файла
        "EXECUTED",  # Статус
        "нет",  # Сортировка
        "нет",  # Рубли
        "нет",  # Поиск
        "нет", "нет", "нет", "нет", "нет"  # ЗАПАСНЫЕ ОТВЕТЫ НА СЛУЧАЙ ЛИШНИХ ВОПРОСОВ
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

    assert found, f"Сообщение не найдено. Вывод программы: {[c[0][0] for c in mock_print.call_args_list]}"


@patch('builtins.input')
@patch('builtins.print')
def test_main_ruble_filter_enabled(mock_print, mock_input):
    mock_input.side_effect = ["1", "EXECUTED", "нет", "да", "нет"]
    sample_data = [
        {"currency": {"code": "RUB"}, "date": "2023-01-01"},
        {"currency": {"code": "USD"}, "date": "2023-01-02"}
    ]
    with patch('src.main.read_data', return_value=sample_data):
        main()

    mock_print.assert_any_call("Программа: Отфильтрованы только рублевые операции.")

