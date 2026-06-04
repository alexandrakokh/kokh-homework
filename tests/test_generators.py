import pytest
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator


#Фикстура с тестовыми данными транзакций
@pytest.fixture
def sample_transactions():
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160"
        }
    ]

# Фикстура для транзакций без описания
@pytest.fixture
def transactions_with_missing_description():
    return [
        {"id": 1, "description": "Первая транзакция"},
        {"id": 2},  # Нет поля description
        {"id": 3, "description": "Третья транзакция"}
    ]



# Тесты для filter_by_currency
class TestFilterByCurrency:

    def test_filter_usd_transactions(self, sample_transactions):
        """Тест фильтрации транзакций в USD."""
        usd_transactions = list(filter_by_currency(sample_transactions, "USD"))
        assert len(usd_transactions) == 2
        assert all(t["operationAmount"]["currency"]["code"] == "USD" for t in usd_transactions)

    def test_filter_rub_transactions(self, sample_transactions):
        """Тест фильтрации транзакций в RUB."""
        rub_transactions = list(filter_by_currency(sample_transactions, "RUB"))
        assert len(rub_transactions) == 1
        assert rub_transactions[0]["operationAmount"]["currency"]["code"] == "RUB"

    @pytest.mark.parametrize("currency_code,expected_count", [
        ("EUR", 0),
        ("JPY", 0)
    ])
    def test_no_transactions_for_currency(self, sample_transactions, currency_code, expected_count):
        """Тест отсутствия транзакций для заданной валюты."""
        transactions = list(filter_by_currency(sample_transactions, currency_code))
        assert len(transactions) == expected_count

    def test_empty_transactions_list(self):
        """Тест с пустым списком транзакций."""
        result = list(filter_by_currency([], "USD"))
        assert result == []

    def test_transactions_without_operation_amount(self):
        """Тест обработки транзакций без поля operationAmount."""
        incomplete_transactions = [
            {"id": 1},
            {"id": 2, "operationAmount": {}},
            {"id": 3, "operationAmount": {"currency": {}}}
        ]
        result = list(filter_by_currency(incomplete_transactions, "USD"))
        assert result == []

    def test_none_transactions(self):
        """Тест обработки None вместо списка транзакций."""
        result = list(filter_by_currency(None, "USD"))
        assert result == []



# Тесты для transaction_descriptions
class TestTransactionDescriptions:

    def test_get_all_descriptions(self, sample_transactions):
        """Тест получения всех описаний транзакций."""
        descriptions = list(transaction_descriptions(sample_transactions))
        expected = ["Перевод организации", "Перевод со счета на счет", "Перевод со счета на счет"]
        assert descriptions == expected

    def test_with_missing_descriptions(self, transactions_with_missing_description):
        """Тест обработки транзакций без поля description."""
        descriptions = list(transaction_descriptions(transactions_with_missing_description))
        expected = ["Первая транзакция", "", "Третья транзакция"]
        assert descriptions == expected

    def test_empty_transactions_list(self):
        """Тест с пустым списком транзакций."""
        result = list(transaction_descriptions([]))
        assert result == []

    def test_none_transactions(self):
        """Тест обработки None вместо списка транзакций."""
        result = list(transaction_descriptions(None))
        assert result == []


    def test_single_transaction(self):
        """Тест с одной транзакцией."""
        single_transaction = [{"id": 1, "description": "Одиночная транзакция"}]
        result = list(transaction_descriptions(single_transaction))
        assert result == ["Одиночная транзакция"]



