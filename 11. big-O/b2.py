

def unique_ordered(a: list) -> list:
    '''
    По времени O(n^2)
    По памяти O(n)
    '''

    result = []
    for num in a:
        if num in result:
            pass
        else:
            result.append(num)
    return result


def unique_ordered_v2(a: list) -> list:
    '''
    По времени O(n)
    По памяти O(n)
    '''
    
    result = []
    peek = set()
    for num in a:
        if num in peek:
            pass
        else:
            peek.add(num)
            result.append(num)
    return result

if __name__ == '__main__':
    import random

    # примеры из условия и края
    for func in (unique_ordered, unique_ordered_v2):
        assert func([3, 1, 3, 2, 1]) == [3, 1, 2], func.__name__
        assert func([5, 5, 5]) == [5], func.__name__
        assert func([]) == [], func.__name__
        assert func([1, 2, 3]) == [1, 2, 3], func.__name__
        assert func([2, 1, 2, 3, 1, 4]) == [2, 1, 3, 4], func.__name__
        assert func([-1, 0, -1, 0]) == [-1, 0], func.__name__
        assert isinstance(func([1, 1]), list), func.__name__

    # случайные проверки: обе версии должны совпадать с эталоном
    for _ in range(300):
        a = [random.randint(0, 10) for _ in range(random.randint(0, 20))]
        expected = []
        for x in a:
            if x not in expected:
                expected.append(x)
        assert unique_ordered(a) == expected, a
        assert unique_ordered_v2(a) == expected, a

    print('тесты прошли')

    print(unique_ordered([3, 1, 3, 2, 1]))
    print(unique_ordered([5, 5, 5]))
    print(unique_ordered([]))

    print(unique_ordered_v2([3, 1, 3, 2, 1]))
    print(unique_ordered_v2([5, 5, 5]))
    print(unique_ordered_v2([]))