# Решения — тема 7 (Исключения и контекстные менеджеры)

## Задача 4

Дан список строк из лога: `lines = ['0.91', '0.87', 'corrupt', '0.93', '', '1.2e-1', 'NaN?']`. Напиши функцию `parse_metrics(lines)`, которая возвращает кортеж `(values, errors)`: список успешно распарсенных float и список кортежей `(номер_строки, текст_ошибки)` для битых. Требования: ловить только ожидаемый тип ошибки, номера строк с 1, ни одна битая строка не должна прерывать обработку.

```python
lines = ['0.91', '0.87', 'corrupt', '0.93', '', '1.2e-1', 'NaN?']

def parse_metrics(lines):
    values, errors = [], [] 
    for i, line in enumerate(lines):
        try:
            values.append(float(line))
        except ValueError as e:
            errors.append((i, str(e)))
    return values, errors

if __name__ == '__main__':
    values, errors = parse_metrics(lines)
    assert values == [0.91, 0.87, 0.93, 0.12]
    assert [i for i, _ in errors] == [2, 4, 6]
    assert len(errors) == 3

    values, errors = parse_metrics([])
    assert values == []
    assert errors == []

    values, errors = parse_metrics(['1', '2', '3'])
    assert values == [1.0, 2.0, 3.0]
    assert errors == []

    values, errors = parse_metrics(['abc'])
    assert values == []
    assert len(errors) == 1
    assert errors[0][0] == 0

    print('OK')
```

## Задача 5

Код коллеги:

```python
try:
    user = load_user(user_id)          # может бросить KeyError
    permissions = user['permissions']   # тоже может бросить KeyError!
    grant_access(permissions)
except KeyError:
    print(f'Пользователь {user_id} не найден')
```

Объясни, какой баг здесь прячется и какое сообщение получит человек при битой записи пользователя (без ключа 'permissions'). Перепиши через `else`, чтобы каждая ошибка интерпретировалась верно.

```python
# try:
#     user = load_user(user_id)          # может бросить KeyError
#
# except KeyError:
#     print(f'Пользователь {user_id} не найден')
# else:
#     try:
#         permissions = user['permissions']   # тоже может бросить KeyError!
#     except KeyError:
#         print(f'У пользователя {user_id} нет разрешения')
#     else:
#         grant_access(permissions)
```

## Задача 6

Напиши функцию `train_test_split_strict(X, y, test_size)`: она должна бросать `ValueError` с информативным сообщением, если (а) длины X и y не совпадают, (б) `test_size` не в интервале (0, 1), (в) выборка настолько мала, что train или test окажутся пустыми. Если всё ок — вернуть индекс разреза `int(len(X) * (1 - test_size))`. Устно: почему «упасть сразу» лучше, чем «молча посчитать»?

```python
def train_test_split_strict(X, y, test_size):
    if not 0 < test_size < 1:
        raise ValueError(f'test_size: {test_size} не в диапазоне от 0 до 1')
    if len(X) != len(y):
        raise ValueError('Длины X и y не совпадают')
    if (split_idx := int(len(X) * (1 - test_size))) in (0, len(X)):
        raise ValueError(f'Выборка мала (len(X)={len(X)}, test_size={test_size}): train или test пустые')
    return split_idx
```

## Задача 7

Напиши функцию `load_config(path)`, которая читает JSON-конфиг и при любой проблеме (файла нет / JSON битый) бросает наружу единый `ConfigError` (свой класс) с человекочитаемым сообщением, но с сохранением исходной причины в цепочке. Вызывающий код должен видеть в traceback обе ошибки.

```python
import json

class ConfigError(Exception):
    pass

def load_config(path):
    try:
        with open(path) as f:
            config = json.load(f)
    except FileNotFoundError as e:
        raise ConfigError(f'Файл конфига не найден {path}') from e
    except json.JSONDecodeError as e:
        raise ConfigError(f'Файл конфига невалидный: {path}') from e
```

## Задача 9

Напиши класс `Timer`, работающий так:

```python
with Timer('inference') as t:
    heavy_work()
print(t.elapsed)   # время в секундах доступно ПОСЛЕ выхода из блока
```

Требования: печатает `[inference] 3.42s` при выходе, время замеряется даже если внутри блока вылетело исключение, исключение не гасится. Ответь устно: что должен вернуть `__enter__`, чтобы `as t` работал, и что означает возврат `False` из `__exit__`?

```python
import time

class Timer:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.start = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.time() - self.start
        print(f'[{self.name}] {self.elapsed:.2f}')
        return False


if __name__ == '__main__':
    with Timer('sleep') as t:
        time.sleep(0.05)
    assert t.elapsed >= 0.05
    assert isinstance(t.elapsed, float)

    try:
        with Timer('boom') as t2:
            raise ValueError('boom')
    except ValueError:
        pass
    else:
        assert False, 'исключение должно было пролететь дальше'
    assert t2.elapsed >= 0

    print('OK')
```

