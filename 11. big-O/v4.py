import io
import os
import random
import sys
import time
from contextlib import redirect_stdout


def first_ge(a: list, x) -> int:
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo


def solve():
    '''
    Время O(n log n + q log n): одна сортировка, потом бинарный поиск на запрос.
    Наивное решение - O(n * q) = 4 * 10**10 при максимальных ограничениях.
    '''
    data = sys.stdin.read().split()
    n, q = int(data[0]), int(data[1])
    nums = sorted(map(int, data[2:2 + n]))
    answers = []
    for i in range(2 + n, 2 + n + q):
        answers.append(str(first_ge(nums, int(data[i]))))
    print('\n'.join(answers))


def solve_naive():
    '''
    Время O(n * q): на каждый запрос проход по всем числам.
    '''
    data = sys.stdin.read().split()
    n, q = int(data[0]), int(data[1])
    nums = list(map(int, data[2:2 + n]))
    answers = []
    for i in range(2 + n, 2 + n + q):
        x = int(data[i])
        count = 0
        for v in nums:
            if v < x:
                count += 1
        answers.append(str(count))
    print('\n'.join(answers))


def run(func, text, out=None):
    '''
    Запускает func так, будто text подан на стандартный ввод.
    Возвращает вывод как строку, если out не задан, иначе пишет в out.
    '''
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(text)
    try:
        if out is None:
            buf = io.StringIO()
            with redirect_stdout(buf):
                func()
            return buf.getvalue()
        with redirect_stdout(out):
            func()
    finally:
        sys.stdin = old_stdin


def make_input(n, q, seed=0):
    rng = random.Random(seed)
    nums = [rng.randint(-10 ** 9, 10 ** 9) for _ in range(n)]
    queries = [rng.randint(-10 ** 9, 10 ** 9) for _ in range(q)]
    lines = [f'{n} {q}', ' '.join(map(str, nums))] + [str(x) for x in queries]
    return '\n'.join(lines) + '\n', nums, queries


def timeit(func, text):
    # вывод в os.devnull, чтобы не мерить скорость терминала
    with open(os.devnull, 'w') as devnull:
        start = time.perf_counter()
        run(func, text, devnull)
        return time.perf_counter() - start


if __name__ == '__main__':
    if '--bench' not in sys.argv:
        solve()
        sys.exit()

    # тесты на корректность
    example = '5 3\n5 1 4 1 9\n2\n5\n10\n'
    assert run(solve, example) == '2\n3\n5\n'
    assert run(solve_naive, example) == '2\n3\n5\n'

    # повторяющиеся числа, x меньше всех, x больше всех, x равен элементу
    edge = '4 4\n3 3 3 3\n3\n2\n4\n-100\n'
    assert run(solve, edge) == '0\n0\n4\n0\n'

    text, nums, queries = make_input(1000, 1000, seed=1)
    expected = ''.join(f'{sum(v < x for v in nums)}\n' for x in queries)
    assert run(solve, text) == expected
    assert run(solve_naive, text) == expected
    print('тесты: ok\n')

    # замеры: наивное решение на небольших размерах, быстрое на всех
    print(f'{"n = q":>10} {"наивное, с":>12} {"бинпоиск, с":>13} {"во сколько раз":>15}')
    for size in (10 ** 3, 2 * 10 ** 3, 4 * 10 ** 3, 8 * 10 ** 3):
        text, _, _ = make_input(size, size)
        t_naive = timeit(solve_naive, text)
        t_fast = timeit(solve, text)
        print(f'{size:>10} {t_naive:>12.4f} {t_fast:>13.4f} {t_naive / t_fast:>15.1f}')

    text, _, _ = make_input(2 * 10 ** 5, 2 * 10 ** 5)
    t_max = timeit(solve, text)
    print(f'\nбинпоиск при n = q = 2 * 10**5: {t_max:.3f} с')

    # наивное при максимуме слишком долго мерить, оцениваем по последнему замеру:
    # время растёт как n * q, то есть в 4 раза при удвоении размера
    scale = (2 * 10 ** 5 / size) ** 2
    print(f'наивное при n = q = 2 * 10**5 (оценка): {t_naive * scale:.0f} с')
