import time

def fetch_with_retry(fetch_fn, max_attempts=3, delay=1.0):
    for attempt in range(max_attempts):
        try:
            return fetch_fn()
        except (ConnectionError, TimeoutError) as e:
            print(f'Попытка {attempt+1} не удалась {e}')
            if attempt == max_attempts - 1:
                raise
            time.sleep(delay)


if __name__ == '__main__':
    def always_ok():
        return 'data'

    assert fetch_with_retry(always_ok, delay=0) == 'data'

    calls = {'n': 0}
    def fails_twice_then_ok():
        calls['n'] += 1
        if calls['n'] <= 2:
            raise ConnectionError('no network')
        return 'data'

    assert fetch_with_retry(fails_twice_then_ok, max_attempts=3, delay=0) == 'data'
    assert calls['n'] == 3

    def always_fails():
        raise TimeoutError('timeout')

    try:
        fetch_with_retry(always_fails, max_attempts=3, delay=0)
    except TimeoutError:
        pass
    else:
        assert False, 'должно было перебросить исключение после исчерпания попыток'

    def raises_value_error():
        raise ValueError('bad data')

    try:
        fetch_with_retry(raises_value_error, max_attempts=3, delay=0)
    except ValueError:
        pass
    else:
        assert False, 'ValueError должен лететь наружу сразу, без retry'

    print('OK')
