from src.analysis import count_transaction_categories


def test_count_categories():
    transactions = [
        {'description': 'Покупка продуктов'},
        {'description': 'Оплата ЖКХ'},
        {'description': 'Покупка продуктов'},
        {'description': 'Перевод'}
    ]

    categories = ['покупка', 'оплата']
    result = count_transaction_categories(transactions, categories)
    assert result == {'покупка': 2, 'оплата': 1}