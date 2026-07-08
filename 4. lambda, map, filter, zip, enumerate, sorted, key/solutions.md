# Решения — тема 4 (lambda, map, filter, zip, enumerate, sorted, key)

### Задача 1

Дан список `products = [{'name': 'milk', 'price': 80, 'qty': 3}, {'name': 'bread', 'price': 45, 'qty': 10}, {'name': 'cheese', 'price': 450, 'qty': 1}]`. Напиши: (а) сортировку по цене по возрастанию; (б) сортировку по суммарной стоимости позиции (`price * qty`) по убыванию; (в) товар с максимальной ценой — одной строкой без сортировки.

```python
def sort_by_price(products):
    return sorted(products, key=lambda x: x['price'])


def sort_by_total_value_desc(products):
    return sorted(products, key=lambda x: x['price'] * x['qty'], reverse=True)


def most_expensive(products):
    return max(products, key=lambda x: x['price'])


if __name__ == '__main__':
    products = [
        {'name': 'milk', 'price': 80, 'qty': 3},
        {'name': 'bread', 'price': 45, 'qty': 10},
        {'name': 'cheese', 'price': 450, 'qty': 1}
    ]

    assert sort_by_price(products) == [
        {'name': 'bread', 'price': 45, 'qty': 10},
        {'name': 'milk', 'price': 80, 'qty': 3},
        {'name': 'cheese', 'price': 450, 'qty': 1}
    ]
    assert sort_by_total_value_desc(products) == [
        {'name': 'bread', 'price': 45, 'qty': 10},
        {'name': 'cheese', 'price': 450, 'qty': 1},
        {'name': 'milk', 'price': 80, 'qty': 3}
    ]
    assert most_expensive(products) == {'name': 'cheese', 'price': 450, 'qty': 1}

    print(sort_by_price(products))
    print(sort_by_total_value_desc(products))
    print(most_expensive(products))
```

### Задача 3

Джун пишет:

```python
def top_scores(scores, n):
    sorted_scores = scores.sort(reverse=True)
    return sorted_scores[:n]
```

Вызов `top_scores([3, 1, 2], 2)` падает. С какой ошибкой и почему? Исправь двумя способами: (а) без мутации входного списка, (б) с мутацией, но корректно. Какой вариант правильнее для функции и почему (связь с темой ссылок)?

```python
def top_scores(scores, n):
    scores.sort(reverse=True)
    return scores[:n]


def top_scores_no_rewrite(scores, n):
    return sorted(scores, reverse=True)[:n]


if __name__ == '__main__':
    assert top_scores([3, 1, 2], 2) == [3, 2]
    assert top_scores_no_rewrite([3, 1, 2], 2) == [3, 2]
    assert top_scores_no_rewrite([], 2) == []
    assert top_scores_no_rewrite([5], 3) == [5]

    print(top_scores([3, 1, 2], 2))
    print(top_scores_no_rewrite([3, 1, 2], 2))

    # вариант без переписывания исходного списка логичнее,
    # потому что функция не должна преобразовывать исходные данные,
    # если также возвращает и результат,
    # либо одно, либо другое, оба варианта не нужны.
```

### Задача 4

Дан список строк из файла: `raw = ['1.5', '2.7', 'NaN', '3.1', '', '4.0']`. Через `map`/`filter` (без comprehension): (а) убери пустые строки и `'NaN'`; (б) преобразуй оставшееся во float; (в) посчитай сумму. Затем перепиши то же самое одним comprehension и скажи, какой вариант выбрал бы в проде и почему.

```python
def sum_valid(raw):
    data = filter(lambda x: x and x != 'NaN', raw)
    return sum(map(float, data))


def sum_valid_generator(raw):
    return sum(float(x) for x in raw if x and x != 'NaN')


if __name__ == '__main__':
    raw = ['1.5', '2.7', 'NaN', '3.1', '', '4.0']

    assert sum_valid(raw) == 11.3
    assert sum_valid_generator(raw) == 11.3
    assert sum_valid([]) == 0
    assert sum_valid(['NaN', '']) == 0

    print(sum_valid(raw))
    print(sum_valid_generator(raw))
```

### Задача 6

`y_true = [1, 0, 1, 1, 0, 1, 1]`, `y_pred = [1, 0, 0, 1]` (предсказания оборвались из-за бага). Напиши `accuracy(y_true, y_pred)` через `zip` — что она вернёт на этих данных и в чём коварство? Затем перепиши так, чтобы при разных длинах функция бросала `ValueError`.

```python
y_true = [1, 0, 1, 1, 0, 1, 1]
y_pred = [1, 0, 0, 1]

def accuracy(y_true, y_pred):
    try:
        result = sum(t == p for t, p in zip(y_true, y_pred, strict=True)) / len(y_true)
        return result
    except ValueError:
        print('длина не совпадает')
        return None


print(accuracy(y_true, y_pred))

if __name__ == '__main__':
    assert accuracy([1, 0, 1, 1, 0, 1, 1][:4], y_pred) == 1.0
    assert accuracy([1, 1, 1, 1], [0, 0, 0, 0]) == 0.0
    assert accuracy([1, 0, 1, 0], [1, 0, 0, 0]) == 0.75
    assert accuracy(y_true, y_pred) is None
    print('all tests passed')
```

### Задача 7

Дана матрица оценок студентов по предметам: `grades = [[5, 4, 3], [4, 4, 5], [3, 5, 4]]` (строка — студент, столбец — предмет). Одной-двумя строками посчитай средний балл **по каждому предмету**. Объясни, что делает `*` и почему без него не работает.

