# Решения — тема 10 (pandas)

### Задача 1

Напиши две функции, вычисляющие поэлементную сумму двух последовательностей длины `n`:

```python
def sum_loop(a: list[int], b: list[int]) -> list[int]: ...
def sum_vec(a: np.ndarray, b: np.ndarray) -> np.ndarray: ...
```

`sum_loop` — чистый Python со списками. `sum_vec` — numpy, ровно одна операция над массивами. Затем измерь обе на `n = 1_000_000` через `time.perf_counter` и выведи отношение времён.

Пример на 3 элементах: `a=[1,2,3]`, `b=[10,20,30]` → обе возвращают `[11,22,33]`.

Ограничение: в `sum_vec` запрещены `for`, `map`, списковые включения и `np.vectorize`.

```python
import numpy as np
from time import perf_counter

def sum_loop(a: list[int], b: list[int]) -> list[int]:
    if len(a) == len(b):
        result = []
        for i in range(len(a)):
            result.append(a[i] + b[i])
        return result
    else:
        raise ValueError("Массивы разной длины, поэлементной суммы не выйдет")

def sum_vec(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    if len(a) == len(b):
        return a + b
    else:
        raise ValueError("Массивы разной длины, поэлементной суммы не выйдет")

if __name__ == '__main__':
    a = [1, 2, 3]
    b = [10, 20, 30]
    assert sum_loop(a, b) == [11, 22, 33]
    assert np.array_equal(sum_vec(np.array(a), np.array(b)), [11, 22, 33])
    try:
        sum_loop([1, 2], [1])
        assert False, "ожидался ValueError"
    except ValueError:
        pass
    try:
        sum_vec(np.array([1, 2]), np.array([1]))
        assert False, "ожидался ValueError"
    except ValueError:
        pass


    n = 1_000_000
    lst1 = list(range(n))
    arr1 = np.arange(n)
    lst2 = list(range(n))
    arr2 = np.arange(n)

    res_lst = sum_loop(lst1, lst2)
    start_time_lst = perf_counter()
    res_lst = sum_loop(lst1, lst2)
    end_time_lst = perf_counter()
    execution_time_lst = end_time_lst - start_time_lst

    res_arr = sum_vec(arr1, arr2)
    start_time_arr = perf_counter()
    res_arr = sum_vec(arr1, arr2)
    end_time_arr = perf_counter()
    execution_time_arr = end_time_arr - start_time_arr


    print('lst:', execution_time_lst)
    print('array:', execution_time_arr)
    print(execution_time_lst / execution_time_arr)
```

### Задача 2

Дан список из миллиона небольших целых. Напиши функцию, которая возвращает кортеж из двух чисел: сколько байт занимает этот список вместе со всеми объектами внутри, и сколько байт занимает эквивалентный `np.array` с `dtype=int64`.

```python
def compare_size(values: list[int]) -> tuple[int, int]: ...
```

Пример на 5 элементах `[10,20,30,40,50]`: результат вида `(отчёт_для_списка, 40)` — второе число это `5 × 8`.

Ограничение: размер списка считать честно — сам массив указателей плюс объекты, на которые они указывают, каждый уникальный объект учитывать один раз.

```python
import numpy as np
import sys

def sizely(values: list[int]) -> tuple[int, int]:

    list_size = sys.getsizeof(values)

    seen = set()
    for x in values:
        if id(x) not in seen:
            list_size += sys.getsizeof(x)
            seen.add(id(x))

    array_size = np.array(values, dtype='int64').nbytes

    return list_size, array_size


if __name__ == '__main__':
    # пример из задачи: массив должен весить ровно 5 * 8 = 40 байт
    l_size, a_size = sizely([10, 20, 30, 40, 50])
    assert a_size == 40

    # маленькие целые кешируются CPython (-5..256) — один и тот же объект
    # переиспользуется много раз, значит должен учитываться один раз
    values_small = [1] * 1000
    l_size_small, _ = sizely(values_small)
    expected = sys.getsizeof(values_small) + sys.getsizeof(1)
    assert l_size_small == expected

    # наивный (неправильный) подсчёт умножил бы размер числа на 1000 —
    # честный результат должен быть заметно меньше
    naive = sys.getsizeof(values_small) + sys.getsizeof(1) * 1000
    assert l_size_small < naive

    # большие целые вне диапазона кеша обычно не переиспользуются между
    # собой, поэтому размер должен расти почти пропорционально их числу
    values_big = [1_000_000 + i for i in range(1000)]
    l_size_big, _ = sizely(values_big)
    assert l_size_big > sys.getsizeof(values_big) + sys.getsizeof(1_000_000) * 500

    print("all tests passed")
```