# Тесты для card_number_generator
class TestCardNumberGenerator:

    def test_basic_range(self):
        """Тест генерации базового диапазона номеров карт."""
        cards = list(card_number_generator(1, 3))
        expected = [
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
            "0000 0000 0000 0003"
        ]
        assert cards == expected

    def test_formatting_correctness(self):
        """Тест корректности форматирования номеров карт."""
        card = next(card_number_generator(1234567890123456, 1234567890123456))
        assert card == "1234 5678 9012 3456"

    def test_edge_values(self):
        """Тест крайних значений диапазона."""
        # Минимальное значение
        min_card = next(card_number_generator(1, 1))
        assert min_card == "0000 0000 0000 0001"

        # Максимальное значение
        max_card = next(card_number_generator(9999999999999999, 9999999999999999))
        assert max_card == "9999 9999 9999 9999"

    def test_single_card(self):
        """Тест генерации одного номера карты."""
        cards = list(card_number_generator(42, 42))
        assert cards == ["0000 0000 0000 0042"]

    def test_large_range(self):
        """Тест большого диапазона (проверка производительности и корректности)."""
        cards = list(card_number_generator(9999999999999990, 9999999999999995))
        expected = [
            "9999 9999 9999 9990",
            "9999 9999 9999 9991",
            "9999 9999 9999 9992",
            "9999 9999 9999 9993",
            "9999 9999 9999 9994",
            "9999 9999 9999 9995"
        ]
        assert cards == expected

    def test_generator_iteration(self):
        """Тест итерации по генератору без преобразования в список."""
        generator = card_number_generator(100, 102)
        cards = []
        for card in generator:
            cards.append(card)
        expected = ["0000 0000 0000 0100", "0000 0000 0000 0101", "0000 0000 0000 0102"]
        assert cards == expected


# Тесты на проверку исключений для card_number_generator
class TestCardNumberGeneratorExceptions:

    @pytest.mark.parametrize("start,end,expected_exception,expected_message", [
        (0, 5, ValueError, "Начальное значение должно быть не меньше 1"),
        (1, 10000000000000000, ValueError, "Конечное значение не может превышать 9999999999999999"),
        (5, 1, ValueError, "Начальное значение не может быть больше конечного"),
        ("1", 5, TypeError, "Начальное и конечное значения должны быть целыми числами"),
        (1, "5", TypeError, "Начальное и конечное значения должны быть целыми числами")
    ])
    def test_invalid_parameters(self, start, end, expected_exception, expected_message):
        """Тест обработки некорректных параметров."""
        with pytest.raises(expected_exception) as exc_info:
            list(card_number_generator(start, end))
        assert str(exc_info.value) == expected_message

    def test_negative_values(self):
        """Тест отрицательных значений."""
        with pytest.raises(ValueError) as exc_info:
            list(card_number_generator(-5, 5))
        assert "Начальное значение должно быть не меньше 1" in str(exc_info.value)


# Дополнительные тесты для edge-случаев
class TestEdgeCases:

    def test_filter_with_nested_missing_fields(self):
        """Тест фильтрации с неполными вложенными структурами."""
        incomplete_transactions = [
            {"id": 1, "operationAmount": {}},
            {"id": 2, "operationAmount": {"currency": {}}},
            {"id": 3, "operationAmount": {"currency": {"code": "USD"}}},
            {"id": 4, "operationAmount": {"currency": {"code": "RUB"}}}
        ]
        usd_transactions = list(filter_by_currency(incomplete_transactions, "USD"))
        assert len(usd_transactions) == 1
        assert usd_transactions[0]["id"] == 3

    def test_transaction_descriptions_with_complex_data(self):
        """Тест описаний со сложными структурами данных."""
        complex_transactions = [
            {"id": 1, "description": "Транзакция 1"},
            {"id": 2, "description": ""},  # Пустое описание
            {"id": 3},  # Нет описания
            {"id": 4, "description": "Транзакция 4"}
        ]
        descriptions = list(transaction_descriptions(complex_transactions))
        expected = ["Транзакция 1", "", "", "Транзакция 4"]
        assert descriptions == expected

    def test_card_generator_with_boundary_values(self):
        """Тест граничных значений для генератора карт."""
        # Минимально возможное значение
        min_card = next(card_number_generator(1, 1))
        assert min_card == "0000 0000 0000 0001"

        # Максимально возможное значение
        max_card = next(card_number_generator(9999999999999999, 9999999999999999))
        assert max_card == "9999 9999 9999 9999"

        # Значение с ведущими нулями в середине диапазона
        mid_card = next(card_number_generator(123, 123))
        assert mid_card == "0000 0000 0000 0123"