import re
from typing import List, Dict

def search_transactions_by_description(
    transactions: List[Dict],
    search_string: str
) -> List[Dict]:
    """
    Поиск транзакций по описанию с использованием регулярных выражений.
    """
    pattern = re.compile(re.escape(search_string), re.IGNORECASE)
    return [
        transaction
        for transaction in transactions
        if pattern.search(transaction.get('description', ''))
    ]