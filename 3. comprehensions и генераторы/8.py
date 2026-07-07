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