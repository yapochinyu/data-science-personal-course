def two_sum(a: list, target: int) -> tuple[int, int]:
    '''
    Сложность по времени O(n^2)
    Сложность по памяти O(1)
    '''
    for i in range(len(a)):
        for j in range(i+1, len(a)):
            if a[i] + a[j] == target:
                return (i, j)
    else:
        return (-1, -1)

def two_sum_v2(a: list, target: int) -> tuple[int, int]:
    '''
    Сложность по времени O(n)
    Сложность по памяти O(n)
    '''
    seen = {}
    for i in range(len(a)):
        if (_ := target - a[i]) in seen:
            return (seen[_], i)
        else:
            seen[a[i]] = i
    else:
        return (-1, -1)
    



if __name__ == '__main__':
    for f in (two_sum, two_sum_v2):
        # примеры из условия
        assert f([2, 7, 11, 15], 9) == (0, 1)
        assert f([3, 2, 4], 6) == (1, 2)
        assert f([3], 6) == (-1, -1)
        assert f([3, 3], 6) == (0, 1)

        # пустой список и один элемент
        assert f([], 0) == (-1, -1)
        assert f([0], 0) == (-1, -1)

        # пары нет
        assert f([1, 2, 3], 100) == (-1, -1)
        assert f([5, 5, 5], 7) == (-1, -1)

        # пара в конце и в середине
        assert f([1, 2, 3, 4, 5], 9) == (3, 4)
        assert f([1, 4, 8, 6, 3], 10) == (1, 3)

        # пара не рядом, i и j далеко друг от друга
        assert f([8, 1, 1, 1, 1, 2], 10) == (0, 5)

        # отрицательные числа и нули
        assert f([-3, 4, 3, 90], 0) == (0, 2)
        assert f([-1, -2, -3, -4], -7) == (2, 3)
        assert f([0, 4, 3, 0], 0) == (0, 3)
        assert f([0], 0) == (-1, -1)

        # дубликаты: число не должно найти само себя
        assert f([4, 1, 2], 8) == (-1, -1)
        assert f([1, 2, 2, 7], 4) == (1, 2)

        # исходный список не меняется
        a = [3, 2, 4]
        f(a, 6)
        assert a == [3, 2, 4]

    print('OK')
