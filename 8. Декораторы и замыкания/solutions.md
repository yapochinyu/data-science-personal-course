# Решения — Тема 8. Декораторы и замыкания

### Задача 1
Напиши функцию `compose(*funcs)`, которая принимает произвольное число функций и возвращает **новую функцию**, применяющую их слева направо: `pipeline = compose(strip, lower, tokenize)` → `pipeline(text)` эквивалентно `tokenize(lower(strip(text)))`. Проверь на `compose(str.strip, str.lower, str.split)`. Устно: где здесь замыкание и что именно оно держит?

```python
def compose(*funcs):
    def inner(x):
        for func in funcs:
            x = func(x)
        return x
    return inner


if __name__ == '__main__':
    pipeline = compose(str.strip, str.lower, str.split)
    assert pipeline('  Hello WORLD  ') == ['hello', 'world']

    identity = compose()
    assert identity(42) == 42
    assert identity('abc') == 'abc'

    single = compose(str.upper)
    assert single('abc') == 'ABC'

    add_one = lambda x: x + 1
    double = lambda x: x * 2
    assert compose(add_one, double)(3) == 8  # (3+1)*2
    assert compose(double, add_one)(3) == 7  # (3*2)+1

    assert pipeline.__closure__[0].cell_contents == (str.strip, str.lower, str.split)

    print('all tests passed')
```

### Задача 3
Напиши фабрику `make_threshold_filter(threshold)`, возвращающую функцию, которая из списка чисел оставляет только значения выше порога. Создай два независимых фильтра (`strict = make_threshold_filter(0.9)`, `loose = make_threshold_filter(0.5)`), примени оба к `[0.4, 0.6, 0.95]`. Затем распечатай `strict.__closure__[0].cell_contents` и объясни, что ты видишь.

```python
def make_threshold_filter(threshold):
    def threshold_filter(nums):
        filtered = [num for num in nums if num > threshold]
        return filtered
    return threshold_filter


strict = make_threshold_filter(0.9)
loose = make_threshold_filter(0.5)

data = [0.4, 0.6, 0.95]

print(strict(data))
print(loose(data))

print(strict.__closure__[0].cell_contents)
```

### Задача 4
Даны два наброска (счётчик и логгер). Первый падает, второй работает. Объясни, почему, и почини первый. Затем добавь в починенный счётчик функцию сброса: сделай так, чтобы `make_counter()` возвращал **две** функции — `inc` и `reset`, работающие с одним и тем же счётчиком.

```python
def make_counter():
    count = 0
    def inc():
        nonlocal count
        count += 1
        return count

    def reset():
        nonlocal count
        count = 0
        return count
    
    return inc, reset

def make_logger():
    lines = []
    def log(msg):
        lines.append(msg)
        return len(lines)
    return log


if __name__ == '__main__':
    inc, reset = make_counter()
    assert inc() == 1
    assert inc() == 2
    assert inc() == 3
    assert reset() == 0
    assert inc() == 1

    inc2, reset2 = make_counter()
    assert inc2() == 1
    assert inc() == 2  # независим от inc2

    log = make_logger()
    assert log('a') == 1
    assert log('b') == 2
    assert log('c') == 3

    print('all tests passed')
```

### Задача 5
Не запуская, скажи, что напечатает каждый вызов классического примера с `lambda` в цикле, и исправь двумя разными способами. Дополнительно ответь: изменится ли ответ, если заменить цикл на list comprehension?

```python
funcs = []
for i in range(3):
    funcs.append(lambda x, i=i: x * i)

funcs2 = []

def make_mult(i):
    return lambda x: x * i

for i in range(3):
    funcs2.append(make_mult(i))


if __name__ == '__main__':
    assert [f(10) for f in funcs] == [0, 10, 20]
    assert [f(10) for f in funcs2] == [0, 10, 20]
    print('OK')
```

### Задача 6
Напиши с нуля декоратор `timer`, который печатает время выполнения и **возвращает результат оригинальной функции**. Требования: работает с любой сигнатурой, сохраняет `__name__` и докстринг. Проверь на функции `def slow_sum(*nums, delay=0.1): ...` и убедись, что `slow_sum.__name__` не превратился в `'wrapper'`.

```python
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
```

### Задача 9
Напиши декоратор `debug`, который печатает вызов и результат, **сознательно без** `functools.wraps`. Затем в коде продемонстрируй три конкретные поломки: `f.__name__`, `f.__doc__`, `help(f)`. Добавь `wraps` и покажи, что всё починилось. Устно: почему это не косметика, а реальная проблема для FastAPI и pytest?

```python
from functools import wraps


def debug(func):
    def wrapper(*args, **kwargs):
        print(f'function: {func.__name__}, {args, kwargs}')
        result = func(*args, **kwargs)
        return result
    return wrapper

@debug
def summator(*nums, multiplier=1):
    '''
    сумматор
    '''
    return sum(nums * multiplier)

print(summator.__name__)
print(summator.__doc__)
help(summator)


def debug_b(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f'function: {func.__name__}, {args, kwargs}')
        result = func(*args, **kwargs)
        return result
    return wrapper        



@debug_b
def summer(*nums, multiplier=1):
    '''
    сумматор
    '''
    return sum(nums * multiplier)

print(summer.__name__)
print(summer.__doc__)
help(summer)
```

