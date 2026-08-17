# Тема 9. numpy — решения

### 1. → Идеи 1, 2

**Код + рассуждение.** Замерь через `time.perf_counter` сумму квадратов миллиона чисел тремя способами: питоновский цикл по `list`, `sum(x*x for x in lst)`, `(a**2).sum()` на `ndarray`. Затем повтори замер на массиве из 10 элементов и объясни, почему картина переворачивается. Дополнительно: сделай `a.astype(object)` и объясни, какая из четырёх причин скорости исчезла.

```python
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
```

---

### 2. → Идеи 3, 4

**Каверзная, код руками.** Массив `a` — C-непрерывный, формы `(1000, 50)`. Для каждого выражения скажи «view или copy» и обоснуй через критерий регулярности, затем проверь себя кодом через `np.shares_memory`: `a[10:20]`, `a[::-2]`, `a[[0,1,2]]`, `a[np.ones(1000, dtype=bool)]`, `a[0, :]`, `a[:, 0]`, `a.T`, `a.flatten()`, `a.ravel()`.

```python
import numpy as np

a = np.arange(50000).reshape(1000, 50)


b1 = a[10:20] # view
b2 = a[::-2] # view
b3 = a[[0,1,2]] # copy
b4 = a[np.ones(1000, dtype=bool)] #copy
b5 = a[0, :] # view
b6 = a[:, 0] # view
b7 = a.T # view
b8 = a.flatten() # copy
b9 = a.ravel() # view

# print("a", a, "b1", b1, "b2", b2, "b3", b3, "b4", b4, "b5", b5, "b6", b6, "b7", b7, "b8", b8, "b9", b9, sep='\n')

b_list = [b1, b2, b3, b4, b5, b6, b7, b8, b9]

for i, b in enumerate(b_list, start = 1):
    print(f"a shares memory with b{i}" if np.shares_memory(a, b) else f"a doesn't share memory with b{i}")
```

---

### 3. → Идея 4

**Код руками, отладочная.** Напиши `zero_negatives_inplace(a)` (обнуляет отрицательные в самом `a`) и `zero_negatives_copy(a)` (возвращает новый массив, вход не трогает). Затем напиши третью функцию, которая выглядит как первая, но ничего не меняет, и объясни почему. Добавь `assert`, который ловит эту ошибку.

```python
import numpy as np

def zero_negatives_inplase(arr: np.ndarray):
    arr[arr < 0] = 0
    return arr


def zero_negatives_copy(arr: np.ndarray):
    arr_copy = arr.copy()
    arr_copy[arr_copy < 0] = 0
    return arr_copy


if __name__ == '__main__':
    a = np.array([-3, 1, -2, 5, -1])
    result = zero_negatives_inplase(a)
    assert np.array_equal(a, [0, 1, 0, 5, 0])
    assert result is a

    a = np.array([-3, 1, -2, 5, -1])
    before = a.copy()
    result = zero_negatives_copy(a)
    assert np.array_equal(a, before)
    assert np.array_equal(result, [0, 1, 0, 5, 0])

    print("OK")
```

---

### 4. → Идея 5

**Код руками + провокация.** Отбери из `a` элементы, которые строго больше 0 и меньше 10 и при этом не NaN. Сначала напиши «интуитивный» вариант через `and`/`not`, объясни ошибку, потом правильный. Отдельно скажи, что вернут `~np.array([True, False])` и `~np.array([1, 0], dtype=np.int8)`, и почему второе опасно.

```python
import numpy as np

a = np.array([-5, 5, 10, 15, np.nan, 0, -1, 9, np.nan, 17, 7, 5])

if __name__ == '__main__':
    try:
        wrong_mask = (a > 0) and (a < 10) and not np.isnan(a)
        wrong_result = a[wrong_mask]
        assert False, "ожидалась ValueError на 'and' с массивом"
    except ValueError:
        pass

    mask = (a > 0) & (a < 10) & ~np.isnan(a)
    result = a[mask]
    assert np.array_equal(result, [5, 9, 7, 5])

    assert np.array_equal(~np.array([True, False]), [False, True])
    assert np.array_equal(~np.array([1, 0], dtype=np.int8), [-2, -1]) # побитовая инверсия на числах происходит в дополнительном коде

    print("OK")
```

