# Решения — Тема 6. ООП: классы, наследование, инкапсуляция, полиморфизм, dunder-методы

### Задача 1 (идеи 1, 2, 3) — код руками (базовый скелет)

Напиши класс `BankAccount`: конструктор принимает `owner` и начальный `balance` (по умолчанию 0); методы `deposit(amount)` и `withdraw(amount)` — снятие при недостатке средств бросает `ValueError`; метод `__repr__` вида `BankAccount(owner='Anna', balance=150)`. Создай два счёта и покажи, что операции с одним не влияют на другой. Затем вызови `deposit` двумя эквивалентными способами: через точку и через класс.

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError
        else:
            self.balance -= amount

    def __repr__(self):
        return f'BankAccount(owner={self.owner!r}, balance={self.balance})'


if __name__ == '__main__':
    bank_anna = BankAccount('Anna', 150)
    bank_boris = BankAccount('Boris', 100)

    # операции с одним счётом не влияют на другой
    bank_anna.deposit(50)
    assert bank_anna.balance == 200
    assert bank_boris.balance == 100

    bank_boris.withdraw(30)
    assert bank_boris.balance == 70
    assert bank_anna.balance == 200

    # deposit через точку и через класс — эквивалентны
    bank_boris.deposit(100)
    assert bank_boris.balance == 170

    BankAccount.deposit(bank_anna, 100)
    assert bank_anna.balance == 300

    # withdraw при недостатке средств бросает ValueError
    try:
        bank_boris.withdraw(10_000)
        assert False, 'ожидался ValueError'
    except ValueError:
        pass

    assert repr(bank_anna) == "BankAccount(owner='Anna', balance=300)"

    print('OK')
```

### Задача 4 (идея 4) — код руками

Напиши класс `Experiment`, где: `total_experiments` — счётчик всех созданных экспериментов (атрибут класса, инкрементируется в `__init__` правильно — через класс, не через self), а `metrics` — список метрик конкретного эксперимента (у каждого свой). Создай три эксперимента, добавь метрики в один, покажи, что счётчик общий (=3), а метрики — независимые.

```python
class Experiment:
    total_experiments = 0

    def __init__(self, metrics=None):
        Experiment.total_experiments += 1
        if metrics is None:
            self.metrics = []
        else:
            self.metrics = metrics


if __name__ == '__main__':
    e1 = Experiment()
    e2 = Experiment()
    e3 = Experiment(['acc'])

    # счётчик общий на всех
    assert Experiment.total_experiments == 3
    assert e1.total_experiments == 3
    assert e2.total_experiments == 3
    assert e3.total_experiments == 3

    # metrics — независимые у каждого экземпляра
    e1.metrics.append('loss')
    assert e1.metrics == ['loss']
    assert e2.metrics == []
    assert e3.metrics == ['acc']

    # дефолтный список не расшарен между экземплярами (мина изменяемого дефолта)
    e4 = Experiment()
    assert e4.metrics == []

    print('OK')
