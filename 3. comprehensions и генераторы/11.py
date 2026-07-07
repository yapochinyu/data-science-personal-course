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