### Задача 3

Напиши функцию, которая по массиву и способу взятия куска говорит, получилось представление или копия — не полагаясь на изменение данных.

```python
def is_view(base: np.ndarray, piece: np.ndarray) -> bool: ...
```

Проверь её на четырёх случаях для `a = np.array([10,20,30,40,50])`: `a[1:4]`, `a[::2]`, `a[[0,3,1]]`, `a[a > 15]`.

Ожидаемый вывод: `True, True, False, False`.

Ограничение: нельзя записывать в `piece` и смотреть, изменился ли `base`.

```python
import numpy as np

def is_view(base: np.ndarray, piece: np.ndarray) -> bool:
    if base is piece.base: # улучшение return base is piece.base
        return True
    else:
        return False


if __name__ == '__main__':
    a = np.array([10, 20, 30, 40, 50])

    assert is_view(a, a[1:4])
    assert is_view(a, a[::2])
    assert not is_view(a, a[[0, 3, 1]])
    assert not is_view(a, a[a > 15])

    print('all tests passed')
```

### Задача 4

Реализуй руками упрощённый поиск по метке, чтобы показать, почему он не зависит от размера данных.

```python
class LabeledArray:
    def __init__(self, values: list, labels: list): ...
    def get(self, label) -> object: ...      # значение по метке
    def probes(self) -> int: ...              # сколько сравнений меток сделал последний get
```

Внутри — массив корзин фиксированного размера 8, раскладка по остатку от деления хеша на 8, коллизии хранятся списком внутри корзины. `probes` считает, сколько раз пришлось сравнить метку на равенство.

Пример: метки `['Аня','Боря','Вика']`, значения `[100,250,90]`. `get('Боря')` → `250`, `probes()` → небольшое число (1 или 2), а не 3.

Ограничение: нельзя использовать встроенный словарь как хранилище меток; перебор всех меток подряд не засчитывается.

```python
import numpy as np

class LabeledArray:
    def __init__(self, values: list, labels: list):
        self.values = values
        self.labels = labels
        self.counter = 0
        self.buckets = [[] for _ in range(8)]
        for num, label in enumerate(labels):
            self.buckets[hash(label) % 8].append((label, num))
            

    def get(self, label):
        self.counter = 0
        for name, num in self.buckets[hash(label) % 8]:
            if name == label:
                self.counter += 1
                return self.values[num]
            else:
                self.counter += 1
        else: 
            raise ValueError("No item in LabeledArray")
        

    def probes(self):
        return self.counter


if __name__ == '__main__':
    arr = LabeledArray([100, 250, 90], ['Аня', 'Боря', 'Вика'])

    assert arr.get('Аня') == 100
    assert arr.get('Боря') == 250
    assert arr.get('Вика') == 90

    # сравнений минимум 1 и не больше числа меток
    arr.get('Боря')
    assert 1 <= arr.probes() <= 3

    # счётчик обнуляется на каждом get
    arr.get('Аня')
    first = arr.probes()
    arr.get('Аня')
    assert arr.probes() == first

    # отсутствующая метка даёт исключение
    try:
        arr.get('Гриша')
        assert False, 'ожидалось исключение'
    except ValueError:
        pass

    # числовые метки
    years = LabeledArray(['a', 'b', 'c'], [2020, 2021, 2022])
    assert years.get(2021) == 'b'

    # большой массив: все метки находятся, значения верные
    n = 1000
    big = LabeledArray(list(range(n)), [str(i) for i in range(n)])
    for i in range(0, n, 37):
        assert big.get(str(i)) == i
        assert 1 <= big.probes() <= n

    print('all tests passed')
```

### Задача 5

Дана таблица на 200 000 строк с 30 столбцами `float64`. Напиши две функции, добавляющие 50 новых числовых столбцов, и сравни их по времени:

```python
def add_cols_loop(df: pd.DataFrame, new: dict[str, np.ndarray]) -> pd.DataFrame: ...
def add_cols_once(df: pd.DataFrame, new: dict[str, np.ndarray]) -> pd.DataFrame: ...
```

`new` — словарь «имя столбца → массив нужной длины». Первая функция добавляет их по одному, вторая — за один раз. Обе возвращают таблицу с теми же 30 + 50 столбцами.

Пример на маленьком: `df` 3×2, `new = {'c': [1,2,3], 'd': [4,5,6]}` → обе дают таблицу 3×4 с одинаковым содержимым.

Дополнительно: выведи количество блоков в результате каждой функции.

```python
import pandas as pd
import numpy as np
from time import perf_counter

def add_cols_loop(df: pd.DataFrame, new: dict[str, np.ndarray]) -> pd.DataFrame: 
    df = df.copy()
    for col_name, col_values in new.items():
        df[col_name] = col_values
    return df

def add_cols_once(df: pd.DataFrame, new: dict[str, np.ndarray]) -> pd.DataFrame: 
    return pd.concat([df, pd.DataFrame(new)], axis = 1)

if __name__ == '__main__':
    rng = np.random.default_rng(0)
    n_rows = 200_000
    df = pd.DataFrame(rng.random((n_rows, 30)), columns=[f'c{i}' for i in range(30)])
    new = {f'new{i}': rng.random(n_rows) for i in range(50)}
    original = df.copy()

    res_loop = add_cols_loop(df, new)
    res_once = add_cols_once(df, new)

    # форма и имена столбцов
    assert res_loop.shape == (n_rows, 80)
    assert res_once.shape == (n_rows, 80)
    assert list(res_loop.columns) == list(res_once.columns)
    assert list(res_once.columns) == list(df.columns) + list(new)

    # обе функции дают одинаковую таблицу
    assert res_loop.equals(res_once)

    # значения новых столбцов на месте
    for name, values in new.items():
        assert np.array_equal(res_once[name].to_numpy(), values)

    # исходная таблица не изменена
    assert df.equals(original)
    assert df.shape == (n_rows, 30)

    # замер времени
    start = perf_counter()
    add_cols_loop(df, new)
    t_loop = perf_counter() - start

    start = perf_counter()
    add_cols_once(df, new)
    t_once = perf_counter() - start

    print(f'loop: {t_loop:.4f} s, once: {t_once:.4f} s')

    print('all tests passed')
```

### Задача 6

Напиши функцию, которая показывает, при каком значении целочисленный идентификатор портится после появления пропуска.

```python
def find_breaking_id(start: int) -> int: ...
```

Она должна найти наименьшее целое `x >= start`, для которого `pd.Series([x, None]).iloc[0]` даёт значение, не равное `x`. Вернуть это `x`.

Пример: `find_breaking_id(9_007_199_254_740_990)` → число в районе `9_007_199_254_740_993`.

Дополнительно: покажи, что с `dtype='Int64'` то же самое не ломается ни при каком `x` до `10**18`.

```python
import pandas as pd


def find_breaking_id(start: int) -> int:
    x = start
    while int(pd.Series([x, None]).iloc[0]) == x:
        x += 1
    return x


if __name__ == '__main__':
    limit = 2 ** 53

    # пример из условия: граница рядом с 2**53 + 1
    res = find_breaking_id(9_007_199_254_740_990)
    assert res == limit + 1

    # если начать выше границы, портится сразу или через пару шагов
    assert find_breaking_id(limit + 1) == limit + 1

    # найденное число действительно портится, предыдущее — нет
    assert int(pd.Series([res, None]).iloc[0]) != res
    assert int(pd.Series([res - 1, None]).iloc[0]) == res - 1

    # до границы всё точно
    assert int(pd.Series([limit, None]).iloc[0]) == limit
    assert int(pd.Series([12345, None]).iloc[0]) == 12345

    # Int64 не ломается ни на границе, ни выше
    for x in [limit - 1, limit, limit + 1, limit + 3, 10 ** 15, 10 ** 17, 10 ** 18]:
        s = pd.Series([x, None], dtype='Int64')
        assert s.iloc[0] == x
        assert s.isna().iloc[1]

    print('all tests passed')
```

### Задача 7