## Задача 10

Перепиши Timer из задачи 9 через `@contextmanager`. Затем напиши второй менеджер `temp_seed(seed)`: внутри блока `with temp_seed(42):` у `random` зафиксирован seed, а при выходе восстанавливается прежнее состояние генератора (`random.getstate()` / `random.setstate()`), даже при исключении. Устно: какую роль играет `yield` и почему код после него обязан быть в `finally`?

```python
from contextlib import contextmanager
import time
import random

@contextmanager
def Timer(name):
    start = time.time()
    state = {}
    try:
        yield state
    finally:
        state['elapsed'] = time.time() - start
        print(f'[{name}] {state["elapsed"]:.2f}')

@contextmanager
def temp_seed(seed):
    state = random.getstate()
    random.seed(seed)
    try:
        yield
    finally:
        random.setstate(state)


if __name__ == '__main__':
    with Timer('sleep') as t:
        time.sleep(0.05)
    assert t['elapsed'] >= 0.05

    try:
        with Timer('boom') as t2:
            raise ValueError('boom')
    except ValueError:
        pass
    else:
        assert False, 'исключение должно было пролететь дальше'
    assert t2['elapsed'] >= 0

    random.seed(123)
    before = random.getstate()
    with temp_seed(42):
        a = random.random()
    with temp_seed(42):
        b = random.random()
    assert a == b, 'одинаковый seed должен давать одинаковое число'
    assert random.getstate() == before, 'состояние генератора должно восстановиться'

    try:
        with temp_seed(1):
            raise ValueError('boom')
    except ValueError:
        pass
    else:
        assert False, 'исключение должно было пролететь дальше'
    assert random.getstate() == before, 'состояние должно восстановиться даже после исключения'

    print('OK')
```

## Задача 12

Напиши функцию `fetch_with_retry(fetch_fn, max_attempts=3, delay=1.0)`: вызывает `fetch_fn()`, при `ConnectionError` или `TimeoutError` ждёт `delay` секунд (`time.sleep`) и пробует снова, максимум `max_attempts` попыток; каждую неудачу логирует print-ом с номером попытки; если все попытки исчерпаны — перебрасывает последнее исключение. Любые другие типы ошибок должны лететь наружу сразу, без retry.

```python
import time

def fetch_with_retry(fetch_fn, max_attempts=3, delay=1.0):
    for attempt in range(max_attempts):
        try:
            return fetch_fn()
        except (ConnectionError, TimeoutError) as e:
            print(f'Попытка {attempt+1} не удалась {e}')
            if attempt == max_attempts - 1:
                raise
            time.sleep(delay)


if __name__ == '__main__':
    def always_ok():
        return 'data'

    assert fetch_with_retry(always_ok, delay=0) == 'data'

    calls = {'n': 0}
    def fails_twice_then_ok():
        calls['n'] += 1
        if calls['n'] <= 2:
            raise ConnectionError('no network')
        return 'data'

    assert fetch_with_retry(fails_twice_then_ok, max_attempts=3, delay=0) == 'data'
    assert calls['n'] == 3

    def always_fails():
        raise TimeoutError('timeout')

    try:
        fetch_with_retry(always_fails, max_attempts=3, delay=0)
    except TimeoutError:
        pass
    else:
        assert False, 'должно было перебросить исключение после исчерпания попыток'

    def raises_value_error():
        raise ValueError('bad data')

    try:
        fetch_with_retry(raises_value_error, max_attempts=3, delay=0)
    except ValueError:
        pass
    else:
        assert False, 'ValueError должен лететь наружу сразу, без retry'

    print('OK')
```

## Задача 13

Дан словарь кешированных предсказаний `cache` и функция `compute(x)`. Напиши получение значения «из кеша или вычислить и положить» тремя способами: (а) LBYL через `if in`; (б) EAFP через try/except KeyError; (в) идиоматично одним методом словаря (подумай, какой из двух подходит: `get` или `setdefault` — и чем они тут отличаются!). Затем назови сценарий, где (а) содержит race condition, а (б) — нет.

```python
# #LBYL
# if x in cache:
#     val = cache[x]
# else:
#     val = compute(x)
#     cache[x] = val

# #EAFP
# try:
#     val = cache[x]
# except KeyError:
#     val = compute(x)
#     cache[x] = val

# #idiom
# val = cache.get(x, compute(x))
```

## Задача 14

Ревью кода стажёра — найди минимум четыре проблемы и перепиши правильно:

```python
def process_dataset(paths):
    results = []
    for path in paths:
        try:
            f = open(path)
            data = json.load(f)
            results.append(transform(data))
            f.close()
        except:
            pass
    return results
```

```python
import json

def process_dataset(paths):
    results = []
    for path in paths:
        try:
            with open(path) as f:
                data = json.load(f)
                results.append(transform(data))
        except (OSError, json.JSONDecodeError) as e:
            print(f'Путь: {path} Ошибка: {e}')
    return results
```
