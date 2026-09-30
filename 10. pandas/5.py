import pandas as pd
import numpy as np
from time import perf_counter

def add_cols_loop(df: pd.DataFrame, new: dict[str, np.ndarray]) -> pd.DataFrame: 
    df = df.copy()
    for col_name, col_values in new.items():
        df[col_name] = col_values
    return df

def add_cols_once(df: pd.DataFrame, new: dict[str, np.ndarray]) -> pd.DataFrame: 
    return pd.concat([df, pd.DataFrame(new)], axis = 1)

if __name__ == '__main__':
    rng = np.random.default_rng(0)
    n_rows = 200_000
    df = pd.DataFrame(rng.random((n_rows, 30)), columns=[f'c{i}' for i in range(30)])
    new = {f'new{i}': rng.random(n_rows) for i in range(50)}
    original = df.copy()

    res_loop = add_cols_loop(df, new)
    res_once = add_cols_once(df, new)

    # форма и имена столбцов
    assert res_loop.shape == (n_rows, 80)
    assert res_once.shape == (n_rows, 80)
    assert list(res_loop.columns) == list(res_once.columns)
    assert list(res_once.columns) == list(df.columns) + list(new)

    # обе функции дают одинаковую таблицу
    assert res_loop.equals(res_once)

    # значения новых столбцов на месте
    for name, values in new.items():
        assert np.array_equal(res_once[name].to_numpy(), values)

    # исходная таблица не изменена
    assert df.equals(original)
    assert df.shape == (n_rows, 30)

    # замер времени
    start = perf_counter()
    add_cols_loop(df, new)
    t_loop = perf_counter() - start

    start = perf_counter()
    add_cols_once(df, new)
    t_once = perf_counter() - start

    print(f'loop: {t_loop:.4f} s, once: {t_once:.4f} s')

    print('all tests passed')
