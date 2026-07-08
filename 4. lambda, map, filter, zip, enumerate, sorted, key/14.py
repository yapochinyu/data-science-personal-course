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