def total_by_user(transactions):
    if not transactions:
        return {}
    total = {}
    for transaction in transactions:
        total[transaction['user']] = total.get(transaction['user'], 0) + transaction['amount']
    return total


if __name__ == '__main__':
    transactions = [
        {'user': 'a', 'amount': 100},
        {'user': 'b', 'amount': 50},
        {'user': 'a', 'amount': 30},
    ]
    assert total_by_user(transactions) == {'a': 130, 'b': 50}
    assert total_by_user([]) == {}
    assert total_by_user([{'user': 'x', 'amount': 5}]) == {'x': 5}

    print("все тесты прошли")

    # Все операции с словарями в решении имеют константую сложность,
    # а также у нас есть полный проход по списку транзакций,
    # поэтому сложность всей программы O(n)
