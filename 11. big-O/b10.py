
def ways_naive(n: int) -> int:
    '''
    Сложность по времени O(^n)
    Сложность по памяти O(n)
    '''
    if n == 2:
        return 2
    if n <= 1:
        return 1
    return ways_naive(n - 1) + ways_naive(n - 2) + ways_naive(n - 3)

def ways_memo(n: int, memo=None) -> int:
    '''
    Сложность по времени O(n)
    Сложность по памяти O(n)
    '''
    
    if memo is None:
        memo = {}
    if n == 2:
        return 2
    if n <= 1:
        return 1
    if n in memo:
        return memo[n]
    memo[n] = ways_memo(n - 1, memo) + ways_memo(n - 2, memo) + ways_memo(n - 3, memo)
    return memo[n]

def ways_loop(n: int) -> int:
    '''
    Время O(n), память O(1): хранятся только три последних значения.
    '''
    if n == 2:
        return 2
    if n <= 1:
        return 1
    a, b, c = 1, 1, 2  # ways(0), ways(1), ways(2)
    for _ in range(n - 2):
        a, b, c = b, c, a + b + c
    return c


if __name__ == '__main__':
    expected = [1, 1, 2, 4, 7, 13, 24, 44]
    for n, e in enumerate(expected):
        assert ways_naive(n) == e
        assert ways_memo(n) == e
        assert ways_loop(n) == e

    assert ways_memo(500) == ways_loop(500)

    try:
        ways_memo(5000)  # глубина стопки около 5000 кадров, лимит около 1000
        assert False, 'ожидали RecursionError'
    except RecursionError:
        pass

    assert ways_loop(5000) > 0
    assert ways_loop(10 ** 5) > 0
    print('ok')
