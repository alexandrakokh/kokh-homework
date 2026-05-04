import pytest
from src.processing import filter_by_state, sort_by_date


class TestFilterByState:
    def test_filter_executed_transactions(self, sample_transactions):
        """Тестирование фильтрации по статусу EXECUTED."""
        filtered = filter_by_state(sample_transactions, 'EXECUTED')
        assert len(filtered) == 2
        for transaction in filtered:
            assert transaction['state'] == 'EXECUTED'


    def test_filter_canceled_transactions(self, sample_transactions):
        """Тестирование фильтрации по статусу CANCELED."""
        filtered = filter_by_state(sample_transactions, 'CANCELED')
        assert len(filtered) == 2
        for transaction in filtered:
            assert transaction['state'] == 'CANCELED'


    def test_filter_nonexistent_state(self, sample_transactions):
        """Тестирование фильтрации по несуществующему статусу."""
        filtered = filter_by_state(sample_transactions, 'PENDING')
        assert len(filtered) == 0


    @pytest.mark.parametrize("state", ['EXECUTED', 'CANCELED', 'PENDING'])
    def test_parametrized_filtering(self, sample_transactions, state):
        """Параметризованные тесты для различных статусов."""
        filtered = filter_by_state(sample_transactions, state)
        if state in ['EXECUTED', 'CANCELED']:
            assert len(filtered) > 0
        else:
            assert len(filtered) == 0


class TestSortByDate:
    def test_sort_descending(self, sample_transactions):
        """Тестирование сортировки по дате в порядке убывания."""
        sorted_transactions = sort_by_date(sample_transactions, reverse=True)
        dates = [t['date'] for t in sorted_transactions]
        assert dates == sorted(dates, reverse=True)


    def test_sort_ascending(self, sample_transactions):
        """Тестирование сортировки по дате в порядке возрастания."""
        sorted_transactions = sort_by_date(sample_transactions, reverse=False)
        dates = [t['date'] for t in sorted_transactions]
        assert dates == sorted(dates)


    def test_sort_with_duplicate_dates(self):
        """Тестирование сортировки при одинаковых датах."""
        transactions_with_duplicates = [
            {'id': 1, 'date': '2024-01-01T10:00:00'},
            {'id': 2, 'date': '2024-01-01T10:00:00'},
            {'id': 3, 'date': '2024-01-02T11:00:00'}
        ]
        sorted_transactions = sort_by_date(transactions_with_duplicates)
        expected_order = [1, 2, 3]  # ID в порядке появления при одинаковых датах
        actual_order = [t['id'] for t in sorted_transactions]
        assert actual_order == expected_order


    def test_sort_with_invalid_dates(self):
        """Тестирование обработки некорректных дат."""
        transactions_with_invalid = [
            {'id': 1, 'date': 'invalid-date-format'},
            {'id': 2, 'date': '2024-01-01T10:00:00'}
        ]
        with pytest.raises(ValueError):
            sort_by_date(transactions_with_invalid)


    def test_empty_list_sorting(self):
        """Тестирование сортировки пустого списка."""
        result = sort_by_date([])
        assert result == []