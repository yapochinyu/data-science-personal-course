def group_sum(keys: list, values: list[float]) -> dict:
    unique_keys = []
    codes = []
    for key in keys:
        if key in unique_keys:
            codes.append(unique_keys.index(key))
        else:
            unique_keys.append(key)
            codes.append(len(unique_keys) - 1)

    sums = [0] * len(unique_keys)

    for code, value in zip(codes, values):
        sums[code] += value
        
    return dict(zip(unique_keys, sums))


if __name__ == '__main__':
    assert group_sum(['B', 'A', 'B', 'C', 'A'], [10, 20, 5, 7, 3]) == {'B': 15, 'A': 23, 'C': 7}

