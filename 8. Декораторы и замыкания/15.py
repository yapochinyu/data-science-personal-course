from functools import wraps

def rate_limited(max_calls):
    def decorator(func):
        calls = 0

        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal calls
            if calls >= max_calls:
                raise RuntimeError('лимит вызовов исчерпан')
            calls += 1
            return func(*args, **kwargs)
        return wrapper
    return decorator


@rate_limited(2)
def greet(name):
    return f'привет, {name}'


@rate_limited(1)
def shout(text):
    return text.upper()


if __name__ == '__main__':
    assert greet('a') == 'привет, a'
    assert greet('b') == 'привет, b'
    try:
        greet('c')
        assert False, 'ожидался RuntimeError'
    except RuntimeError:
        pass

    # независимость: у shout свой счётчик, greet его уже исчерпал
    assert shout('ok') == 'OK'
    try:
        shout('again')
        assert False, 'ожидался RuntimeError'
    except RuntimeError:
        pass

    assert greet.__name__ == 'greet'

    print('OK')