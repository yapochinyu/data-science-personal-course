import numpy as np

a = np.array([-5, 5, 10, 15, np.nan, 0, -1, 9, np.nan, 17, 7, 5])

if __name__ == '__main__':
    try:
        wrong_mask = (a > 0) and (a < 10) and not np.isnan(a)
        wrong_result = a[wrong_mask]
        assert False, "ожидалась ValueError на 'and' с массивом"
    except ValueError:
        pass

    mask = (a > 0) & (a < 10) & ~np.isnan(a)
    result = a[mask]
    assert np.array_equal(result, [5, 9, 7, 5])

    assert np.array_equal(~np.array([True, False]), [False, True])
    assert np.array_equal(~np.array([1, 0], dtype=np.int8), [-2, -1]) # побитовая инверсия на числах происходит в дополнительном коде

    print("OK")

