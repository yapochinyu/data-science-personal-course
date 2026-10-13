import pandas as pd
import numpy as np

def predict_nans(a: pd.Series, b: pd.Series) -> int:
    return len(set(a.index) ^ set(b.index))


def predict_nans_dup(a: pd.Series, b: pd.Series) -> int:
    # сколько раз встречается каждая метка у каждого операнда
    count_a = a.index.value_counts()
    count_b = b.index.value_counts()

    # NaN дают строки только по меткам, которых нет у второго операнда;
    # такая метка даёт столько строк, сколько раз она повторяется у своего операнда
    only_a = count_a[~count_a.index.isin(count_b.index)].sum()
    only_b = count_b[~count_b.index.isin(count_a.index)].sum()
    return int(only_a + only_b)


if __name__ == '__main__':
    s = pd.Series([1, 2, 3], index=['x', 'y', 'z'])
    s2 = pd.Series([1, 2, 3], index=['y', 'z', 'v'])
    assert predict_nans(s, s2) == 2

    s3 = pd.Series([1, 2], index=['x', 'y'])
    s4 = pd.Series([1, 2], index=['p', 'q'])
    assert predict_nans(s3, s4) == 4

    # дубликаты: метка 'y' повторяется дважды и есть только у первого операнда
    d1 = pd.Series([1, 2], index=['y', 'y'])
    d2 = pd.Series([10], index=['z'])
    assert predict_nans(d1, d2) == 2      # старая версия ошибается
    assert predict_nans_dup(d1, d2) == 3

    # общая метка с дубликатами даёт строки без NaN (2 × 3 = 6), в ответ не входит
    d3 = pd.Series([1, 2], index=['x', 'x'])
    d4 = pd.Series([1, 2, 3], index=['x', 'x', 'x'])
    assert predict_nans_dup(d3, d4) == 0

    # без дубликатов даёт то же, что и простая версия
    assert predict_nans_dup(s, s2) == 2
    assert predict_nans_dup(s3, s4) == 4

    # сверка с настоящим сложением на случайных данных с дубликатами
    rng = np.random.default_rng(0)
    labels = list('abcdef')
    for _ in range(200):
        a = pd.Series(1.0, index=rng.choice(labels, size=rng.integers(1, 8)))
        b = pd.Series(1.0, index=rng.choice(labels, size=rng.integers(1, 8)))
        assert predict_nans_dup(a, b) == (a + b).isna().sum()
