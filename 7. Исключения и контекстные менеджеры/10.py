from contextlib import contextmanager
import time
import random

@contextmanager
def Timer(name):
    start = time.time()
    state = {}
    try:
        yield state
    finally:
        state['elapsed'] = time.time() - start
        print(f'[{name}] {state["elapsed"]:.2f}')

@contextmanager
def temp_seed(seed):
    state = random.getstate()
    random.seed(seed)
    try:
        yield
    finally:
        random.setstate(state)


if __name__ == '__main__':
    with Timer('sleep') as t:
        time.sleep(0.05)
    assert t['elapsed'] >= 0.05

    try:
        with Timer('boom') as t2:
            raise ValueError('boom')
    except ValueError:
        pass
    else:
        assert False, 'исключение должно было пролететь дальше'
    assert t2['elapsed'] >= 0

    random.seed(123)
    before = random.getstate()
    with temp_seed(42):
        a = random.random()
    with temp_seed(42):
        b = random.random()
    assert a == b, 'одинаковый seed должен давать одинаковое число'
    assert random.getstate() == before, 'состояние генератора должно восстановиться'

    try:
        with temp_seed(1):
            raise ValueError('boom')
    except ValueError:
        pass
    else:
        assert False, 'исключение должно было пролететь дальше'
    assert random.getstate() == before, 'состояние должно восстановиться даже после исключения'

    print('OK')

