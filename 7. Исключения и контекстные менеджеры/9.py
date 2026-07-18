import time

class Timer:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.start = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.time() - self.start
        print(f'[{self.name}] {self.elapsed:.2f}')
        return False


if __name__ == '__main__':
    with Timer('sleep') as t:
        time.sleep(0.05)
    assert t.elapsed >= 0.05
    assert isinstance(t.elapsed, float)

    try:
        with Timer('boom') as t2:
            raise ValueError('boom')
    except ValueError:
        pass
    else:
        assert False, 'исключение должно было пролететь дальше'
    assert t2.elapsed >= 0

    print('OK')
