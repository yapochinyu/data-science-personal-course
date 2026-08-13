import numpy as np

def zero_negatives_inplase(arr: np.ndarray):
    arr[arr < 0] = 0
    return arr


def zero_negatives_copy(arr: np.ndarray):
    arr_copy = arr.copy()
    arr_copy[arr_copy < 0] = 0
    return arr_copy


if __name__ == '__main__':
    a = np.array([-3, 1, -2, 5, -1])
    result = zero_negatives_inplase(a)
    assert np.array_equal(a, [0, 1, 0, 5, 0])
    assert result is a

    a = np.array([-3, 1, -2, 5, -1])
    before = a.copy()
    result = zero_negatives_copy(a)
    assert np.array_equal(a, before)
    assert np.array_equal(result, [0, 1, 0, 5, 0])

    print("OK")