### Задача 10
Напиши декоратор `memoize` со словарём в замыкании: ключ — кортеж позиционных аргументов, значение — результат. Примени к наивной рекурсивной `fib(n)` и сравни `fib(35)` с кешем и без (замерь `time.perf_counter`). Затем добавь атрибуты `wrapper.hits` и `wrapper.misses` — счётчики попаданий и промахов, доступные снаружи.

```python
from functools import wraps
from time import perf_counter

def memoize(func):
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


@memoize
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
```

### Задача 12
Напиши декоратор с параметрами `@validate_range(low, high)`: он проверяет, что **все** числовые позиционные аргументы декорируемой функции лежат в `[low, high]`, иначе бросает `ValueError` с информативным сообщением; при успехе — вызывает оригинал. Проверь на `@validate_range(0, 1) def combine(p1, p2): return p1 * p2`. Затем напиши эквивалент вызова без синтаксического сахара.

```python
from functools import wraps

def validate_range(low, high):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for arg in args:
                if isinstance(arg, (int, float)) and not low <= arg <= high:
                    raise ValueError(f'аргумент {arg} не в диапозоне {low}: {high}')
            result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator


@validate_range(0, 1)
def combine(p1, p2): 
    return p1 * p2


# combine = validate_range(0, 1)(combine)


if __name__ == '__main__':
    assert combine(0.5, 1) == 0.5
    assert combine(0, 1) == 0

    try:
        combine(2, 0.5)
        assert False, 'ожидался ValueError'
    except ValueError:
        pass

    print('OK')
```

### Задача 14
Напиши систему регистрации трансформаций: декоратор `@register('normalize')` кладёт функцию в глобальный словарь `REGISTRY` под указанным именем и **возвращает функцию неизменённой**. Зарегистрируй три функции, затем напиши `apply_pipeline(data, steps)`, применяющий по именам: `apply_pipeline(x, ['normalize', 'clip'])`. Отдельно ответь: почему `register` может вернуть исходную функцию без обёртки?

```python
REGISTRY = {}

def register(name):
    def decorator(func):
        REGISTRY[name] = func
        return func
    return decorator


@register('normalize')
def normalize(data):
    return [x / max(data) for x in data]


@register('clip')
def clip(data, low=0, high=1):
    return [min(max(x, low), high) for x in data]


@register('double')
def double(data):
    return [x * 2 for x in data]


def apply_pipeline(data, steps):
    for step in steps:
        if step not in REGISTRY:
            raise ValueError(f'неизвестный шаг: {step}')
        data = REGISTRY[step](data)
    return data


# register может вернуть функцию без обёртки, потому что декоратору не
# обязательно менять поведение функции — здесь его задача исчерпывается
# побочным эффектом (записью в REGISTRY) в момент определения функции.
# Вызов функции остаётся прежним, никакой обёртки не требуется.


if __name__ == '__main__':
    assert apply_pipeline([1, 2, 4], ['normalize']) == [0.25, 0.5, 1.0]
    assert apply_pipeline([-1, 0.5, 2], ['clip']) == [0, 0.5, 1]
    assert apply_pipeline([1, 2], ['double']) == [2, 4]
    assert apply_pipeline([1, 2, 4], ['normalize', 'clip']) == [0.25, 0.5, 1.0]

    try:
        apply_pipeline([1], ['unknown'])
        assert False, 'ожидался ValueError'
    except ValueError:
        pass

    print('OK')
```

### Задача 15
Напиши декоратор `@rate_limited(max_calls)`: он разрешает функции выполниться не более `max_calls` раз, а на всех последующих вызовах бросает `RuntimeError('лимит вызовов исчерпан')`. Требования: счётчик живёт в замыкании (не глобальная переменная), работает с любой сигнатурой, метаданные сохранены, счётчик у каждой декорированной функции свой. Продемонстрируй независимость на двух разных функциях.

```python
from functools import wraps

def rate_limited(max_calls):
    def decorator(func):
        calls = 0

        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal calls
            if calls >= max_calls:
                raise RuntimeError('лимит вызовов исчерпан')
            calls += 1
            return func(*args, **kwargs)
        return wrapper
    return decorator


@rate_limited(2)
def greet(name):
    return f'привет, {name}'


@rate_limited(1)
def shout(text):
    return text.upper()


if __name__ == '__main__':
    assert greet('a') == 'привет, a'
    assert greet('b') == 'привет, b'
    try:
        greet('c')
        assert False, 'ожидался RuntimeError'
    except RuntimeError:
        pass

    # независимость: у shout свой счётчик, greet его уже исчерпал
    assert shout('ok') == 'OK'
    try:
        shout('again')
        assert False, 'ожидался RuntimeError'
    except RuntimeError:
        pass

    assert greet.__name__ == 'greet'

    print('OK')
```