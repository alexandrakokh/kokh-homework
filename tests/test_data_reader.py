from unittest.mock import Mock, patch, mock_open
import json
import pytest
import pandas as pd
from tests.conftest import sample_transactions
from src.data_reader import (
    read_transactions_from_csv,
    read_transactions_from_excel,
    read_transactions_from_json
)


# Отключаем логирование для тестов
@pytest.fixture(autouse=True)
def disable_logging():
    import logging
    logging.disable(logging.CRITICAL)


# Тесты для CSV
@patch("src.data_reader.pd.read_csv")
def test_read_csv_success(mock_read_csv):
    mock_df = Mock()
    mock_df.to_dict.return_value = [
        {"id": 1, "amount": 100, "currency": "RUB"},
        {"id": 2, "amount": 200, "currency": "USD"}
    ]
    mock_read_csv.return_value = mock_df

    result = read_transactions_from_csv("test.csv")
    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(item, dict) for item in result)
    assert result[0]["id"] == 1
    assert result[1]["amount"] == 200


@patch("src.data_reader.pd.read_csv")
def test_read_csv_file_not_found(mock_read_csv):
    mock_read_csv.side_effect = FileNotFoundError
    result = read_transactions_from_csv("non_existent.csv")
    assert result == []


@patch("src.data_reader.pd.read_csv")
def test_read_csv_empty_file(mock_read_csv):
    mock_df = Mock()
    mock_df.to_dict.return_value = []
    mock_read_csv.return_value = mock_df
    result = read_transactions_from_csv("empty.csv")
    assert result == []


# Тесты для Excel
@patch("src.data_reader.pd.read_excel")
def test_read_excel_success(mock_read_excel):
    mock_df = Mock()
    mock_df.to_dict.return_value = [
        {"id": 3, "amount": 300, "currency": "EUR"},
        {"id": 4, "amount": 400, "currency": "GBP"}
    ]
    mock_read_excel.return_value = mock_df

    result = read_transactions_from_excel("test.xlsx")
    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(item, dict) for item in result)
    assert result[0]["id"] == 3
    assert result[1]["currency"] == "GBP"


@patch("src.data_reader.pd.read_excel")
def test_read_excel_file_not_found(mock_read_excel):
    mock_read_excel.side_effect = FileNotFoundError
    result = read_transactions_from_excel("non_existent.xlsx")
    assert result == []


def test_read_json_file_not_found():
    result = read_transactions_from_json("non_existent.json")
    assert result == []


def test_read_json_invalid_format():
    with patch("builtins.open", mock_open(read_data="{invalid_json}")):
        result = read_transactions_from_json("invalid.json")
        assert result == []

# Тесты на обработку ошибок
@patch("src.data_reader.pd.read_csv")
def test_read_csv_exception(mock_read_csv):
    mock_read_csv.side_effect = Exception("Test exception")
    result = read_transactions_from_csv("test.csv")
    assert result == []

@patch("src.data_reader.pd.read_excel")
def test_read_excel_exception(mock_read_excel):
    mock_read_excel.side_effect = Exception("Test exception")
    result = read_transactions_from_excel("test.xlsx")
    assert result == []

@patch("builtins.open")
def test_read_json_file_error(mock_open):
    mock_open.side_effect = IOError("File error")
    result = read_transactions_from_json("test.json")
    assert result == []

@patch("builtins.open")
def test_read_json_permission_error(mock_open):
    mock_open.side_effect = PermissionError("No permission")
    result = read_transactions_from_json("test.json")
    assert result == []

@patch("src.data_reader.pd.read_csv")
def test_csv_empty_result(mock_read_csv):
    mock_df = Mock()
    mock_df.to_dict.return_value = []
    mock_read_csv.return_value = mock_df
    result = read_transactions_from_csv("empty.csv")
    assert result == []

@patch("src.data_reader.pd.read_excel")
def test_excel_empty_result(mock_read_excel):
    mock_df = Mock()
    mock_df.to_dict.return_value = []
    mock_read_excel.return_value = mock_df
    result = read_transactions_from_excel("empty.xlsx")
    assert result == []

def test_json_empty_file(tmp_path):
    test_file = tmp_path / "empty.json"
    test_file.write_text("")
    result = read_transactions_from_json(str(test_file))
    assert result == []

def test_json_corrupted_file(tmp_path):
    test_file = tmp_path / "corrupted.json"
    test_file.write_text("{corrupted_data")
    result = read_transactions_from_json(str(test_file))
    assert result == []

@patch("src.data_reader.pd.read_csv")
def test_csv_invalid_data(mock_read_csv):
    mock_read_csv.side_effect = pd.errors.EmptyDataError
    result = read_transactions_from_csv("invalid.csv")
    assert result == []