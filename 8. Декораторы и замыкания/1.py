def compose(*funcs):
    def inner(x):
        for func in funcs:
            x = func(x)
        return x
    return inner


if __name__ == '__main__':
    pipeline = compose(str.strip, str.lower, str.split)
    assert pipeline('  Hello WORLD  ') == ['hello', 'world']

    identity = compose()
    assert identity(42) == 42
    assert identity('abc') == 'abc'

    single = compose(str.upper)
    assert single('abc') == 'ABC'

    add_one = lambda x: x + 1
    double = lambda x: x * 2
    assert compose(add_one, double)(3) == 8  # (3+1)*2
    assert compose(double, add_one)(3) == 7  # (3*2)+1

    assert pipeline.__closure__[0].cell_contents == (str.strip, str.lower, str.split)

    print('all tests passed')