def count_pairs(a: list[int], k: int) -> int:
    '''
    Сложность по времени O(n^2)
    Сложность по памяти O(1)
    '''
    count = 0
    for i in range(len(a)):
        for j in range(i+1, len(a)):
            if a[i] + a[j] <= k:
                count += 1
    return count

def count_pairs_v2(a: list[int], k: int) -> int:
    '''
    Сложность по времени O(n)
    Сложность по памяти O(1)
    '''
    count = 0
    i, j = 0, len(a) - 1
    while i < j:
        if a[i] + a[j] <= k:
            count += j - i
            i += 1
        else:
            j -= 1
    return count


if __name__ == '__main__':
    import random

    for f in (count_pairs, count_pairs_v2):
        # пример
        assert f([1, 2, 3, 4, 6], 5) == 4

        # пустой список и один элемент
        assert f([], 5) == 0
        assert f([3], 10) == 0

        # два элемента
        assert f([1, 2], 3) == 1
        assert f([1, 2], 2) == 0

        # сумма ровно k включается
        assert f([1, 4], 5) == 1
        assert f([1, 4], 4) == 0

        # все пары подходят
        assert f([1, 2, 3, 4], 100) == 6

        # ни одна пара не подходит
        assert f([5, 6, 7], 3) == 0

        # одинаковые значения
        assert f([2, 2, 2, 2], 4) == 6
        assert f([2, 2, 2, 2], 3) == 0

        # отрицательные числа
        assert f([-5, -3, 0, 2, 4], 0) == 6
        assert f([-5, -3, 0, 2, 4], -8) == 1
        assert f([-5, -3, 0, 2, 4], -9) == 0

        # сверка с перебором на случайных данных
        random.seed(0)
        for _ in range(300):
            n = random.randint(0, 12)
            b = sorted(random.randint(-6, 6) for _ in range(n))
            k = random.randint(-12, 12)
            expected = sum(1 for i in range(n) for j in range(i + 1, n) if b[i] + b[j] <= k)
            assert f(b, k) == expected, (b, k)

        # входные данные не меняются
        c = [1, 2, 3, 4, 6]
        f(c, 5)
        assert c == [1, 2, 3, 4, 6]

    print('OK')