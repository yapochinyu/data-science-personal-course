import pandas as pd


def find_breaking_id(start: int) -> int:
    x = start
    while int(pd.Series([x, None]).iloc[0]) == x:
        x += 1
    return x


if __name__ == '__main__':
    limit = 2 ** 53

    # пример из условия: граница рядом с 2**53 + 1
    res = find_breaking_id(9_007_199_254_740_990)
    assert res == limit + 1

    # если начать выше границы, портится сразу или через пару шагов
    assert find_breaking_id(limit + 1) == limit + 1

    # найденное число действительно портится, предыдущее — нет
    assert int(pd.Series([res, None]).iloc[0]) != res
    assert int(pd.Series([res - 1, None]).iloc[0]) == res - 1

    # до границы всё точно
    assert int(pd.Series([limit, None]).iloc[0]) == limit
    assert int(pd.Series([12345, None]).iloc[0]) == 12345

    # Int64 не ломается ни на границе, ни выше
    for x in [limit - 1, limit, limit + 1, limit + 3, 10 ** 15, 10 ** 17, 10 ** 18]:
        s = pd.Series([x, None], dtype='Int64')
        assert s.iloc[0] == x
        assert s.isna().iloc[1]

    print('all tests passed')