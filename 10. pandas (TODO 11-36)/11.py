import numpy as np
import pandas as pd
from time import perf_counter


def compare_agg(n_rows: int, n_groups: int) -> tuple[float, float]:
    rng = np.random.default_rng(0)
    df = pd.DataFrame({
        'user': rng.integers(0, n_groups, n_rows),
        'amount': rng.random(n_rows),
    })

    # A: своя функция через agg
    start = perf_counter()
    r1 = df.groupby('user')['amount'].agg(lambda s: s.max() - s.min())
    t_a = perf_counter() - start

    # B: готовые агрегаты и вычитание столбцов
    start = perf_counter()
    g = df.groupby('user')['amount']
    r2 = g.max() - g.min()
    t_b = perf_counter() - start

    # сначала убеждаемся, что результаты совпадают
    assert np.allclose(r1, r2)

    return t_a, t_b


if __name__ == '__main__':
    t_a, t_b = compare_agg(500_000, 100_000)
    print(f'A (lambda): {t_a:.3f} s, B (max - min): {t_b:.3f} s')
    print(f'разрыв: {t_a / t_b:.0f}x')