---

### 5. → Идея 6

**Код руками.** Напиши три нормализации матрицы `X` формы `(n, d)`: (а) стандартизация по признакам, (б) деление каждой строки на её сумму, (в) min-max по строкам в `[0,1]`. Везде используй `keepdims`. Затем убери `keepdims` и покажи, в каком случае код упадёт, а в каком молча посчитает не то. Объясни, почему второй случай хуже.

```python
import numpy as np


def standardize_features(X: np.ndarray) -> np.ndarray:
    # по каждому признаку (столбцу): вычесть среднее, поделить на std
    mean = X.mean(axis=0, keepdims=True)   # (1, d)
    std = X.std(axis=0, keepdims=True)     # (1, d)
    return (X - mean) / std


def normalize_rows_by_sum(X: np.ndarray) -> np.ndarray:
    # каждая строка делится на свою сумму
    row_sum = X.sum(axis=1, keepdims=True)  # (n, 1)
    return X / row_sum


def minmax_rows(X: np.ndarray) -> np.ndarray:
    # каждая строка приводится к [0, 1] по своему min/max
    row_min = X.min(axis=1, keepdims=True)  # (n, 1)
    row_max = X.max(axis=1, keepdims=True)  # (n, 1)
    return (X - row_min) / (row_max - row_min)


# те же три функции, но без keepdims - для демонстрации проблемы
def standardize_features_no_keepdims(X: np.ndarray) -> np.ndarray:
    mean = X.mean(axis=0)   # (d,)
    std = X.std(axis=0)     # (d,)
    return (X - mean) / std  # (d,) broadcast-ится к (n,d) по столбцам - совпадает с ожиданием


def normalize_rows_by_sum_no_keepdims(X: np.ndarray) -> np.ndarray:
    row_sum = X.sum(axis=1)  # (n,)
    return X / row_sum       # (n,) broadcast-ится к (n,d) по столбцам, а нужно было по строкам


def minmax_rows_no_keepdims(X: np.ndarray) -> np.ndarray:
    row_min = X.min(axis=1)  # (n,)
    row_max = X.max(axis=1)  # (n,)
    return (X - row_min) / (row_max - row_min)


if __name__ == '__main__':
    X = np.array([
        [1., 2., 3., 4.],
        [10., 20., 30., 40.],
        [5., 8., 5., 9.],
    ])

    X_std = standardize_features(X)
    assert X_std.shape == X.shape
    assert np.allclose(X_std.mean(axis=0), 0, atol=1e-10)

    X_row_norm = normalize_rows_by_sum(X)
    assert X_row_norm.shape == X.shape
    assert np.allclose(X_row_norm.sum(axis=1), 1)

    X_minmax = minmax_rows(X)
    assert X_minmax.shape == X.shape
    assert np.allclose(X_minmax.min(axis=1), 0)
    assert np.allclose(X_minmax.max(axis=1), 1)

    # без keepdims для (n,d) с n != d: сумма по строкам (n,)
    # не может broadcast-иться к (n,d) по строкам -> падает
    try:
        normalize_rows_by_sum_no_keepdims(X)
        assert False, "ожидалась ValueError из-за несовпадения форм при broadcasting"
    except ValueError:
        pass

    # квадратная матрица (5,5): n == d, поэтому (n,) молча broadcast-ится
    # по СТОЛБЦАМ вместо строк - результат в форме X.shape, но считает не то,
    # что задумано, и никакой ошибки не будет
    X_square = np.array([
        [1., 2., 3., 4., 5.],
        [10., 20., 30., 40., 50.],
        [2., 2., 2., 2., 2.],
        [100., 90., 80., 70., 60.],
        [0., 1., 0., 1., 0.],
    ])

    correct = minmax_rows(X_square)
    silently_wrong = minmax_rows_no_keepdims(X_square)

    # без keepdims строки не приводятся к [0,1] так, как задумано
    assert not np.allclose(correct, silently_wrong)
    # но форма результата всё равно (5,5) - ошибка не бросается в глаза
    assert silently_wrong.shape == X_square.shape

    print("OK")
```

