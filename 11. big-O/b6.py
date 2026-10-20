from b5 import first_ge_v2

def count_in_range(a: list[int], queries: list[tuple[int, int]]) -> list[int]:
    '''
    Сложность по времени O(q*n)
    Сложность по памяти O(q)
    При n = q = 10^5: 10^10 операций, в 1000 раз больше бюджета 10^7.
    '''
    result = []
    for query in queries:
        count = 0
        for num in a:
            if query[0] <= num <= query[1]:
                count += 1
        result.append(count)
    return result


def count_in_range_v2(a: list[int], queries: list[tuple[int, int]]) -> list[int]:
    '''
    Сложность по времени O(q*logn)
    Сложность по памяти O(q)
    Если a не отсортирован: одна сортировка O(n*logn) заранее,
    итого O((n+q)*logn), а память O(n) на копию (sorted).
    При n = q = 10^5: ~2*17*10^5 = 3.4*10^6 на запросы
    + ~1.7*10^6 на сортировку = ~5*10^6, укладывается в 10^7.
    '''
    result = []
    for query in queries:
        result.append(first_ge_v2(a, query[1] + 1) - first_ge_v2(a, query[0]))
    return result



if __name__ == '__main__':
    import random

    for f in (count_in_range, count_in_range_v2):
        a = [1, 3, 3, 5, 8]
        # пример из условия
        assert f(a, [(2, 5), (3, 3), (6, 7)]) == [3, 2, 0]

        # нет запросов
        assert f(a, []) == []

        # пустой список
        assert f([], [(0, 10), (5, 5)]) == [0, 0]

        # границы включаются
        assert f(a, [(1, 8)]) == [5]
        assert f(a, [(1, 1)]) == [1]
        assert f(a, [(8, 8)]) == [1]
        assert f(a, [(5, 8)]) == [2]

        # отрезок вне данных
        assert f(a, [(-10, 0)]) == [0]
        assert f(a, [(9, 20)]) == [0]
        assert f(a, [(-10, 100)]) == [5]

        # отрезок между элементами
        assert f(a, [(4, 4)]) == [0]
        assert f(a, [(6, 7)]) == [0]

        # одинаковые значения
        assert f([2, 2, 2, 2], [(2, 2), (1, 1), (3, 3), (1, 3)]) == [4, 0, 0, 4]

        # отрицательные числа
        assert f([-5, -3, -3, 0, 4], [(-3, -3), (-4, 0), (-6, -6)]) == [2, 3, 0]

        # одинаковые запросы подряд, порядок ответов = порядок запросов
        assert f(a, [(3, 3), (1, 1), (3, 3)]) == [2, 1, 2]

        # сверка с простым подсчётом на случайных данных
        random.seed(0)
        for _ in range(200):
            n = random.randint(0, 12)
            b = sorted(random.randint(-6, 6) for _ in range(n))
            qs = []
            for _ in range(random.randint(0, 10)):
                l = random.randint(-8, 8)
                qs.append((l, random.randint(l, 8)))
            expected = [sum(1 for v in b if l <= v <= r) for l, r in qs]
            assert f(b, qs) == expected, (b, qs)

        # входные данные не меняются
        c = [1, 3, 3, 5, 8]
        qc = [(2, 5), (3, 3)]
        f(c, qc)
        assert c == [1, 3, 3, 5, 8] and qc == [(2, 5), (3, 3)]

    print('OK')
