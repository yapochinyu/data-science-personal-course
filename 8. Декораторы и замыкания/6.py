from functools import wraps
from time import time
from time import sleep

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        finish = time() - start
        print(f'function: {func.__name__}, time: {finish:.2f}')
        return result
    return wrapper

@timer
def slow_sum(*nums, delay=0.1):
    '''
    Функция складывает все позиционные аргументы, каждая следующая прибавка
    вычисляется через delay, по умолчанию 0.1
    '''
    summa = 0
    for num in nums:
        summa += num
        sleep(delay)
    return summa

if __name__ == '__main__':
    assert slow_sum(1, 1, 1, 1, 1, 1, 1) == 7
    assert slow_sum.__name__ == 'slow_sum'
    assert slow_sum.__doc__ is not None
    print('OK')