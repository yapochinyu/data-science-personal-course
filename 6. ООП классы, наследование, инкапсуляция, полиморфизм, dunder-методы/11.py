class Vector:
    def __init__(self, *coords):
        self.coords = list(coords)

    def __repr__(self):
        return f'Vector {self.coords}'
    
    def __eq__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented
        return self.coords == other.coords

    def __add__(self, other):
        if len(self.coords) != len(other.coords):
            raise ValueError('vectors must have the same length')
        else:
            return Vector(*[x + y for x, y in zip(self.coords, other.coords)])
        
    def __mul__(self, scalar):
        return Vector(*[x * scalar for x in self.coords])

    def __len__(self):
        return len(self.coords)


if __name__ == '__main__':
    v1 = Vector(1, 2, 3)
    v2 = Vector(1, 2, 3)
    v3 = Vector(4, 5, 6)

    assert repr(v1) == 'Vector [1, 2, 3]'
    assert v1 == v2
    assert v1 != v3
    assert v1 != 'not a vector'
    assert (v1 == 'not a vector') is False

    assert v1 + v3 == Vector(5, 7, 9)
    try:
        v1 + Vector(1, 2)
        assert False, 'expected ValueError for mismatched lengths'
    except ValueError:
        pass

    assert v1 * 2 == Vector(2, 4, 6)
    assert len(v1) == 3
    assert len(Vector(1, 2, 3, 4, 5)) == 5

    print('all tests passed')
