import numpy as np

def is_view(base: np.ndarray, piece: np.ndarray) -> bool:
    if base is piece.base: # улучшение return base is piece.base
        return True
    else:
        return False


if __name__ == '__main__':
    a = np.array([10, 20, 30, 40, 50])

    assert is_view(a, a[1:4])
    assert is_view(a, a[::2])
    assert not is_view(a, a[[0, 3, 1]])
    assert not is_view(a, a[a > 15])

    print('all tests passed')
