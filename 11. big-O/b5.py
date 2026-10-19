def first_ge(a: list, x) -> int:
    '''
    
    '''
    for i in range(len(a)):
        if a[i] >= x:
            return i
    return len(a)

def first_ge_v2(a: list, x) -> int:
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo

    


if __name__ == '__main__':
    for f in (first_ge, first_ge_v2):
        a = [1, 3, 3, 5, 8]
        # примеры из условия
        assert f(a, 3) == 1
        assert f(a, 4) == 3
        assert f(a, 0) == 0
        assert f(a, 9) == 5
        assert f([], 7) == 0

        # границы: первый и последний элемент
        assert f(a, 1) == 0
        assert f(a, 8) == 4
        assert f(a, 2) == 1
        assert f(a, 6) == 4

        # один элемент
        assert f([5], 4) == 0
        assert f([5], 5) == 0
        assert f([5], 6) == 1

        # много одинаковых значений
        assert f([2, 2, 2, 2], 2) == 0
        assert f([2, 2, 2, 2], 1) == 0
        assert f([2, 2, 2, 2], 3) == 4
        assert f([1, 2, 2, 2, 2, 3], 2) == 1
        assert f([1, 2, 2, 2, 2, 3], 3) == 5

        # отрицательные числа
        assert f([-5, -3, -3, 0, 4], -3) == 1
        assert f([-5, -3, -3, 0, 4], -4) == 1
        assert f([-5, -3, -3, 0, 4], -6) == 0

        # чётная и нечётная длина, все x подряд: ответ = число элементов < x
        for b in ([1, 3, 3, 5, 8], [1, 3, 3, 5], [0, 0, 1, 1, 2, 2], [7]):
            for x in range(-1, 11):
                assert f(b, x) == sum(1 for v in b if v < x)

        # исходный список не меняется
        c = [1, 3, 3, 5, 8]
        f(c, 3)
        assert c == [1, 3, 3, 5, 8]

    print('OK')
