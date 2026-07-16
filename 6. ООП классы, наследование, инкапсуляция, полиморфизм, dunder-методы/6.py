class Dataset:
    def __init__(self, _data=None):
        self.data = _data
    
    @property
    def size(self):
        return len(self._data)
    
    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, value):
        if not value:
            raise ValueError('data не может быть пустым')
        self._data = value
    
    @property
    def mean(self):
        return sum(self._data) / len(self._data)