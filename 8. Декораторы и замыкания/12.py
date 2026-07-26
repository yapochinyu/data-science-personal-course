from functools import wraps

def validate_range(low, high):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for arg in args:
                if isinstance(arg, (int, float)) and not low <= arg <= high:
                    raise ValueError(f'аргумент {arg} не в диапозоне {low}: {high}')
            result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator


@validate_range(0, 1)
def combine(p1, p2): 
    return p1 * p2


# combine = validate_range(0, 1)(combine)


if __name__ == '__main__':
    assert combine(0.5, 1) == 0.5
    assert combine(0, 1) == 0

    try:
        combine(2, 0.5)
        assert False, 'ожидался ValueError'
    except ValueError:
        pass

    print('OK')