```

### Задача 5 (идея 6) — рассуждение + провокация

Интервьюер: «Сделай атрибут `__balance` приватным через два подчёркивания — теперь его точно нельзя изменить снаружи, верно?» Опровергни кодом: покажи, как прочитать и изменить `__balance` снаружи. Затем объясни, для чего name mangling нужен НА САМОМ ДЕЛЕ, с примером из наследования.

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.__balance = balance

    @property
    def balance(self):
        return self.__balance

    def deposit(self, amount):
        self.__balance += amount

    def withdraw(self, amount):
        if amount > self.__balance:
            raise ValueError
        else:
            self.__balance -= amount

    def __repr__(self):
        return f'BankAccount(owner={self.owner!r}, balance={self.__balance})'


if __name__ == '__main__':
    bank_anna = BankAccount('Anna', 150)
    bank_boris = BankAccount('Boris', 100)

    # операции с одним счётом не влияют на другой
    bank_anna.deposit(50)
    assert bank_anna.balance == 200
    assert bank_boris.balance == 100

    bank_boris.withdraw(30)
    assert bank_boris.balance == 70
    assert bank_anna.balance == 200

    # deposit через точку и через класс — эквивалентны
    bank_boris.deposit(100)
    assert bank_boris.balance == 170

    BankAccount.deposit(bank_anna, 100)
    assert bank_anna.balance == 300

    # withdraw при недостатке средств бросает ValueError
    try:
        bank_boris.withdraw(10_000)
        assert False, 'ожидался ValueError'
    except ValueError:
        pass

    assert repr(bank_anna) == "BankAccount(owner='Anna', balance=300)"

    # __balance — приватный через name mangling, напрямую снаружи недоступен
    try:
        bank_anna.__balance
        assert False, 'ожидался AttributeError'
    except AttributeError:
        pass

    # но доступен через переименованное имя (mangling, а не защита доступа)
    assert bank_anna._BankAccount__balance == 300

    print('OK')
```

### Задача 6 (идея 7) — код руками

Напиши класс `Dataset` с приватным по соглашению атрибутом `_data` (список чисел): (а) `size` — read-only property, возвращающая длину; (б) property `data` с сеттером, который принимает только непустой список, иначе `ValueError`; (в) вычисляемая property `mean`, считающая среднее на лету. Продемонстрируй, что `ds.size = 10` падает с ошибкой.

```python
class Dataset:
    def __init__(self, _data=None):
        self.data = data
    
    @property
    def size(self):
        return len(self._data)
    
    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, value):
        if not value:
            raise ValueError('data не может быть пустым')
        self._data = value
    
    @property
    def mean(self):
        return sum(self._data) / len(self._data)
```

### Задача 7 (идеи 8, 9) — код руками (типовая задача собеса)

Есть базовый класс:

```python
class BaseModel:
    def __init__(self, name):
        self.name = name
        self.is_fitted = False

    def fit(self, X, y):
        self.is_fitted = True

    def predict(self, X):
        if not self.is_fitted:
            raise RuntimeError('Model is not fitted')
        return [0] * len(X)
```

Напиши наследника `MeanModel(BaseModel)`: конструктор дополнительно принимает `round_digits`; `fit` вычисляет и сохраняет среднее `y` (и не забывает пометить модель обученной — переиспользуй родительский fit, не копируй `self.is_fitted = True`); `predict` возвращает список из среднего (округлённого) длиной `len(X)`, сохраняя родительскую проверку обученности.

```python
class BaseModel:
    def __init__(self, name):
        self.name = name
        self.is_fitted = False

    def fit(self, X, y):
        self.is_fitted = True

    def _check_fitted(self):
        if not self.is_fitted:
            raise RuntimeError('Model is not fitted')
        
    def predict(self, X):
        self._check_fitted()
        return [0] * len(X)
    

class MeanModel(BaseModel):
    def __init__(self, name, round_digits):
        super().__init__(name)
        self.round_digits = round_digits

    def fit(self, X, y):
        super().fit(X, y)
        self.mean_ = sum(y) / len(y)

    def predict(self, X):
        self._check_fitted()
        value = round(self.mean_, self.round_digits)
        return [value] * len(X)


if __name__ == '__main__':
    base = BaseModel('base')
    try:
        base.predict([1, 2, 3])
        assert False, 'expected RuntimeError before fit'
    except RuntimeError:
        pass

    base.fit([1, 2], [1, 2])
    assert base.is_fitted is True
    assert base.predict([1, 2, 3]) == [0, 0, 0]

    model = MeanModel('mean', round_digits=2)
    assert model.name == 'mean'
    assert model.round_digits == 2
    assert model.is_fitted is False

    try:
        model.predict([1, 2, 3])
        assert False, 'expected RuntimeError before fit'
    except RuntimeError:
        pass

    model.fit([0, 0, 0], [1, 2, 3])
    assert model.is_fitted is True
    assert model.mean_ == 2.0, 'mean_ должен считаться по y, а не по X'

    preds = model.predict([10, 20, 30, 40])
    assert preds == [2.0, 2.0, 2.0, 2.0]
    assert len(preds) == 4

    model2 = MeanModel('mean2', round_digits=3)
    model2.fit([0], [1, 2, 4])
    preds2 = model2.predict([1, 1])
    assert preds2 == [round(7 / 3, 3), round(7 / 3, 3)]

    print('all tests passed')
```

