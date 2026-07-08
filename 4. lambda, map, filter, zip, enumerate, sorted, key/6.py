y_true = [1, 0, 1, 1, 0, 1, 1]
y_pred = [1, 0, 0, 1]

def accuracy(y_true, y_pred):
    try:
        result = sum(t == p for t, p in zip(y_true, y_pred, strict=True)) / len(y_true)
        return result
    except ValueError:
        print('длина не совпадает')
        return None
    

print(accuracy(y_true, y_pred))

if __name__ == '__main__':
    assert accuracy([1, 0, 1, 1, 0, 1, 1][:4], y_pred) == 1.0
    assert accuracy([1, 1, 1, 1], [0, 0, 0, 0]) == 0.0
    assert accuracy([1, 0, 1, 0], [1, 0, 0, 0]) == 0.75
    assert accuracy(y_true, y_pred) is None
    print('all tests passed')