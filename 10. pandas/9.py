import pandas as pd

df = pd.DataFrame({'v': [10, 20, 30, 40, 50, 60]}, index=[10, 20, 30, 40, 50, 60])


def describe(result) -> str:
    if isinstance(result, pd.DataFrame):
        return f"{len(result)} rows {result['v'].tolist()}"
    if isinstance(result, pd.Series):
        return str(result['v'])
    return str(result)


def probe() -> list[str]:
    cases = [
        ('loc[20]', lambda: df.loc[20]),
        ('iloc[20]', lambda: df.iloc[20]),
        ('loc[10:30]', lambda: df.loc[10:30]),
        ('iloc[10:30]', lambda: df.iloc[10:30]),
        ('loc[0]', lambda: df.loc[0]),
        ('iloc[0]', lambda: df.iloc[0]),
        ('[10:30]', lambda: df[10:30]),
        ('[0:2]', lambda: df[0:2]),
    ]
    out = []
    for name, expr in cases:
        try:
            out.append(f"{name} -> {describe(expr())}")
        except Exception as e:
            out.append(f"{name} -> {type(e).__name__}")
    return out


if __name__ == "__main__":
    res = probe()
    for line in res:
        print(line)
    assert res == [
        "loc[20] -> 20",
        "iloc[20] -> IndexError",
        "loc[10:30] -> 3 rows [10, 20, 30]",
        "iloc[10:30] -> 0 rows []",
        "loc[0] -> KeyError",
        "iloc[0] -> 10",
        "[10:30] -> 0 rows []",
        "[0:2] -> 2 rows [10, 20]",
    ]
