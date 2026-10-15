def has_common(a: list, b: list) -> bool:
    small = min(a, b, key=len)
    big = a if small is b else a
    for i in big:
        if i in small:
            return True
    return False

def has_common_smart(a: list, b: list) -> bool:
    small = min(a, b, key=len)
    big = a if small is b else a
    small = set(small)
    for i in big:
            if i in small:
                return True
    return False

if __name__ == '__main__':
    import random
    import time

    # примеры из условия и края
    for func in (has_common, has_common_smart):
        assert func([1, 5, 9], [2, 9, 4]) is True
        assert func([1, 2], [3]) is False
        assert func([], [1]) is False
        assert func([1], []) is False
        assert func([], []) is False
        assert func([7, 7, 7], [7]) is True
        assert func([1, 2, 3], [3, 4, 5]) is True
        assert func([1, 2, 3], [4, 5, 6]) is False

    # случайные проверки: обе версии должны совпадать с эталоном
    for _ in range(300):
        a = [random.randint(0, 30) for _ in range(random.randint(0, 15))]
        b = [random.randint(0, 30) for _ in range(random.randint(0, 15))]
        expected = bool(set(a) & set(b))
        assert has_common(a, b) == expected, (a, b)
        assert has_common_smart(a, b) == expected, (a, b)

    print('тесты на корректность прошли')

    def measure(func, a, b, repeat=3):
        best = float('inf')
        for _ in range(repeat):
            start = time.perf_counter()
            func(a, b)
            best = min(best, time.perf_counter() - start)
        return best

    # замеры: худший случай — общих элементов нет, поэтому проходим весь большой список
    cases = {
        'n=2000, m=2000': (list(range(2000)), list(range(10000, 12000))),
        'n=1000000, m=10': (list(range(1000000)), list(range(-10, 0))),
        'n=10, m=1000000': (list(range(-10, 0)), list(range(1000000))),
    }
    for title, (a, b) in cases.items():
        t_naive = measure(has_common, a, b)
        t_smart = measure(has_common_smart, a, b)
        print(f'{title}: naive {t_naive:.4f} c, smart {t_smart:.4f} c')
