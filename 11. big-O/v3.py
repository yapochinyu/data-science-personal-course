import io
import os
import random
import sys
import time
from contextlib import redirect_stdout


def solve_slow():
    '''
    Время O(n + q) в среднем, но с q вызовами input() и q вызовами print.
    '''
    _, q = map(int, input().split())
    nums = set(map(int, input().split()))
    for _ in range(q):
        x = int(input())
        print('YES' if x in nums else 'NO')


def solve_fast():
    '''
    Время O(n + q) в среднем: один read, один split, один print.
    '''
    data = sys.stdin.read().split()
    n, q = int(data[0]), int(data[1])
    nums = set(map(int, data[2:2 + n]))
    answers = []
    for i in range(2 + n, 2 + n + q):
        answers.append('YES' if int(data[i]) in nums else 'NO')
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
    queries = [rng.choice(nums) if rng.random() < 0.5 else rng.randint(-10 ** 9, 10 ** 9)
               for _ in range(q)]
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
        solve_fast()
        sys.exit()

    # тесты на корректность
    example = '5 3\n4 8 15 16 23\n8\n5\n23\n'
    assert run(solve_slow, example) == 'YES\nNO\nYES\n'
    assert run(solve_fast, example) == 'YES\nNO\nYES\n'

    text, nums, queries = make_input(1000, 1000, seed=1)
    expected = ''.join('YES\n' if x in set(nums) else 'NO\n' for x in queries)
    assert run(solve_slow, text) == expected
    assert run(solve_fast, text) == expected
    print('тесты: ok\n')

    # замеры
    print(f'{"n = q":>10} {"input+print, с":>16} {"read+join, с":>14} {"во сколько раз":>15}')
    for size in (10 ** 3, 10 ** 4, 10 ** 5, 2 * 10 ** 5):
        text, _, _ = make_input(size, size)
        t_slow = timeit(solve_slow, text)
        t_fast = timeit(solve_fast, text)
        print(f'{size:>10} {t_slow:>16.4f} {t_fast:>14.4f} {t_slow / t_fast:>15.2f}')
