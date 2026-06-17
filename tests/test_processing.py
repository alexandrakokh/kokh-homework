import pytest
from src.processing import process_bank_operations, filter_by_state, sort_by_date


class TestFilterByState:
    def test_filter_executed_transactions(self, sample_transactions):
        """Тестирование фильтрации по статусу EXECUTED."""
        filtered = filter_by_state(sample_transactions, "EXECUTED")
        assert len(filtered) == 2
        for transaction in filtered:
            assert transaction["state"] == "EXECUTED"

    def test_filter_canceled_transactions(self, sample_transactions):
        """Тестирование фильтрации по статусу CANCELED."""
        filtered = filter_by_state(sample_transactions, "CANCELED")
        assert len(filtered) == 2
        for transaction in filtered:
            assert transaction["state"] == "CANCELED"

    def test_filter_nonexistent_state(self, sample_transactions):
        """Тестирование фильтрации по несуществующему статусу."""
        filtered = filter_by_state(sample_transactions, "PENDING")
        assert len(filtered) == 0

    @pytest.mark.parametrize("state", ["EXECUTED", "CANCELED", "PENDING"])
    def test_parametrized_filtering(self, sample_transactions, state):
        """Параметризованные тесты для различных статусов."""
        filtered = filter_by_state(sample_transactions, state)
        if state in ["EXECUTED", "CANCELED"]:
            assert len(filtered) > 0
        else:
            assert len(filtered) == 0


class TestSortByDate:
    def test_sort_descending(self, sample_transactions):
        """Тестирование сортировки по дате в порядке убывания."""
        sorted_transactions = sort_by_date(sample_transactions, reverse=True)
        dates = [t["date"] for t in sorted_transactions]
        # Проверяем, что список отсортирован правильно
        assert dates == sorted(dates, reverse=True)

    def test_sort_ascending(self, sample_transactions):
        """Тестирование сортировки по дате в порядке возрастания."""
        sorted_transactions = sort_by_date(sample_transactions, reverse=False)
        dates = [t["date"] for t in sorted_transactions]
        assert dates == sorted(dates)

    def test_sort_with_duplicate_dates(self):
        """Тестирование сортировки при одинаковых датах (стабильность)."""
        transactions_with_duplicates = [
            {"id": 1, "date": "2024-01-01T10:00:00"},
            {"id": 2, "date": "2024-01-01T10:00:00"},
            {"id": 3, "date": "2024-01-02T11:00:00"},
        ]
        sorted_transactions = sort_by_date(transactions_with_duplicates)
        # При одинаковых датах порядок должен сохраняться (стабильная сортировка)
        expected_order = [1, 2, 3]
        actual_order = [t["id"] for t in sorted_transactions]
        assert actual_order == expected_order

    def test_sort_with_invalid_dates(self):
        """Тестирование обработки некорректных дат (должно выбрасывать ValueError)."""
        transactions_with_invalid = [
            {"id": 1, "date": "invalid-date-format"},
            {"id": 2, "date": "2024-01-01T10:00:00"},
        ]
        with pytest.raises(ValueError):
            sort_by_date(transactions_with_invalid)

    def test_empty_list_sorting(self):
        """Тестирование сортировки пустого списка."""
        result = sort_by_date([])
        assert result == []


class TestCategoryCounting:
    def test_count_categories_basic(self):
        """Базовый тест: подсчет разных категорий."""
        transactions = [
            {"description": "Покупка продуктов в магазине"},
            {"description": "Оплата бензина на АЗС"},
            {"description": "Перевод другу"},
            {"description": "Еще одна покупка продуктов"},
        ]
        categories = ["продукты", "бензин", "переводы"]

        result = process_bank_operations(transactions, categories)

        assert result["продукты"] == 2
        assert result["бензин"] == 1
        assert result["переводы"] == 1

    def test_count_categories_case_insensitive(self):
        """Тест: регистр не важен."""
        transactions = [{"description": "ПОКУПКА ПРОДУКТОВ"}, {"description": "оплата Бензина"}]
        categories = ["Продукты", "Бензин"]

        result = process_bank_operations(transactions, categories)

        assert result["Продукты"] == 1
        assert result["Бензин"] == 1

    def test_count_categories_missing_category(self):
        """Тест: если категория не найдена, возвращается 0."""
        transactions = [{"description": "Покупка еды"}]
        categories = ["еда", "одежда"]  # 'одежда' не встретится

        result = process_bank_operations(transactions, categories)

        assert result["еда"] == 1
        assert result["одежда"] == 0

    def test_count_categories_empty_list(self):
        """Тест: пустой список транзакций."""
        transactions = []
        categories = ["продукты", "бензин"]

        result = process_bank_operations(transactions, categories)

        assert result == {"продукты": 0, "бензин": 0}
