lines = ['0.91', '0.87', 'corrupt', '0.93', '', '1.2e-1', 'NaN?']

def parse_metrics(lines):
    values, errors = [], [] 
    for i, line in enumerate(lines, start=1):
        try:
            values.append(float(line))
        except ValueError as e:
            errors.append((i, str(e)))
    return values, errors

if __name__ == '__main__':
    values, errors = parse_metrics(lines)
    assert values == [0.91, 0.87, 0.93, 0.12]
    assert [i for i, _ in errors] == [2, 4, 6]
    assert len(errors) == 3

    values, errors = parse_metrics([])
    assert values == []
    assert errors == []

    values, errors = parse_metrics(['1', '2', '3'])
    assert values == [1.0, 2.0, 3.0]
    assert errors == []

    values, errors = parse_metrics(['abc'])
    assert values == []
    assert len(errors) == 1
    assert errors[0][0] == 0

    print('OK')

