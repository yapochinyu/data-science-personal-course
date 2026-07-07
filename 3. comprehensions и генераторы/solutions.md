### Задача 1

Дан список `temps = [21.5, -3.0, 15.2, -7.8, 30.1, 0.0]`. Напиши тремя отдельными comprehension: (а) только положительные температуры; (б) все температуры, где отрицательные заменены на 0; (в) квадраты только положительных температур. Затем для каждого скажи вслух: это фильтр, преобразование или комбинация?

```python
temps = [21.5, -3.0, 15.2, -7.8, 30.1, 0.0]

print([temp for temp in temps if temp > 0])

print([temp if temp >= 0 else 0 for temp in temps])

print([temp**2 if temp >= 0 else temp for temp in temps])
```

### Задача 3

Не запуская, скажи тип каждого выражения и обоснуй:

```python
a = [x*2 for x in range(3)]
b = {x*2 for x in range(3)}
c = {x: x*2 for x in range(3)}
d = (x*2 for x in range(3))
```

Затем напиши одну строку, которая даёт из тех же данных именно кортеж `(0, 2, 4)`.

```python
a = [x*2 for x in range(3)]
b = {x*2 for x in range(3)}
c = {x: x*2 for x in range(3)}
d = (x*2 for x in range(3))
e = tuple(x*2 for x in range(3))

print(a)
print(b)
print(c)
print(d)
print(e)
```

### Задача 4

Дана матрица `matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]`. Одним comprehension: (а) разверни её в плоский список; (б) собери плоский список только чётных элементов. Затем напиши эквивалент пункта (а) обычными вложенными циклами и проговори правило порядка `for`.

```python
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

lst = [x for row in matrix for x in row]

even = [x for row in matrix for x in row if x % 2 == 0]

lst_2 = []

for row in matrix:
    for x in row:
        lst_2.append(x)


print(lst)
print(even)
print(lst_2)
```

### Задача 6

Напиши генератор-функцию `fibonacci()`, отдающую числа Фибоначчи бесконечно. Затем кодом получи первые 10 чисел (подумай, чем — цикл с `next`, `islice`?). Устно ответь: почему это принципиально невозможно сделать списком и что именно хранит генератор между вызовами?

```python
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a+b

gen = fibonacci()

print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))
```

### Задача 7

Найди баг и исправь двумя способами:

```python
def stats(data):
    squares = (x**2 for x in data)
    total = sum(squares)
    maximum = max(squares)
    return total, maximum

print(stats([1, 2, 3]))
```

Что именно произойдёт при запуске и почему баг называют «тихим»?

```python
# def stats(data):
#     squares = (x**2 for x in data)
#     total = sum(squares)
#     maximum = max(squares)
#     return total, maximum

# print(stats([1, 2, 3]))

# Вызовет ValueError, потому что у нас исчерпан генератор на второй раз


def stats(data):
    squares = [x**2 for x in data]
    total = sum(squares)
    maximum = max(squares)
    return total, maximum

print(stats([1, 2, 3]))

def stats_gen(data):
    total = sum(x**2 for x in data)
    maximum = max(x**2 for x in data) 
    return total, maximum

print(stats_gen([1, 2, 3]))
```

### Задача 8

Напиши функцию `first_anomaly(values, threshold)`, которая возвращает первое значение больше `threshold`, а если такого нет — `None`. Требования: без цикла `for` с `break`, через генераторное выражение и `next`; данные могут быть огромными, лишние элементы вычисляться не должны.

```python
def first_anomaly(values, threshold):
    return next((v for v in values if v > threshold), None)


if __name__ == '__main__':
    assert first_anomaly([1, 2, 3, 10, 4], 5) == 10
    assert first_anomaly([1, 2, 3], 5) is None
    assert first_anomaly([], 5) is None
    assert first_anomaly([-1, -2, -3], -5) == -1
    assert first_anomaly([5, 5, 5], 5) is None

    def spy():
        calls = []
        for v in [1, 2, 100, 3, 200]:
            calls.append(v)
            yield v

    gen = spy()
    result = first_anomaly(gen, 50)
    assert result == 100
    assert next(gen) == 3, "генератор не должен вычислять элементы после найденного"

    print('OK')
```

### Задача 9

Напиши генератор-функцию `batch_generator(dataset, batch_size)`, которая отдаёт данные батчами по `batch_size` элементов, включая последний неполный батч. `dataset` может быть любым итерируемым (в том числе другим генератором). Проверь себя: что вернёт `list(batch_generator(range(7), 3))`?

```python
def batch_generator(dataset, batch_size):
    batch = []
    for item in dataset:
        batch.append(item)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:
        yield batch

print(list(batch_generator(range(7), 3)))
```

### Задача 10

Файл `metrics.csv` на 50 ГБ, в память не влезает. Формат строки: `timestamp,user_id,latency`. Напиши функцию `mean_latency(filepath)`, считающую среднее значение третьего столбца с O(1) памяти. Устно объясни, какой объект здесь уже является генератором «из коробки».

```python
def mean_latency(filepath):
    summ, count = 0, 0
    with open(filepath, 'r') as f:
        next(f) # для строки заголовка
        for line in f:
            summ += float(line.split(',')[2])
            count += 1
    return summ / count
```

### Задача 11

Построй ленивый пайплайн из трёх генераторов-функций: `parse(lines)` — превращает строки в float; `drop_outliers(values, low, high)` — отбрасывает значения вне диапазона; `scale(values, factor)` — умножает на factor. Соедини их в цепочку над `raw = ['1.5', '100.0', '2.5', '-50.0', '3.0']` и материализуй результат. Устно: в какой момент реально происходят вычисления?

```python
raw = ['1.5', '100.0', '2.5', '-50.0', '3.0']

def parse(lines):
    for line in lines:
        yield float(line)

def drop_outliers(values, low, high):
    for value in values:
        if low < value < high:
            yield value

def scale(values, factor):
    for value in values:
        yield value * factor

pipeline = scale(drop_outliers(parse(raw), 0, 10), 2)

print(list(pipeline))
```

### Задача 12

Напиши генератор-функцию `flatten(nested)`, разворачивающую произвольно вложенные списки в плоский поток: `list(flatten([1, [2, [3, 4]], 5])) → [1, 2, 3, 4, 5]`. Используй `yield from`. Затем объясни, чем `yield from flatten(item)` отличается от просто `flatten(item)` внутри цикла.

```python
def flatten(nested):
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item


print(list(flatten([1, [2, [3, 4]], 5])))
```