```python
grades = [
    [5, 4, 3], 
    [4, 4, 5], 
    [3, 5, 4]
    ]


mean_by_subject = [sum(col) / len(col) for col in zip(*grades)]
print(mean_by_subject)
```

### Задача 8

Дан список лоссов по батчам: `losses = [0.9, 0.7, 0.72, 0.5, 0.55, 0.3]`. Напиши функцию `spikes(losses)`, возвращающую список номеров батчей (нумерация с 1), где лосс **вырос** относительно предыдущего батча. Без `range(len(...))`. Подумай, что здесь зипуется с чем.

```python
losses = [0.9, 0.7, 0.72, 0.5, 0.55, 0.3]

def spikes(losses):
    spikes = []
    for i, loss in enumerate(losses):
        if i == 0:
            pass
        elif loss > losses[i - 1]:
            spikes.append(i)
    return spikes

print(spikes(losses))
```

### Задача 10

Дан список слов. Верни их отсортированными по правилу: сначала по длине по возрастанию, при равной длине — по алфавиту. `words = ['pear', 'fig', 'apple', 'kiwi', 'date']`. Одна строка. Затем усложнение: по длине по **убыванию**, при равной — по алфавиту по возрастанию.

```python
words = ['pear', 'fig', 'apple', 'kiwi', 'date']

print(sorted(words, key=lambda x: (len(x), x.lower())))
print(sorted(words, key=lambda x: (-len(x), x.lower())))
```

### Задача 11

Список сотрудников: `staff = [{'name': 'Anna', 'dept': 'ML', 'salary': 200}, {'name': 'Boris', 'dept': 'Data', 'salary': 180}, {'name': 'Vera', 'dept': 'ML', 'salary': 220}, {'name': 'Gleb', 'dept': 'Data', 'salary': 180}]`. Отсортируй: по `dept` по алфавиту по возрастанию, внутри отдела — по `salary` по **убыванию**, при равной зарплате — по `name` по возрастанию. Минус для строки `dept` не сработал бы, но здесь он и не нужен — а вот придумай решение и вторым способом: через несколько проходов сортировки.

```python
staff = [
    {'name': 'Anna', 'dept': 'ML', 'salary': 200},
    {'name': 'Boris', 'dept': 'Data', 'salary': 180},
    {'name': 'Vera', 'dept': 'ML', 'salary': 220},
    {'name': 'Gleb', 'dept': 'Data', 'salary': 180}
    ]


print(sorted(staff, key=lambda s: (s['dept'], -s['salary'], s['name'])))

print(sorted(sorted(sorted(staff, key=lambda x : x['name']), key=lambda x : x['salary'], reverse=True), key=lambda x : x['dept']))
```

### Задача 13

`names = ['Alice', 'Bob', 'Charlie', 'David']`, `scores = [88, 95, 88, 70]`. Верни имена в порядке убывания балла; при равных баллах — в алфавитном порядке. Одной цепочкой `zip` + `sorted` + comprehension. Проверь себя: где в итоге окажутся Alice и Charlie и почему именно в таком порядке?

```python
names = ['Alice', 'Bob', 'Charlie', 'David']
scores = [88, 95, 88, 70]

print([name for name, score in sorted(zip(names, scores), key=lambda x: (-x[1], x[0]))])
```

### Задача 14

Напиши функцию `make_scaler(factor)`, которая возвращает функцию, умножающую аргумент на `factor`. Затем: `doubler = make_scaler(2); tripler = make_scaler(3)` — примени обе через `map` к `[1, 2, 3]`. Устно объясни, почему `doubler` «помнит» свой factor после завершения `make_scaler` (назови термин).

```python
def make_scaler(factor):
    return lambda x : x * factor

doubler = make_scaler(2)

tripler = make_scaler(3)

print(list(map(doubler, [1, 2, 3])))
print(list(map(tripler, [1, 2, 3])))


def make_scaler_with_def(factor):
    def scaler(x):
        return x * factor
    return scaler

doubler_def = make_scaler_with_def(2)

tripler_def = make_scaler_with_def(3)

print(list(map(doubler_def, [1, 2, 3])))
print(list(map(tripler_def, [1, 2, 3])))


if __name__ == '__main__':
    assert list(map(doubler_def, [1, 2, 3])) == [2, 4, 6]
    assert list(map(tripler_def, [1, 2, 3])) == [3, 6, 9]
    print("ok")
```

### Задача 15

Перед тобой код коллеги:

```python
get_price = lambda item: item['price']
prices = list(map(get_price, items))
expensive = list(filter(lambda item: item['price'] > 1000, items))
names = list(map(lambda item: item['name'], expensive))
```

Назови минимум три претензии ревьюера к этому коду и перепиши всё в два выражения идиоматичным Python.

```python
items = [
    {'name': 'laptop', 'price': 1500},
    {'name': 'mouse', 'price': 25},
    {'name': 'monitor', 'price': 1200},
    {'name': 'keyboard', 'price': 60},
    {'name': 'server', 'price': 5000},
]

get_price = lambda item: item['price'] # непонятно, зачем этот промежуточный шаг присваивания имени функции
prices = list(map(get_price, items)) # 
expensive = list(filter(lambda item: item['price'] > 1000, items)) # почему бы тогда здесь не использовать get_price
names = list(map(lambda item: item['name'], expensive)) # очень дорогое использование инструментов, проще и читаемее через comprehensions
print(names)

names = [item['name'] for item in items if item['price'] > 1000]
print(names)
```