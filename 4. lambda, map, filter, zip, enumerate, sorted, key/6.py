y_true = [1, 0, 1, 1, 0, 1, 1]
y_pred = [1, 0, 0, 1]

accuracy = sum(t == p for t, p in zip(y_true, y_pred, strict=True))
print(accuracy)