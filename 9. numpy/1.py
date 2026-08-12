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

    for name, (func, big_data, small_data) in runs.items():
        result_big_data, elapsed_big_data = func(big_data)
        result_small_data, elapsed_small_data = func(small_data)
        print(f'{name} result on million = {result_big_data}, time on million = {elapsed_big_data}', end= ' ')
        print(f'result on ten = {result_small_data}, time on ten = {elapsed_small_data}')