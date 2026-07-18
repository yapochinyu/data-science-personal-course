def train_test_split_strict(X, y, test_size):
    if not 0 < test_size < 1:
        raise ValueError(f'test_size: {test_size} не в диапазоне от 0 до 1')
    if len(X) != len(y):
        raise ValueError('Длины X и y не совпадают')
    if (split_idx := int(len(X) * (1 - test_size))) in (0, len(X)):
        raise ValueError(f'Выборка мала (len(X)={len(X)}, test_size={test_size}): train или test пустые')
    return split_idx