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
