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