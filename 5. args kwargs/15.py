def pipe(data, *funcs, verbose=False, **common_kwargs):
    for func in funcs:
        if verbose:
            print(func.__name__)
        data = func(data, **common_kwargs)
    return data


if __name__ == '__main__':
    def add(x, factor=1):
        return x + factor

    def double(x, factor=1):
        return x * 2

    def mul_factor(x, factor=1):
        return x * factor

    assert pipe(1, add, double) == 4          # (1+1)*2 = 4
    assert pipe(1, add, add, factor=10) == 21  # 1+10+10

    result = pipe(2, mul_factor, verbose=True, factor=3)
    assert result == 6                         # 2*3

    assert pipe(5) == 5                        # без funcs

    print("all tests passed")