Дана Series `s = pd.Series([1.0, np.nan, 5.0])`. Коллега утверждает: «`s[s > 2]` возвращает одну строку со значением 5.0 — значит pandas правильно понял, что пропуск не больше двойки».

Напиши функцию, которая демонстрирует, что это рассуждение неверно, и покажи, как выглядит честный ответ:

```python
def compare_semantics() -> dict: ...
```

Возвращает словарь с четырьмя ключами: `'nan_gt'`, `'nan_lt'`, `'nan_eq'` — результаты сравнения пропуска с двойкой тремя операторами, и `'na_gt'` — результат того же сравнения для `pd.Series([1, pd.NA, 5], dtype='Int64')`.

Ожидаемый вид: первые три — одинаковые булевы значения, четвёртый — объект, отличающийся от них обоих.

Дополнительно: покажи, что `s2[s2 > 2]` для `Int64`-версии падает, и приведи два варианта явного решения.

```python
import pandas as pd
import numpy as np


def compare_semantics() -> dict:
    s = pd.Series([1.0, np.nan, 5.0])
    s2 = pd.Series([1, pd.NA, 5], dtype='Int64')
    
    nan_gt = s > 2
    nan_lt = s < 2
    nan_eq = s == 2
    na_gt = s2 > 2

    result = {
        'nan_gt':nan_gt[1],
        'nan_lt':nan_lt[1],
        'nan_eq':nan_eq[1],
        'na_gt':na_gt[1]
    }
    
    return result

if __name__ == '__main__':
    dictionary = compare_semantics()
    print(dictionary)
    assert dictionary['nan_gt'] == False
    assert dictionary['nan_lt'] == False
    assert dictionary['nan_eq'] == False
    assert dictionary['na_gt'] is pd.NA
    
```

### Задача 8

Напиши функцию, которая по двум Series предсказывает, сколько NaN будет в результате их сложения — **не выполняя сложение**.

```python
def predict_nans(a: pd.Series, b: pd.Series) -> int: ...
```

Пример: `a` с индексом `['x','y','z']`, `b` с индексом `['y','z','w']`, пропусков в данных нет → результат `2`.  
Второй пример: `a` с индексом `['x','y']`, `b` с индексом `['p','q']` → результат `4`.

Ограничение: запрещено вызывать `a + b`, `align`, `reindex`. Считать, что в самих данных пропусков нет.

```python
import pandas as pd
import numpy as np

def predict_nans(a: pd.Series, b: pd.Series) -> int:
    return len(set(a.index) ^ set(b.index))


def predict_nans_dup(a: pd.Series, b: pd.Series) -> int:
    # сколько раз встречается каждая метка у каждого операнда
    count_a = a.index.value_counts()
    count_b = b.index.value_counts()

    # NaN дают строки только по меткам, которых нет у второго операнда;
    # такая метка даёт столько строк, сколько раз она повторяется у своего операнда
    only_a = count_a[~count_a.index.isin(count_b.index)].sum()
    only_b = count_b[~count_b.index.isin(count_a.index)].sum()
    return int(only_a + only_b)


if __name__ == '__main__':
    s = pd.Series([1, 2, 3], index=['x', 'y', 'z'])
    s2 = pd.Series([1, 2, 3], index=['y', 'z', 'v'])
    assert predict_nans(s, s2) == 2

    s3 = pd.Series([1, 2], index=['x', 'y'])
    s4 = pd.Series([1, 2], index=['p', 'q'])
    assert predict_nans(s3, s4) == 4

    # дубликаты: метка 'y' повторяется дважды и есть только у первого операнда
    d1 = pd.Series([1, 2], index=['y', 'y'])
    d2 = pd.Series([10], index=['z'])
    assert predict_nans(d1, d2) == 2      # старая версия ошибается
    assert predict_nans_dup(d1, d2) == 3

    # общая метка с дубликатами даёт строки без NaN (2 × 3 = 6), в ответ не входит
    d3 = pd.Series([1, 2], index=['x', 'x'])
    d4 = pd.Series([1, 2, 3], index=['x', 'x', 'x'])
    assert predict_nans_dup(d3, d4) == 0

    # без дубликатов даёт то же, что и простая версия
    assert predict_nans_dup(s, s2) == 2
    assert predict_nans_dup(s3, s4) == 4

    # сверка с настоящим сложением на случайных данных с дубликатами
    rng = np.random.default_rng(0)
    labels = list('abcdef')
    for _ in range(200):
        a = pd.Series(1.0, index=rng.choice(labels, size=rng.integers(1, 8)))
        b = pd.Series(1.0, index=rng.choice(labels, size=rng.integers(1, 8)))
        assert predict_nans_dup(a, b) == (a + b).isna().sum()
```

