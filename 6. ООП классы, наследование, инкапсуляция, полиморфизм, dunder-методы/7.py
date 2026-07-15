class BaseModel:
    def __init__(self, name):
        self.name = name
        self.is_fitted = False

    def fit(self, X, y):
        self.is_fitted = True

    def _check_fitted(self):
        if not self.is_fitted:
            raise RuntimeError('Model is not fitted')
        
    def predict(self, X):
        self._check_fitted()
        return [0] * len(X)
    

class MeanModel(BaseModel):
    def __init__(self, name, round_digits):
        super().__init__(name)
        self.round_digits = round_digits

    def fit(self, X, y):
        super().fit(X, y)
        self.mean_ = sum(y) / len(y)

    def predict(self, X):
        self._check_fitted()
        value = round(self.mean_, self.round_digits)
        return [value] * len(X)


if __name__ == '__main__':
    base = BaseModel('base')
    try:
        base.predict([1, 2, 3])
        assert False, 'expected RuntimeError before fit'
    except RuntimeError:
        pass

    base.fit([1, 2], [1, 2])
    assert base.is_fitted is True
    assert base.predict([1, 2, 3]) == [0, 0, 0]

    model = MeanModel('mean', round_digits=2)
    assert model.name == 'mean'
    assert model.round_digits == 2
    assert model.is_fitted is False

    try:
        model.predict([1, 2, 3])
        assert False, 'expected RuntimeError before fit'
    except RuntimeError:
        pass

    model.fit([0, 0, 0], [1, 2, 3])
    assert model.is_fitted is True
    assert model.mean_ == 2.0, 'mean_ должен считаться по y, а не по X'

    preds = model.predict([10, 20, 30, 40])
    assert preds == [2.0, 2.0, 2.0, 2.0]
    assert len(preds) == 4

    model2 = MeanModel('mean2', round_digits=3)
    model2.fit([0], [1, 2, 4])
    preds2 = model2.predict([1, 1])
    assert preds2 == [round(7 / 3, 3), round(7 / 3, 3)]

    print('all tests passed')