### Задача 10 (идеи 11, 12) — код руками (ML-сценарий)

Напиши два класса без общего родителя: `ConstantModel` (в `fit` запоминает самый частый класс из y, в `predict` возвращает его для всех объектов) и `ThresholdModel(threshold)` (fit ничего не делает, predict возвращает 1 там, где `x > threshold`, иначе 0 — X это список чисел). Затем напиши функцию `evaluate(models, X, y)`, которая обучает каждую модель и возвращает dict `{имя_класса: accuracy}`. Устно объясни, почему функция работает с обоими классами и как называется этот принцип.

```python
class ConstantModel:
    def fit(self, X, y):
        self._moda = max(set(y), key=y.count)

    def predict(self, X):
        return [self._moda] * len(X)

class ThresholdModel:
    def __init__(self, threshold=0.5):
        self.threshold = threshold
    

    def fit(self, X, y):
        pass
    
    def predict(self, X):
        return [1 if x > self.threshold else 0 for x in X]
    


def evaluate(models, X, y):
    models_dict = {}
    for model in models:
        model.fit(X, y)
        preds = model.predict(X)
        accuracy = sum(true == pred for true, pred in zip(y, preds)) / len(y)
        models_dict[type(model).__name__] = accuracy
    return models_dict


if __name__ == '__main__':
    y = [0, 0, 1, 0, 1]
    X_const = [None] * len(y)

    cm = ConstantModel()
    cm.fit(X_const, y)
    assert cm._moda == 0
    assert cm.predict(X_const) == [0, 0, 0, 0, 0]

    X_thr = [0.1, 0.9, 0.6, 0.2, 0.8]
    tm = ThresholdModel(threshold=0.5)
    tm.fit(X_thr, y)
    assert tm.predict(X_thr) == [0, 1, 1, 0, 1]

    tm_default = ThresholdModel()
    assert tm_default.threshold == 0.5

    results = evaluate([ConstantModel(), ThresholdModel(threshold=0.5)], X_thr, y)
    assert set(results.keys()) == {'ConstantModel', 'ThresholdModel'}
    assert results['ConstantModel'] == 3 / 5
    assert results['ThresholdModel'] == 4 / 5

    print('all tests passed')
```

### Задача 11 (идеи 13, 15) — код руками (классика: Vector)

Напиши класс `Vector` для n-мерного вектора (координаты — в списке): `__init__(*coords)`, `__repr__`, `__eq__` (покоординатное равенство, с чужими типами — `NotImplemented`), `__add__` (покоординатная сумма, при разных длинах — `ValueError`), `__mul__` (умножение на скаляр), `__len__` (размерность). Продемонстрируй все операции. Бонус устно: почему `v * 2` работает, а `2 * v` упадёт, и какой dunder это чинит?

