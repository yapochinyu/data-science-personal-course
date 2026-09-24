from time import perf_counter
from functools import wraps
import numpy as np

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)
        end = perf_counter()
        elapsed = end - start
        return result, elapsed
    return wrapper

@timer
def python_cycle(lst):
    result = 0
    for num in lst:
        result += num * num
    return result

@timer
def generator(lst):
    return sum(x*x for x in lst)

@timer
def numpy_summator(array):
    return (array**2).sum()

def measure(func, data, repeats=1):
    times = []
    for _ in range(repeats):
        result, elapsed = func(data)
        times.append(elapsed)
    times = times[1:] if len(times) > 1 else times  # выбросить прогревочный вызов
    return result, sum(times) / len(times)


if __name__ == '__main__':
    million_list = list(range(1_000_000))
    small_list = list(range(10))
    million_array = np.array(million_list)
    small_array = np.array(small_list)

    runs = {
        'Python-цикл': (python_cycle, million_list, small_list),
        'Сумма генератора': (generator, million_list, small_list),
        'Сумма ndarray': (numpy_summator, million_array, small_array)
        }

    rows = []
    for name, (func, big_data, small_data) in runs.items():
        result_big, t_big = measure(func, big_data, repeats=1)
        result_small, t_small = measure(func, small_data, repeats=100_000)
        rows.append((name, result_big, t_big, result_small, t_small))

    header = f"{'Способ':<20}{'Время (1e6), с':>18}{'Время (10), с':>18}"
    print(header)
    print('-' * len(header))
    for name, result_big, t_big, result_small, t_small in rows:
        print(f"{name:<20}{t_big:>18.6f}{t_small:>18.9f}")