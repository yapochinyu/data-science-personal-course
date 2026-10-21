def merge(a: list[int], b: list[int]) -> list[int]:
    '''
    Сложность по времени O((n+m)log(n+m))
    Сложность по памяти O(n+m)
    '''
    return sorted(a + b)

def merge_v2(a: list[int], b: list[int]) -> list[int]:
    '''
    Сложность по времени O(n+m)
    Сложность по памяти O(n+m)
    '''
    result = []
    i = 0
    j = 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            result.append(a[i])
            i += 1
        else:
            result.append(b[j])
            j += 1
    if i < len(a):
        result.extend(a[i:])
    elif j < len(b):
        result.extend(b[j:])
    return result


if __name__ == '__main__':
    import random

    for f in (merge, merge_v2):
        # примеры из условия
        assert f([1, 4, 9], [2, 3, 10, 11]) == [1, 2, 3, 4, 9, 10, 11]
        assert f([], [5]) == [5]
        assert f([2, 2], [2]) == [2, 2, 2]

        # оба пустые
        assert f([], []) == []

        # один пустой
        assert f([1, 2, 3], []) == [1, 2, 3]
        assert f([], [1, 2, 3]) == [1, 2, 3]

        # один список целиком меньше другого
        assert f([1, 2], [3, 4]) == [1, 2, 3, 4]
        assert f([3, 4], [1, 2]) == [1, 2, 3, 4]

        # чередование
        assert f([1, 3, 5], [2, 4, 6]) == [1, 2, 3, 4, 5, 6]

        # равные значения в обоих списках
        assert f([1, 2, 2, 3], [2, 2, 4]) == [1, 2, 2, 2, 2, 3, 4]
        assert f([7, 7], [7, 7]) == [7, 7, 7, 7]

        # отрицательные числа
        assert f([-5, -1, 0], [-3, -2, 4]) == [-5, -3, -2, -1, 0, 4]

        # списки разной длины
        assert f([5], [1, 2, 3, 4, 6, 7, 8]) == [1, 2, 3, 4, 5, 6, 7, 8]

        # сверка с sorted на случайных данных
        random.seed(0)
        for _ in range(300):
            a = sorted(random.randint(-6, 6) for _ in range(random.randint(0, 10)))
            b = sorted(random.randint(-6, 6) for _ in range(random.randint(0, 10)))
            assert f(a, b) == sorted(a + b), (a, b)

        # входные данные не меняются
        a = [1, 4, 9]
        b = [2, 3, 10, 11]
        f(a, b)
        assert a == [1, 4, 9] and b == [2, 3, 10, 11]

        # результат — новый список
        a = [1, 2]
        assert f(a, []) is not a

    print('OK')
