def range_sums(a: list[int], queries: list[tuple[int, int]]) -> list[int]:
    result = []
    for query in queries:
        result.append(sum(a[query[0] : query[1] + 1]))
    return result

def range_sums_v2(a: list[int], queries: list[tuple[int, int]]) -> list[int]:
    p = [0]  
    for x in a:
        p.append(p[-1] + x)
    result = []
    for query in queries:
        result.append(p[query[1] + 1] - p[query[0]])
    return result


if __name__ == '__main__':
    for f in (range_sums, range_sums_v2):
        # пример из условия
        assert f([3, 1, 4, 1, 5], [(0, 2), (1, 3), (4, 4)]) == [8, 6, 5]
        # отрезок из одного элемента: в начале, в середине, в конце
        assert f([7, 2, 9], [(0, 0), (1, 1), (2, 2)]) == [7, 2, 9]
        # весь список целиком
        assert f([1, 2, 3, 4], [(0, 3)]) == [10]
        # отрицательные числа и нули
        assert f([-5, 0, 3, -2], [(0, 3), (0, 1), (2, 3)]) == [-4, -5, 1]
        # элементы, которые больше длины списка (ловит путаницу значений и индексов)
        assert f([100, 200, 300], [(0, 2), (1, 2)]) == [600, 500]
        # повторяющиеся значения
        assert f([2, 2, 2, 2], [(1, 2), (0, 3)]) == [4, 8]
        # запросы в произвольном порядке и повторяющиеся запросы
        assert f([1, 2, 3, 4, 5], [(3, 4), (0, 1), (3, 4)]) == [9, 3, 9]
        # нет запросов
        assert f([1, 2, 3], []) == []
        # список из одного элемента
        assert f([42], [(0, 0)]) == [42]

    # обе версии совпадают на всех возможных отрезках
    a = [3, -1, 4, 0, -5, 9, 2]
    queries = [(l, r) for l in range(len(a)) for r in range(l, len(a))]
    assert range_sums(a, queries) == range_sums_v2(a, queries)
    assert range_sums(a, queries) == [sum(a[l:r + 1]) for l, r in queries]
    print('ok')
