import numpy as np
import time
from functools import wraps


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        wrapper.last_elapsed = elapsed
        return result
    wrapper.last_elapsed = None
    return wrapper


@timer
def f_vectorize(a):
    f = np.vectorize(lambda x: x**2 if x > 0 else -x)
    return f(a)


@timer
def f_listcomp(a):
    return np.array([x**2 if x > 0 else -x for x in a])


@timer
def f_where(a):
    return np.where(a > 0, a**2, -a)


def print_timings(funcs, a):
    rows = []
    for func in funcs:
        func(a)
        cold = func.last_elapsed  # первый вызов
        func(a)
        warm = func.last_elapsed  # прогретый вызов
        rows.append((func.__name__, cold, warm))

    name_width = max(len(name) for name, _, _ in rows)
    print(f'{"function":<{name_width}}  {"cold (s)":>10}  {"warm (s)":>10}')
    for name, cold, warm in rows:
        print(f'{name:<{name_width}}  {cold:>10.4f}  {warm:>10.4f}')

    return rows


if __name__ == '__main__':
    a = np.random.uniform(-1000, 1000, size=1_000_000)
    print_timings([f_vectorize, f_listcomp, f_where], a)

    ref = f_where(a)
    for func in (f_vectorize, f_listcomp):
        assert np.allclose(func(a), ref)

    print('all tests passed')
