
def min_diff(a: list[int]) -> int:
    '''
    Сложность по времени O(n^2)
    Сложность по памяти O(1)
    '''
    minimum = abs(a[0] - a[1])
    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            minimum = min(minimum, abs(a[i] - a[j]))
    return minimum

def min_diff_v2(a: list[int]) -> int:
    '''
    Сложность по времени O(n + n*logn)
    Сложность по памяти O(n)
    '''
    a_sorted = sorted(a)
    minimum = abs(a_sorted[0] - a_sorted[1])
    for i in range(1, len(a_sorted)):
        minimum = min(minimum, abs(a_sorted[i] - a_sorted[i - 1]))
    return minimum

if __name__ == '__main__':
    import random

    for f in (min_diff, min_diff_v2):
        # примеры из условия
        assert f([10, 3, 7, 15, 8]) == 1

        # два элемента
        assert f([1, 5]) == 4
        assert f([5, 1]) == 4

        # дубликаты — разность 0
        assert f([4, 9, 4]) == 0
        assert f([7, 7]) == 0

        # отрицательные числа
        assert f([-10, -3, -7, -15]) == 3
        assert f([-2, 3]) == 5
        assert f([-1, 0, 1]) == 1

        # уже отсортирован / по убыванию
        assert f([1, 2, 4, 8]) == 1
        assert f([8, 4, 2, 1]) == 1

        # ближайшая пара не в начале и не рядом в исходном порядке
        assert f([100, 1, 50, 99, 20]) == 1

        # сверка с перебором всех пар на случайных данных
        random.seed(0)
        for _ in range(300):
            a = [random.randint(-20, 20) for _ in range(random.randint(2, 10))]
            expected = min(abs(a[i] - a[j]) for i in range(len(a)) for j in range(i + 1, len(a)))
            assert f(a) == expected, (f.__name__, a)

        # входной список не меняется
        a = [10, 3, 7, 15, 8]
        f(a)
        assert a == [10, 3, 7, 15, 8]

    print('OK')
