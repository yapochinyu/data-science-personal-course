# Решения — тема 5 (args/kwargs)

### Задача 2

Напиши функцию `describe(*args, **kwargs)`, которая возвращает строку вида `"got 3 positional, 2 keyword: ['lr', 'epochs']"` — количество позиционных, количество именованных и отсортированный список имён именованных. Проверь на вызове `describe(1, 'a', [2], lr=0.1, epochs=10)`.

```python
def describe(*args, **kwargs):
    return f"got {len(args)} positional, {len(kwargs)} keyword: {[name for name in kwargs]}"

print(describe(1, 'a', [2], lr=0.1, epochs=10))
```

### Задача 4

Напиши функцию `train(X, y, *, lr=0.01, epochs=10, verbose=False)`, где все настройки передаются строго по имени. Продемонстрируй: (а) корректный вызов; (б) вызов `train(X, y, 0.1)` — что произойдёт и почему это защита от бага; (в) объясни, зачем такой API в реальных библиотеках.

```python
def train(X, y, *, lr=0.01, epochs=10, verbose=False):
    return None

X_train = []
y_train = []
# Корректный вызов
train(X_train, y_train, lr=0.005, epochs=100, verbose=True)
# Неправильный вызов
try:
    train(X_train, y_train, 0.1)
except TypeError:
    print('Чтобы избежать путаницы в подборе гиперпараметров, каждый из них является keyword-only')
```

### Задача 5

Есть конфиг: `config = {'n_estimators': 100, 'max_depth': 5, 'comment': 'best run'}` и функция `def make_model(n_estimators, max_depth, random_state=42): ...`. Вызов `make_model(**config)` падает. Объясни почему и напиши функцию `safe_call(func, config)`, которая передаёт в `func` только те ключи из config, которые функция реально принимает (подсказка: `inspect.signature` или явный набор допустимых имён).

```python
import inspect

config = {'n_estimators': 100, 'max_depth': 5, 'comment': 'best run'}

def make_model(n_estimators, max_depth, random_state=42):
    print("ЯХАУ")
    return None

try:
    make_model(**config)
except TypeError:
    print('функция падает с ошибкой, так как ей переданы keyword аргументы, которые не определены при ее создании.')


def safe_call(func, config):
    allowed = set(inspect.signature(func).parameters)
    return func(**{k: v for k, v in config.items() if k in allowed})

safe_call(make_model, config)
```

### Задача 6

Дан список точек `points = [(1, 2), (3, 4), (0, 0), (5, 1)]` и функция `def dist(x1, y1, x2, y2): return ((x1-x2)**2 + (y1-y2)**2) ** 0.5`. Не меняя `dist` и не обращаясь к элементам кортежей по индексам, найди пару точек с максимальным расстоянием. Используй распаковку и `itertools.combinations`.

```python
from itertools import combinations

points = [(1, 2), (3, 4), (0, 0), (5, 1)]

def dist(x1, y1, x2, y2): 
    return ((x1-x2)**2 + (y1-y2)**2) ** 0.5

longest = max(combinations(points, 2), key=lambda pair: dist(*pair[0], *pair[1]))

print(longest)
```

### Задача 7

Дан лог обучения: `log = ['header', 'epoch1: 0.9', 'epoch2: 0.7', 'epoch3: 0.5', 'total: 3']`. Одной строкой распаковки в присваивании разложи его на `header`, `epochs` (список середины) и `total`. Затем ответь: какого типа `epochs`, что в нём окажется при `log` из двух элементов, и почему `a, *b, *c = log` невозможно?

```python
log = ['header', 'epoch1: 0.9', 'epoch2: 0.7', 'epoch3: 0.5', 'total: 3']

header, *epochs, total = log

print(header)
print(epochs)
print(total)
```

### Задача 9

Функция кеширования фичей с багом:

```python
def get_features(user_id, cache={}):
    if user_id not in cache:
        cache[user_id] = expensive_compute(user_id)
    return cache[user_id]
```

(а) Объясни: это баг или намеренный приём? Чем он отличается от бага с `log=[]` из прошлой задачи? (б) Перепиши через паттерн `None`. (в) Объясни, почему вариант `cache = cache or {}` сломает кеширование полностью.

```python
def expensive_compute(x):
    return x**x

def get_features(user_id, cache=None):
    if cache is None:
        cache = {}

    if user_id not in cache:
        cache[user_id] = expensive_compute(user_id)
    return cache[user_id]
```

### Задача 11

Напиши декоратор `retry(n)`, который перезапускает функцию до `n` раз при исключении, а если все попытки провалились — пробрасывает последнее исключение. Требование: должен работать с функцией любой сигнатуры. Продемонстрируй на функции с позиционными и именованными аргументами.

```python
def retry(n):
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_execution = None
            for attempt in range(n):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_execution = e
            raise last_execution
        return wrapper
    return decorator


@retry(3)
def flaky(x, y, fail_times=0):
    flaky.calls = getattr(flaky, 'calls', 0) + 1
    if flaky.calls <= fail_times:
        raise ValueError("падение")
    return x + y

print(flaky(2, 3, fail_times=2))
```

### Задача 12

Есть базовый конфиг и эксперименты:

```python
base = {'lr': 0.01, 'epochs': 100, 'batch_size': 32}
experiments = [{'lr': 0.1}, {'batch_size': 64}, {'lr': 0.001, 'epochs': 200}]
```

Напиши функцию `run_all(model_fn, base, experiments)`, которая для каждого эксперимента вызывает `model_fn` с базовым конфигом, поверх которого наложены параметры эксперимента. Мержить словари — через распаковку `**`, base мутировать нельзя.

```python
base = {'lr': 0.01, 'epochs': 100, 'batch_size': 32}
experiments = [{'lr': 0.1}, {'batch_size': 64}, {'lr': 0.001, 'epochs': 200}]


def run_all(model_fn, base, experiments):
    results = []
    for experiment in experiments:
        results.append(model_fn(**{**base, **experiment}))
    return results
```

### Задача 15

Напиши функцию `pipe(data, *funcs, verbose=False, **common_kwargs)`, которая последовательно применяет к `data` каждую функцию из `funcs`, передавая в каждый вызов также `common_kwargs`; при `verbose=True` печатает имя каждой функции (`func.__name__`). Пример использования:

```python
result = pipe(x, normalize, clip, scale, verbose=True, factor=2)
# каждая функция вызывается как func(data, factor=2)
```

```python
def pipe(data, *funcs, verbose=False, **common_kwargs):
    for func in funcs:
        if verbose:
            print(func.__name__)
        data = func(data, **common_kwargs)
    return data


if __name__ == '__main__':
    def add(x, factor=1):
        return x + factor

    def double(x, factor=1):
        return x * 2

    def mul_factor(x, factor=1):
        return x * factor

    assert pipe(1, add, double) == 4          # (1+1)*2 = 4
    assert pipe(1, add, add, factor=10) == 21  # 1+10+10

    result = pipe(2, mul_factor, verbose=True, factor=3)
    assert result == 6                         # 2*3

    assert pipe(5) == 5                        # без funcs

    print("all tests passed")
```