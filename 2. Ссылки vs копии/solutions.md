# Решения — тема 2 (Ссылки vs копии)

### Задача 3 (идея 5) — провокация + код

Джун написал: `sorted_scores = scores.sort()`, а потом упал с `TypeError: 'NoneType' object is not iterable`. Объясни, почему в `sorted_scores` оказался `None`, и напиши два корректных варианта: (а) когда исходный список можно менять, (б) когда исходный нужно сохранить нетронутым.

```python
scores = [1, 22, 3, 41, 5]

sorted_scores = sorted(scores)

scores.sort()

print(sorted_scores)

print(scores)


scores.append(6)

print(sorted_scores)

print(scores)
```

### Задача 4 (идея 6) — код руками

Есть список конфигов экспериментов: `base_configs = [{'lr': 0.01, 'epochs': 10}, {'lr': 0.1, 'epochs': 5}]`. Напиши функцию `clone_and_bump_lr(configs, factor)`, которая возвращает независимую копию списка, где все `lr` умножены на `factor`, а исходный `base_configs` гарантированно не меняется. Сначала напиши «наивно неправильный» вариант через `configs.copy()` и покажи, где он ломается, потом правильный.

```python
import copy

base_configs = [{'lr': 0.01, 'epochs': 10}, {'lr': 0.1, 'epochs': 5}]


def clone_and_bump_lr_wrong(configs, factor):
    bumped_configs = configs.copy()
    for config in bumped_configs:
        config['lr'] *= factor
    return bumped_configs


def clone_and_bump_lr(configs, factor):

    bumped_configs = copy.deepcopy(configs)
    for config in bumped_configs:
        config['lr'] *= factor
    return bumped_configs


if __name__ == '__main__':
    wrong_result = clone_and_bump_lr_wrong(base_configs, 10)
    assert base_configs == [{'lr': 0.1, 'epochs': 10}, {'lr': 1.0, 'epochs': 5}]
    assert wrong_result[0] is base_configs[0]

    base_configs = [{'lr': 0.01, 'epochs': 10}, {'lr': 0.1, 'epochs': 5}]
    result = clone_and_bump_lr(base_configs, 10)
    assert result == [{'lr': 0.1, 'epochs': 10}, {'lr': 1.0, 'epochs': 5}]
    assert base_configs == [{'lr': 0.01, 'epochs': 10}, {'lr': 0.1, 'epochs': 5}]
    assert result[0] is not base_configs[0]

    print("все тесты прошли")
```

### Задача 6 (идея 8) — код руками + провокация

Напиши функцию `zeros_matrix(rows, cols)`, возвращающую матрицу нулей как список списков, так чтобы `m[0][0] = 1` менял ровно одну ячейку. Затем объясни: почему `[[0] * cols] * rows` — баг, а сам внутренний `[0] * cols` — нет, хотя оператор `*` в обоих случаях «копирует одно и то же».

```python
def zeros_matrix(rows, cols):
    return [[0] * cols for _ in range(rows)]


if __name__ == '__main__':
    m = zeros_matrix(3, 3)
    assert m == [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    m[0][0] = 1
    assert m == [[1, 0, 0], [0, 0, 0], [0, 0, 0]], "изменилась не одна ячейка"
    assert m[1] == [0, 0, 0], "строки не должны быть общим объектом"

    assert m[0] is not m[1], "[[0]*cols]*rows дал бы общий объект для всех строк"

    assert zeros_matrix(0, 5) == []
    assert zeros_matrix(2, 0) == [[], []]

    print("все тесты прошли")
```

### Задача 7 (идея 9) — код руками

Дана функция накопления метрик:

```python
def log_metric(value, history=[]):
    history.append(value)
    return history
```

Предскажи вывод `print(log_metric(0.9)); print(log_metric(0.8))`, объясни механизм через `__defaults__` и перепиши функцию правильно. Бонус: приведи случай, когда такое поведение используют намеренно.

```python
def log_metric(value, history=None):
    if history == None:
        history = []
    history.append(value)
    return history
```

### Задача 8 (идея 10) — код руками

Функция препроцессинга:

```python
def add_bias(features):
    features.append('bias')
    return features
```

Покажи кодом, какой баг возникнет при двух вызовах `add_bias(X)` на одном `X`, и перепиши функцию так, чтобы она не мутировала вход. Затем скажи одним предложением, почему в ML-пайплайнах мутация входа особенно опасна.

```python
def add_bias(features):
    return features + ['bias']
```

### Задача 9 (идея 11) — код руками + провокация

Не запуская, предскажи содержимое `a` после каждого блока и объясни разницу:

```python
import numpy as np
a = np.arange(5)
b = a[1:4]
b[0] = 99
# что в a?

a = np.arange(5)
c = a[a > 2]
c[0] = 99
# что в a?
```

Затем напиши, как безопасно взять срез numpy-массива для последующей мутации.

```python
import numpy as np
a = np.arange(5)
b = a[1:4]
b[0] = 99
# что в a?
# в а изменится элемент под индексом 1
print(a)


a = np.arange(5)
c = a[a > 2]
c[0] = 99
# что в a?
# здесь а не изменится
print(a)


a = np.arange(5)
b = a[1:4].copy()
b[0] = 99

print(a)
```

### Задача 10 (идея 12) — код руками

Есть `df` с колонками `age`, `salary`. Нужно взять пользователей старше 30 и добавить им колонку `segment='senior'`, не изменив исходный `df` и не поймав `SettingWithCopyWarning`. Напиши «опасный» вариант, который даёт предупреждение, и корректный. Объясни, откуда pandas вообще берёт это предупреждение.

```python
import pandas as pd

df = pd.DataFrame({
    'age': [25, 35, 45, 22, 51],
    'salary': [50000, 65000, 80000, 42000, 90000],
})


def add_senior_segment(df):
    df2 = df[df['age'] > 30].copy()
    df2['segment'] = 'senior'
    return df2
```

### Задача 13 (идея 7) — код руками (сложная)

Напиши свою функцию `my_deepcopy(obj)` для структур из вложенных `list` и `dict` (значения — списки, словари или неизменяемые типы). Требование: она должна корректно обработать циклическую ссылку (`a = [1]; a.append(a)`) без `RecursionError`. Объясни роль `memo`.

```python
def my_deepcopy(obj, memo=None):
    if memo is None:
        memo = {}
    
    obj_id = id(obj)
    if obj_id in memo:
        return memo[obj_id]
    
    if isinstance(obj, (list)):
        copy = []
        memo[obj_id] = copy
        for item in obj:
            copy.append(my_deepcopy(item, memo))
        return copy
    elif isinstance(obj, dict):
        copy = {}
        memo[obj_id] = copy
        for key, value in obj.items():
            copy[key] = my_deepcopy(value, memo)
        return copy
    else:
        return obj
```