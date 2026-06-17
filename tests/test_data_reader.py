from unittest.mock import Mock, patch
import pytest
import pandas as pd
from src.data_reader import (
    read_transactions_from_csv,
    read_transactions_from_excel,
    read_transactions_from_json
)


# Отключаем логирование для чистоты вывода тестов
@pytest.fixture(autouse=True)
def disable_logging():
    import logging
    logging.disable(logging.CRITICAL)


# --- Тесты для CSV ---

@patch("src.data_reader.pd.read_csv")
def test_read_csv_success(mock_read_csv):
    """
    Проверяет успешное чтение CSV.
    Исправление: Настраиваем mock так, чтобы dropna и fillna возвращали сам объект,
    чтобы цепочка вызовов в коде не теряла данные.
    """
    mock_df = Mock()

    expected_data = [
        {"id": 1, "amount": 100, "currency": "RUB"},
        {"id": 2, "amount": 200, "currency": "USD"}
    ]

    # 1. Настраиваем to_dict, чтобы он отдавал наши данные
    mock_df.to_dict.return_value = expected_data

    # 2.Говорим моку, что dropna и fillna ничего не меняют, а просто возвращают себя
    mock_df.dropna.return_value = mock_df
    mock_df.fillna.return_value = mock_df

    # 3. Настраиваем read_csv, чтобы он возвращал наш подготовленный df
    mock_read_csv.return_value = mock_df

    # 4. Вызываем функцию
    result = read_transactions_from_csv("test.csv")

    # 5. Проверки
    assert isinstance(result, list)
    assert len(result) == 2
    assert result == expected_data


@patch("src.data_reader.pd.read_csv")
def test_read_csv_file_not_found(mock_read_csv):
    """Проверяет обработку FileNotFoundError"""
    mock_read_csv.side_effect = FileNotFoundError
    result = read_transactions_from_csv("non_existent.csv")
    assert result == []


@patch("src.data_reader.pd.read_csv")
def test_read_csv_empty_file(mock_read_csv):
    """Проверяет чтение файла, где нет данных (пустой список)"""
    mock_df = Mock()
    mock_df.to_dict.return_value = []
    mock_read_csv.return_value = mock_df

    result = read_transactions_from_csv("empty.csv")
    assert result == []


@patch("src.data_reader.pd.read_csv")
def test_read_csv_exception_handling(mock_read_csv):
    """Проверяет обработку любых других исключений"""
    mock_read_csv.side_effect = Exception("Critical Error")
    result = read_transactions_from_csv("broken.csv")
    assert result == []


@patch("src.data_reader.pd.read_csv")
def test_csv_invalid_data_error(mock_read_csv):
    """Проверяет обработку специфичной ошибки pandas EmptyDataError"""
    mock_read_csv.side_effect = pd.errors.EmptyDataError
    result = read_transactions_from_csv("invalid.csv")
    assert result == []


# --- Тесты для Excel ---

@patch("src.data_reader.pd.read_excel")
def test_read_excel_success(mock_read_excel):
    mock_df = Mock()
    expected_data = [
        {"id": 3, "amount": 300, "currency": "EUR"},
        {"id": 4, "amount": 400, "currency": "GBP"}
    ]
    mock_df.to_dict.return_value = expected_data
    mock_read_excel.return_value = mock_df

    result = read_transactions_from_excel("test.xlsx")

    assert isinstance(result, list)
    assert len(result) == 2
    assert result == expected_data


@patch("src.data_reader.pd.read_excel")
def test_read_excel_file_not_found(mock_read_excel):
    mock_read_excel.side_effect = FileNotFoundError
    result = read_transactions_from_excel("non_existent.xlsx")
    assert result == []


@patch("src.data_reader.pd.read_excel")
def test_read_excel_exception_handling(mock_read_excel):
    mock_read_excel.side_effect = Exception("Excel Error")
    result = read_transactions_from_excel("broken.xlsx")
    assert result == []


# --- Тесты для JSON ---

def test_read_json_file_not_found():
    """Проверка отсутствия файла"""
    result = read_transactions_from_json("non_existent.json")
    assert result == []


def test_read_json_invalid_format():
    """Проверка невалидного JSON содержимого"""
    from unittest.mock import mock_open
    with patch("builtins.open", mock_open(read_data="{invalid_json}")):
        result = read_transactions_from_json("invalid.json")
        assert result == []


def test_read_json_file_error():
    """Проверка ошибки открытия файла (IOError)"""
    from unittest.mock import patch
    with patch("builtins.open") as mock_open:
        mock_open.side_effect = IOError("File error")
        result = read_transactions_from_json("test.json")
        assert result == []


def test_read_json_permission_error():
    """Проверка ошибки прав доступа"""
    from unittest.mock import patch
    with patch("builtins.open") as mock_open:
        mock_open.side_effect = PermissionError("No permission")
        result = read_transactions_from_json("test.json")
        assert result == []


def test_json_empty_file(tmp_path):
    """Проверка пустого JSON файла"""
    test_file = tmp_path / "empty.json"
    test_file.write_text("")
    result = read_transactions_from_json(str(test_file))
    assert result == []


def test_json_corrupted_file(tmp_path):
    """Проверка битого JSON файла"""
    test_file = tmp_path / "corrupted.json"
    test_file.write_text("{corrupted_data")
    result = read_transactions_from_json(str(test_file))
    assert result == []
