def leaked_users_naive(train_users, test_users):
    leaked = []
    for user in train_users:
        if user in test_users:
            leaked.append(user)
    return leaked

 


def leaked_users(train_users, test_users):
    leaked = set(train_users) & set(test_users)
    return list(leaked)


if __name__ == '__main__':
    # обычный случай
    result = leaked_users(['a', 'b', 'c'], ['b', 'c', 'd'])
    assert set(result) == {'b', 'c'}, f"ожидали {{'b','c'}}, получили {result}"

    # нет пересечений
    result = leaked_users(['a', 'b'], ['c', 'd'])
    assert result == [], f"ожидали [], получили {result}"

    # один список пустой
    assert leaked_users([], ['a', 'b']) == []
    assert leaked_users(['a', 'b'], []) == []

    # дубликаты внутри одного списка не влияют
    result = leaked_users(['a', 'a', 'b'], ['a'])
    assert set(result) == {'a'}

    print("все тесты прошли")
