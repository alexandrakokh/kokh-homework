from unittest.mock import Mock, patch

import pytest

from src.data_reader import read_transactions_from_csv, read_transactions_from_excel


@patch("src.data_reader.pd.read_csv")
def test_read_csv_success(mock_read_csv):
    """
    Проверяет успешное чтение CSV через Mock.
    Теперь патч сработает, потому что в data_reader.py убрали проверку os.path.exists.
    """
    # 1. Создаем мок-объект DataFrame
    mock_df = Mock()

    mock_df.to_dict.return_value = [{"id": 1, "amount": 100, "currency": "RUB"}]

    # 3. Подменяем результат вызова pd.read_csv на наш мок-DataFrame
    mock_read_csv.return_value = mock_df

    # 4. Вызываем функцию
    result = read_transactions_from_csv("test.csv")

    # 5. Проверки
    assert isinstance(result, list), "Функция должна возвращать список"
    assert len(result) == 1, "Должна быть ровно 1 запись"
    assert isinstance(result[0], dict), "Элемент списка должен быть словарем"
    assert result[0]["id"] == 1
    assert result[0]["amount"] == 100


@patch("src.data_reader.pd.read_excel")
def test_read_excel_success(mock_read_excel):
    """
    Проверяет успешное чтение Excel через мок.
    """
    mock_df = Mock()
    # Эмуляция to_dict(orient='records') для Excel
    mock_df.to_dict.return_value = [{"id": 2, "amount": 200, "currency": "USD"}]
    mock_read_excel.return_value = mock_df

    result = read_transactions_from_excel("test.xlsx")

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["id"] == 2


def test_read_csv_real_data():
    """
    Проверяет чтение реального файла.
    Убедитесь, что файл tests/data/transactions.csv существует!
    """
    csv_path = "tests/data/transactions.csv"

    try:
        result = read_transactions_from_csv(csv_path)

        # Функция возвращает список всех транзакций.
        assert isinstance(result, list), "Реальный файл должен возвращать список записей"
        assert len(result) > 0, "Список не должен быть пустым (файл должен содержать данные)"
        assert isinstance(result[0], dict), "Первая запись должна быть словарем"

    except FileNotFoundError:
        # Если файла нет, тест упадет с понятной ошибкой, а не с AssertionError
        pytest.fail(f"Файл не найден: {csv_path}. Пожалуйста, создайте тестовые данные в папке tests/data")


@patch("src.data_reader.pd.read_csv")
def test_read_csv_file_not_found(mock_read_csv):
    """Проверяет, что функция корректно обрабатывает отсутствие файла и возвращает пустой список."""
    # Имитируем выброс исключения FileNotFoundError при вызове read_csv
    mock_read_csv.side_effect = FileNotFoundError("Файл удален")

    result = read_transactions_from_csv("non_existent.csv")

    assert result == []
