import numpy as np


def standardize_features(X: np.ndarray) -> np.ndarray:
    # по каждому признаку (столбцу): вычесть среднее, поделить на std
    mean = X.mean(axis=0, keepdims=True)   # (1, d)
    std = X.std(axis=0, keepdims=True)     # (1, d)
    return (X - mean) / std


def normalize_rows_by_sum(X: np.ndarray) -> np.ndarray:
    # каждая строка делится на свою сумму
    row_sum = X.sum(axis=1, keepdims=True)  # (n, 1)
    return X / row_sum


def minmax_rows(X: np.ndarray) -> np.ndarray:
    # каждая строка приводится к [0, 1] по своему min/max
    row_min = X.min(axis=1, keepdims=True)  # (n, 1)
    row_max = X.max(axis=1, keepdims=True)  # (n, 1)
    return (X - row_min) / (row_max - row_min)


# те же три функции, но без keepdims - для демонстрации проблемы
def standardize_features_no_keepdims(X: np.ndarray) -> np.ndarray:
    mean = X.mean(axis=0)   # (d,)
    std = X.std(axis=0)     # (d,)
    return (X - mean) / std  # (d,) broadcast-ится к (n,d) по столбцам - совпадает с ожиданием


def normalize_rows_by_sum_no_keepdims(X: np.ndarray) -> np.ndarray:
    row_sum = X.sum(axis=1)  # (n,)
    return X / row_sum       # (n,) broadcast-ится к (n,d) по столбцам, а нужно было по строкам


def minmax_rows_no_keepdims(X: np.ndarray) -> np.ndarray:
    row_min = X.min(axis=1)  # (n,)
    row_max = X.max(axis=1)  # (n,)
    return (X - row_min) / (row_max - row_min)


if __name__ == '__main__':
    X = np.array([
        [1., 2., 3., 4.],
        [10., 20., 30., 40.],
        [5., 8., 5., 9.],
    ])

    X_std = standardize_features(X)
    assert X_std.shape == X.shape
    assert np.allclose(X_std.mean(axis=0), 0, atol=1e-10)

    X_row_norm = normalize_rows_by_sum(X)
    assert X_row_norm.shape == X.shape
    assert np.allclose(X_row_norm.sum(axis=1), 1)

    X_minmax = minmax_rows(X)
    assert X_minmax.shape == X.shape
    assert np.allclose(X_minmax.min(axis=1), 0)
    assert np.allclose(X_minmax.max(axis=1), 1)

    # без keepdims для (n,d) с n != d: сумма по строкам (n,)
    # не может broadcast-иться к (n,d) по строкам -> падает
    try:
        normalize_rows_by_sum_no_keepdims(X)
        assert False, "ожидалась ValueError из-за несовпадения форм при broadcasting"
    except ValueError:
        pass

    # квадратная матрица (5,5): n == d, поэтому (n,) молча broadcast-ится
    # по СТОЛБЦАМ вместо строк - результат в форме X.shape, но считает не то,
    # что задумано, и никакой ошибки не будет
    X_square = np.array([
        [1., 2., 3., 4., 5.],
        [10., 20., 30., 40., 50.],
        [2., 2., 2., 2., 2.],
        [100., 90., 80., 70., 60.],
        [0., 1., 0., 1., 0.],
    ])

    correct = minmax_rows(X_square)
    silently_wrong = minmax_rows_no_keepdims(X_square)

    # без keepdims строки не приводятся к [0,1] так, как задумано
    assert not np.allclose(correct, silently_wrong)
    # но форма результата всё равно (5,5) - ошибка не бросается в глаза
    assert silently_wrong.shape == X_square.shape

    print("OK")
