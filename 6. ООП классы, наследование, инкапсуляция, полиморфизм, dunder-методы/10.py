class ConstantModel:
    def fit(self, X, y):
        self._moda = max(set(y), key=y.count)

    def predict(self, X):
        return [self._moda] * len(X)

class ThresholdModel:
    def __init__(self, threshold=0.5):
        self.threshold = threshold
    

    def fit(self, X, y):
        pass
    
    def predict(self, X):
        return [1 if x > self.threshold else 0 for x in X]
    


def evaluate(models, X, y):
    models_dict = {}
    for model in models:
        model.fit(X, y)
        preds = model.predict(X)
        accuracy = sum(true == pred for true, pred in zip(y, preds)) / len(y)
        models_dict[type(model).__name__] = accuracy
    return models_dict


if __name__ == '__main__':
    y = [0, 0, 1, 0, 1]
    X_const = [None] * len(y)

    cm = ConstantModel()
    cm.fit(X_const, y)
    assert cm._moda == 0
    assert cm.predict(X_const) == [0, 0, 0, 0, 0]

    X_thr = [0.1, 0.9, 0.6, 0.2, 0.8]
    tm = ThresholdModel(threshold=0.5)
    tm.fit(X_thr, y)
    assert tm.predict(X_thr) == [0, 1, 1, 0, 1]

    tm_default = ThresholdModel()
    assert tm_default.threshold == 0.5

    results = evaluate([ConstantModel(), ThresholdModel(threshold=0.5)], X_thr, y)
    assert set(results.keys()) == {'ConstantModel', 'ThresholdModel'}
    assert results['ConstantModel'] == 3 / 5
    assert results['ThresholdModel'] == 4 / 5

    print('all tests passed')

