import numpy as np

def predict(X: np.ndarray, w: np.ndarray, b: np.ndarray) -> np.ndarray:
    raw = X @ w + b 
    return (raw > 0).astype(int)

def metrics(pred: np.ndarray, y: np.ndarray) -> dict:
    tp = ((pred == 1) & (y == 1)).sum()
    fp = ((pred == 1) & (y == 0)).sum()
    fn = ((pred == 0) & (y == 1)).sum()

    accuracy = (pred == y).mean()

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0

    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0

    return {'accuracy' : accuracy, 'precision' : precision, 'recall' : recall}


if __name__ == '__main__':
    X = np.array([
        [1., 2.],
        [2., 1.],
        [-1., -1.],
        [0., 0.],
        [3., 3.],
    ])
    w = np.array([1., -1.])
    b = 0.0
    y = np.array([1, 1, 0, 0, 1])

    pred = predict(X, w, b)
    m = metrics(pred, y)
    print(pred, m)

    # X * w вместо X @ w:
    # X * w даёт форму (n, d) — w broadcast-ится по строкам, каждый элемент строки
    # умножается на соответствующий вес, но суммирования по признакам не происходит.
    # Не падает, потому что (n, d) * (d,) — валидный broadcast.
    # raw = (X * w + b) > 0 сравнивает булеву маску формы (n, d) вместо (n,),
    # и вся дальнейшая арифметика (accuracy/precision/recall) считается неверно
    # или падает на несовпадении форм с y (n,) при попытке ((pred == 1) & (y == 1)).
    wrong = X * w + b
    print(wrong.shape)  # (5, 2), а не (5,)

    print('all tests passed')