```python
class Vector:
    def __init__(self, *coords):
        self.coords = list(coords)

    def __repr__(self):
        return f'Vector {self.coords}'
    
    def __eq__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented
        return self.coords == other.coords

    def __add__(self, other):
        if len(self.coords) != len(other.coords):
            raise ValueError('vectors must have the same length')
        else:
            return Vector(*[x + y for x, y in zip(self.coords, other.coords)])
        
    def __mul__(self, scalar):
        return Vector(*[x * scalar for x in self.coords])

    def __len__(self):
        return len(self.coords)


if __name__ == '__main__':
    v1 = Vector(1, 2, 3)
    v2 = Vector(1, 2, 3)
    v3 = Vector(4, 5, 6)

    assert repr(v1) == 'Vector [1, 2, 3]'
    assert v1 == v2
    assert v1 != v3
    assert v1 != 'not a vector'
    assert (v1 == 'not a vector') is False

    assert v1 + v3 == Vector(5, 7, 9)
    try:
        v1 + Vector(1, 2)
        assert False, 'expected ValueError for mismatched lengths'
    except ValueError:
        pass

    assert v1 * 2 == Vector(2, 4, 6)
    assert len(v1) == 3
    assert len(Vector(1, 2, 3, 4, 5)) == 5

    print('all tests passed')
```

### Задача 12 (идеи 13, 16) — код руками (PyTorch-паттерн без PyTorch)

Напиши класс `CSVDataset`, имитирующий PyTorch Dataset: конструктор принимает список строк вида `'1.5,0'` (фичи и метка через запятую); `__len__` — число примеров; `__getitem__(i)` — кортеж `(float_фича, int_метка)`. Затем напиши функцию `simple_loader(dataset, batch_size)` — генератор (из темы генераторов!), который выдаёт батчи, используя ТОЛЬКО `len(dataset)` и `dataset[i]`. Объясни, почему loader не зависит от того, как датасет хранит данные.

```python
class CSVDataset:
    def __init__(self, lines):
        self.lines = lines

    def __len__(self):
        return len(self.lines)
    
    def __getitem__(self, i):
        return float(self.lines[i].split(',')[0]), int(self.lines[i].split(',')[1])
    


def simple_loader(dataset, batch_size):
    for i in range(0, len(dataset), batch_size):
        end = min(i + batch_size, len(dataset))
        batch = [dataset[x] for x in range(i, end)]
        yield batch


if __name__ == '__main__':
    ds = CSVDataset(['1.5,0', '2.5,1', '3.5,0', '4.5,1', '5.5,0'])

    assert len(ds) == 5
    assert ds[0] == (1.5, 0)
    assert ds[4] == (5.5, 0)

    batches = list(simple_loader(ds, 2))
    assert batches == [
        [(1.5, 0), (2.5, 1)],
        [(3.5, 0), (4.5, 1)],
        [(5.5, 0)],
    ]

    # batch_size делит длину без остатка — нет неполного батча
    batches_exact = list(simple_loader(ds, 5))
    assert len(batches_exact) == 1
    assert len(batches_exact[0]) == 5

    # batch_size больше длины датасета — один неполный батч
    batches_big = list(simple_loader(ds, 100))
    assert batches_big == [[(1.5, 0), (2.5, 1), (3.5, 0), (4.5, 1), (5.5, 0)]]

    # для for достаточно __len__/__getitem__, __iter__ не нужен
    assert [x for x in ds] == [(1.5, 0), (2.5, 1), (3.5, 0), (4.5, 1), (5.5, 0)]

    print('all tests passed')
```

### Задача 14 (идея 15) — код руками + каверза

Дан класс:

```python
class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
```

(а) Сейчас `User(1, 'Anna') == User(1, 'Anna')` даёт False — почему? Добавь `__eq__` (равенство по user_id). (б) После этого выполни `{User(1, 'Anna'): 'admin'}` — что произойдёт и почему? Свяжи с темой хеширования из первой темы. (в) Почини, добавив согласованный `__hash__`.