---

### 6. → Идеи 7, 8

**Рассуждение + код.** Для каждой пары назови итоговую форму или скажи, что упадёт: `(8,1,6)+(7,1)`, `(3,)+(4,)`, `(5,4)+(4,)`, `(5,4)+(5,)`, `(2,3)+(3,2)`. Для падающих напиши минимальную правку через `None` и скажи, что операция теперь означает. Затем напиши функцию `broadcast_cost(shape_a, shape_b, itemsize)`, которая возвращает форму результата и его размер в байтах (реализуй правила сам, не через `np.broadcast_shapes`).

```python
# - (8,1,6)+(7,1) = (8, 7, 6) смысл операции сложно мне понять
# - (3,)+(4,) упадет исправить через a[:, None] таблица всех пар
# - (5,4)+(4,) = (5, 4) вектор прибавляется к каждой строке
# - (5,4)+(5,) упадет, потому что правые оси не равны правка скорее всего b[:, None]
# - (2,3)+(3,2) упадет правки либо a[:, :, None] + b либо a[None, :, :]

def broadcast_cost(shape_a: tuple, shape_b: tuple, itemsize) -> tuple:

    ndim = max(len(shape_a), len(shape_b))

    shape_a = (1,) * (ndim - len(shape_a)) + shape_a
    shape_b = (1,) * (ndim - len(shape_b)) + shape_b

    result_shape = []

    for dim_a, dim_b in zip(shape_a, shape_b):
        if dim_a == dim_b:
            result_shape.append(dim_a)
        elif dim_a == 1:
            result_shape.append(dim_b)
        elif dim_b == 1:
            result_shape.append(dim_a)
        else:
            raise ValueError(
                 f"shapes {shape_a} and {shape_b} are not broadcastable"
            )

    result_shape = tuple(result_shape)

    num_elements = 1
    for dim in result_shape:
        num_elements *= dim

    num_bytes = num_elements * itemsize

    return result_shape, num_bytes
```

---

### 7. → Идея 9

**Код руками.** Для `a = np.arange(12).reshape(3,4)` выведи `a.ravel()`, `a.T.ravel()`, `a.reshape(-1)`, `a.T.reshape(-1)`, `a.flatten()` и для каждого проверь `np.shares_memory(a, ...)`. Объясни, почему ровно один из первых четырёх — копия. Затем напиши `to_c_contiguous(a)`, которая копирует только если это действительно нужно.

```python
import numpy as np

a = np.arange(12).reshape(3,4)

a_raveled = a.ravel() #view
a_transposed_raveled = a.T.ravel() #copy
a_reshaped = a.reshape(-1) #view
a_transposed_reshaped = a.T.reshape(-1) #copy
a_flattened = a.flatten() #copy

print(a_raveled)
print(f'{np.shares_memory(a, a_raveled)} that a_raveled shares memory with a')
print(a_transposed_raveled)
print(f'{np.shares_memory(a, a_transposed_raveled)} that a_transposed_raveled shares memory with a')
print(a_reshaped)
print(f'{np.shares_memory(a, a_reshaped)} that a_reshaped shares memory with a')
print(a_transposed_reshaped)
print(f'{np.shares_memory(a, a_transposed_reshaped)} that a_transposed_reshaped shares memory with a')
print(a_flattened)
print(f'{np.shares_memory(a, a_flattened)} that a_flattened shares memory with a')


def to_c_contiguous(a):
    if a.flags.c_contiguous is True:
        return a
    else:
        return np.ascontiguousarray(a)


if __name__ == '__main__':
    assert np.shares_memory(a, a_raveled)
    assert not np.shares_memory(a, a_transposed_raveled)
    assert np.shares_memory(a, a_reshaped)
    assert not np.shares_memory(a, a_transposed_reshaped)
    assert not np.shares_memory(a, a_flattened)

    b = to_c_contiguous(a)
    assert np.shares_memory(a, b)

    c = a.T
    d = to_c_contiguous(c)
    assert not np.shares_memory(c, d)
    assert d.flags.c_contiguous
    assert np.array_equal(d, c)

    print('all tests passed')
```

