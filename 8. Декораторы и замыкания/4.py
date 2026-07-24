def make_counter():
    count = 0
    def inc():
        nonlocal count
        count += 1
        return count

    def reset():
        nonlocal count
        count = 0
        return count
    
    return inc, reset

def make_logger():
    lines = []
    def log(msg):
        lines.append(msg)
        return len(lines)
    return log


if __name__ == '__main__':
    inc, reset = make_counter()
    assert inc() == 1
    assert inc() == 2
    assert inc() == 3
    assert reset() == 0
    assert inc() == 1

    inc2, reset2 = make_counter()
    assert inc2() == 1
    assert inc() == 2  # независим от inc2

    log = make_logger()
    assert log('a') == 1
    assert log('b') == 2
    assert log('c') == 3

    print('all tests passed')