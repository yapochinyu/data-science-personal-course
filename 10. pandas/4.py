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