---

### 8. → Идея 10

**Код руками + провокация.** `img = np.full((4,4), 250, dtype=np.uint8)`. Напиши «увеличение яркости на 10» наивно и объясни результат числами. Затем реализуй корректный `brighten(img, delta)`, который насыщает значения в `[0,255]` и работает при отрицательном `delta` тоже.

```python
import numpy as np

img = np.full((4,4), 250, dtype=np.uint8)

# print(img)
# print(img + np.uint8(10))

def brighten(img: np.ndarray, delta: int) -> np.ndarray:
    result = img.astype(np.int16) + delta
    result = np.clip(result, 0, 255)
    return result.astype(np.uint8)


if __name__ == '__main__':
    naive = img + np.uint8(10)
    assert np.all(naive == 4)  # 250+10=260, заворачивается по модулю 256

    bright = brighten(img, 10)
    assert np.all(bright == 255)  # 250+10=260, клипается к 255
    assert bright.dtype == np.uint8

    dark = brighten(img, -300)
    assert np.all(dark == 0)  # 250-300 < 0, клипается к 0
    assert dark.dtype == np.uint8

    mid = brighten(img, -10)
    assert np.all(mid == 240)  # 250-10=240, в границах, без клипа

    print('all tests passed')
```

---

### 9. → Идея 11

**Каверзная.** `a = np.arange(5)` (int64). Что произойдёт в каждом случае и почему: `a + 0.5`, `a += 0.5`, `a[:] = a + 0.5`, `a = a + 0.5`? Расставь по степени опасности и объясни, почему падающий вариант безопаснее непадающего.

```python
a = np.arange(5)  # int64

a + 0.5        # ничего не происходит: результат (float64) вычисляется и теряется, никуда не присваивается
a += 0.5       # падает: TypeError, нельзя записать float в существующий int64-буфер (same_kind casting)
a[:] = a + 0.5 # НЕ падает: правая часть float [0.5,1.5,2.5,3.5,4.5], но пишется в int-буфер a,
               # дробная часть обрезается -> a остаётся [0,1,2,3,4], то есть "не изменился"
a = a + 0.5    # нормально работает: создаётся новый float64-массив, имя a теперь указывает на него

Опасность по возрастанию:
1. a + 0.5        — безобиден (просто бесполезен)
4. a = a + 0.5     — безопасен, ожидаемое поведение
2. a += 0.5        — падает громко и сразу, легко заметить и починить
3. a[:] = a + 0.5  — самый опасный: не падает, молча теряет данные (дробную часть),
                     баг может всплыть через сотни строк пайплайна, а не в месте ошибки
```

---

### 10. → Идея 12

**Код руками.** Дана скалярная функция: `x**2`, если `x > 0`, иначе `-x`. Напиши три «векторизации»: через `np.vectorize`, через list comprehension, через маски/`np.where`. Замерь все три на миллионе элементов. Объясни, почему первая почти не быстрее второй. Отдельно: когда `np.where` — плохой выбор и чем его заменить?

```python
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
```

---

## Задачи 11–19 — решений пока нет

Задача 11 обсуждалась устно (подход: `X @ w + b`, `pred = raw > 0`), но код не написан и в репозитории отсутствует.

Задачи 12, 13, 14, 15, 16, 17, 18, 19 не начаты.
