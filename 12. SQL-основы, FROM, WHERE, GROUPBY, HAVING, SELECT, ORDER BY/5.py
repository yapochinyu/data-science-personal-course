def sql_eq(a, b):          # сравнение a = b по правилам SQL
    if a == None or b == None:
        return None
    else:
        return a == b
def sql_not(a):            # NOT
    if a == None:
        return None
    return not a

def sql_and(a, b):         # AND
    if a is not None and b is not None:
        return a and b
    if a is None:
        a, b = b, a        # неизвестное теперь в b
    with_true, with_false = a and True, a and False
    return with_true if with_true == with_false else None
def sql_or(a, b):          # OR
    if a is not None and b is not None:
        return a or b
    if a is None:
        a, b = b, a
    with_true, with_false = a or True, a or False
    return with_true if with_true == with_false else None
def sql_not_in(x, values): # x NOT IN (values)
    result = True
    for v in values:
        result = sql_and(result, sql_not(sql_eq(x, v)))
    return result
def where_filter(rows, cond):  # оставить элементы rows, для которых cond(элемент) вернула True
    return [row for row in rows if cond(row) is True]


if __name__ == '__main__':
    assert sql_eq(5, None) is None
    assert sql_eq(None, None) is None
    assert sql_eq(5, 5) is True
    assert sql_eq(5, 6) is False

    assert sql_not(None) is None
    assert sql_not(True) is False
    assert sql_not(False) is True

    assert sql_and(True, None) is None
    assert sql_and(None, True) is None
    assert sql_and(False, None) is False
    assert sql_and(None, False) is False
    assert sql_and(None, None) is None
    assert sql_and(True, True) is True
    assert sql_and(True, False) is False

    assert sql_or(True, None) is True
    assert sql_or(None, True) is True
    assert sql_or(False, None) is None
    assert sql_or(None, None) is None
    assert sql_or(False, False) is False
    assert sql_or(True, False) is True

    assert sql_not_in(10, [30, None]) is None
    assert sql_not_in(30, [30, None]) is False
    assert sql_not_in(10, [30]) is True
    assert sql_not_in(10, []) is True

    cond = lambda u: sql_not_in(u, [30, None])
    assert where_filter([10, 20, 30, 40, 50], cond) == []
    cond = lambda u: sql_not_in(u, [30])
    assert where_filter([10, 20, 30, 40, 50], cond) == [10, 20, 40, 50]

    print('all ok')
