from functools import wraps
from time import perf_counter

def memorize(func):
    result_dict = {}
    @wraps(func)
    def wrapper(*args, **kwargs):
        if args in result_dict:
            wrapper.hits += 1 
            return result_dict[args]
        wrapper.misses += 1
        result = func(*args, **kwargs)
        result_dict[args] = result
        return result
    wrapper.hits = 0
    wrapper.misses = 0
    return wrapper


@memorize
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)


def fib_plain(n):
    if n < 2:
        return n
    return fib_plain(n-1) + fib_plain(n-2)


if __name__ == '__main__':
    assert fib(10) == 55
    assert fib.misses == 11  # n=0..10 посчитаны один раз каждое
    assert fib.hits > 0      # повторные fib(n-1)/fib(n-2) попали в кеш

    misses_before = fib.misses
    assert fib(10) == 55
    assert fib.misses == misses_before  # второй вызов fib(10) - чистое попадание в кеш

    start = perf_counter()
    fib(35)
    cached_time = perf_counter() - start

    start = perf_counter()
    fib_plain(30)  # 35 без кеша будет ощутимо дольше, берём 30 для сравнения
    plain_time = perf_counter() - start

    print(f'memoize: fib(35) = {cached_time:.6f}s, plain: fib_plain(30) = {plain_time:.6f}s')
    print(f'hits: {fib.hits}, misses: {fib.misses}')
    print('OK')
