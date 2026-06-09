from collections import Counter
from typing import List, Dict

def count_transaction_categories(
    transactions: List[Dict],
    categories: List[str]
) -> Dict[str, int]:
    """
    Подсчет количества операций по категориям.
    """
    counter = Counter()
    for transaction in transactions:
        description = transaction.get('description', '').lower()
        for category in categories:
            if category.lower() in description:
                counter[category] += 1
    return dict(counter)