### Задача 9

Дана таблица:

```python
df = pd.DataFrame({'v': [10, 20, 30, 40, 50, 60]}, index=[10, 20, 30, 40, 50, 60])
```

Для каждого из выражений ниже заранее, **до запуска**, запиши, что получится, — а потом проверь:

```python
df.loc[20]        df.iloc[20]
df.loc[10:30]     df.iloc[10:30]
df.loc[0]         df.iloc[0]
df[10:30]         df[0:2]
```

Оформи это как функцию:

```python
def probe() -> list[str]: ...
```

Она возвращает список из восьми строк: для каждого выражения либо текстовое описание результата, либо имя пойманной ошибки.

Пример элемента вывода: `"loc[20] -> 20"` или `"iloc[20] -> IndexError"`.

Ограничение: каждое выражение обернуть так, чтобы падение одного не мешало проверить остальные.

```python
import pandas as pd

df = pd.DataFrame({'v': [10, 20, 30, 40, 50, 60]}, index=[10, 20, 30, 40, 50, 60])


def describe(result) -> str:
    if isinstance(result, pd.DataFrame):
        return f"{len(result)} rows {result['v'].tolist()}"
    if isinstance(result, pd.Series):
        return str(result['v'])
    return str(result)


def probe() -> list[str]:
    cases = [
        ('loc[20]', lambda: df.loc[20]),
        ('iloc[20]', lambda: df.iloc[20]),
        ('loc[10:30]', lambda: df.loc[10:30]),
        ('iloc[10:30]', lambda: df.iloc[10:30]),
        ('loc[0]', lambda: df.loc[0]),
        ('iloc[0]', lambda: df.iloc[0]),
        ('[10:30]', lambda: df[10:30]),
        ('[0:2]', lambda: df[0:2]),
    ]
    out = []
    for name, expr in cases:
        try:
            out.append(f"{name} -> {describe(expr())}")
        except Exception as e:
            out.append(f"{name} -> {type(e).__name__}")
    return out


if __name__ == "__main__":
    res = probe()
    for line in res:
        print(line)
    assert res == [
        "loc[20] -> 20",
        "iloc[20] -> IndexError",
        "loc[10:30] -> 3 rows [10, 20, 30]",
        "iloc[10:30] -> 0 rows []",
        "loc[0] -> KeyError",
        "iloc[0] -> 10",
        "[10:30] -> 0 rows []",
        "[0:2] -> 2 rows [10, 20]",
    ]
```

### Задача 10

Реализуй `groupby(...).sum()` руками, повторив оба прохода из механизма pandas.

```python
def group_sum(keys: list, values: list[float]) -> dict: ...
```

Возвращает словарь «уникальный ключ → сумма». Внутри обязательно: первый проход даёт массив кодов и список уникальных ключей в порядке появления; второй проход идёт по значениям и кодам одновременно, прибавляя в массив-накопитель.

Пример: `keys=['B','A','B','C','A']`, `values=[10,20,5,7,3]` → `{'B':15, 'A':23, 'C':7}`.

Ограничения: сортировать ничего нельзя; нельзя собирать подсписки значений по группам; нельзя использовать `collections.defaultdict` как накопитель сумм — накопитель должен быть именно списком чисел, адресуемым по коду.

```python
def group_sum(keys: list, values: list[float]) -> dict:
    unique_keys = []
    codes = []
    for key in keys:
        if key in unique_keys:
            codes.append(unique_keys.index(key))
        else:
            unique_keys.append(key)
            codes.append(len(unique_keys) - 1)

    sums = [0] * len(unique_keys)

    for code, value in zip(codes, values):
        sums[code] += value
        
    return dict(zip(unique_keys, sums))


if __name__ == '__main__':
    assert group_sum(['B', 'A', 'B', 'C', 'A'], [10, 20, 5, 7, 3]) == {'B': 15, 'A': 23, 'C': 7}
```