```python
class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name\
        
    def __eq__(self, other):
        if not isinstance(other, User):
            return NotImplemented
        return self.name == other.name and self.user_id == other.user_id
    
    def __hash__(self):
        return hash(self.user_id)


if __name__ == '__main__':
    u1 = User(1, 'Anna')
    u2 = User(1, 'Anna')
    u3 = User(2, 'Boris')

    # равенство по полям, а не по identity
    assert u1 == u2
    assert u1 is not u2
    assert u1 != u3
    assert u1 != 'not a user'

    # объект хешируем — можно класть в set/dict
    users = {u1: 'admin'}
    assert users[u2] == 'admin'  # u2 == u1 и hash(u2) == hash(u1)

    s = {u1, u2, u3}
    assert len(s) == 2  # u1 и u2 равны -> в set один элемент

    assert hash(u1) == hash(u2)
    assert hash(u1) == hash(User(1, 'другое_имя'))  # хеш зависит только от user_id

    print('all tests passed')
```

### Задача 15 (идея 13) — код руками (`__call__`, мост к DL)

Напиши класс `Scaler`: конструктор принимает `mean` и `std`; объект вызывается как функция — `scaler(x)` возвращает `(x - mean) / std`; метод `fit(data)` вычисляет mean и std по списку и возвращает `self` (чтобы работала цепочка `Scaler().fit(data)(x)`). Продемонстрируй цепочку. Устно: какой dunder делает объект вызываемым и где ты уже видел этот паттерн в PyTorch?

```python
class Scaler:
    def __init__(self, mean_value=0, std_value=1):
        self.mean_value = mean_value
        self.std_value = std_value

    def fit(self, data):
        self.mean_value = sum(data) / len(data)
        variance = sum((x - self.mean_value) ** 2 for x in data) / len(data)
        self.std_value = variance ** 0.5
        return self

    def __call__(self, x):
        return (x - self.mean_value) / self.std_value


if __name__ == '__main__':
    data = [2, 4, 4, 4, 5, 5, 7, 9]

    scaler = Scaler().fit(data)

    assert scaler.mean_value == 5.0
    assert round(scaler.std_value, 4) == 2.0

    assert scaler(5) == 0.0
    assert round(scaler(2), 4) == -1.5
    assert round(scaler(9), 4) == 2.0

    # цепочка Scaler().fit(data)(x) работает благодаря return self
    assert round(Scaler().fit(data)(9), 4) == 2.0

    # разные объекты не делят состояние
    other = Scaler().fit([0, 0, 0, 10])
    assert other.mean_value == 2.5
    assert scaler.mean_value != other.mean_value

    print('all tests passed')
```

### Задача 16 (идея 17) — код руками + рассуждение

Есть класс:

```python
class TrainConfig:
    def __init__(self, lr, epochs, batch_size):
        self.lr = lr
        self.epochs = epochs
        self.batch_size = batch_size
```

Перепиши его через `@dataclass` со значениями по умолчанию (`lr=0.01`, `epochs=10`, `batch_size=32`). Продемонстрируй, что бесплатно появились `__repr__` и `__eq__`. Каверза: добавь в dataclass поле `callbacks: list = []` — что скажет Python и почему? Как правильно задать изменяемый дефолт в dataclass?

```python
from dataclasses import dataclass, field


@dataclass
class TrainConfig:
    lr: float = 0.01
    epochs: int = 10
    batch_size: int = 32
    callbacks: list = field(default_factory=list)


if __name__ == '__main__':
    c1 = TrainConfig()

    # __repr__ появился бесплатно
    assert repr(c1) == 'TrainConfig(lr=0.01, epochs=10, batch_size=32, callbacks=[])'

    # __eq__ появился бесплатно: сравнение по полям, а не по identity
    c2 = TrainConfig()
    assert c1 == c2
    assert c1 is not c2

    c3 = TrainConfig(lr=0.1)
    assert c1 != c3

    # default_factory даёт каждому объекту свой независимый список
    c1.callbacks.append('early_stop')
    assert c1.callbacks == ['early_stop']
    assert c2.callbacks == []  # не затронут

    # обычные позиционные/именованные аргументы конструктора работают как обычно
    c4 = TrainConfig(0.05, 20, 64)
    assert c4.lr == 0.05
    assert c4.epochs == 20
    assert c4.batch_size == 64

    print('all tests passed')
```
