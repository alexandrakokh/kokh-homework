from src.search import search_transactions_by_description


def test_search_transactions():
    transactions = [
        {'description': 'Покупка в магазине'},
        {'description': 'Оплата услуг'},
        {'description': 'Перевод другу'}
    ]

    assert len(search_transactions_by_description(transactions, 'покупка')) == 1
    assert len(search_transactions_by_description(transactions, 'перевод')) == 1
