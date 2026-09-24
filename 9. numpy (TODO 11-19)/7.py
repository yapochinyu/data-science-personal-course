import numpy as np

a = np.arange(12).reshape(3,4)

a_raveled = a.ravel() #view
a_transposed_raveled = a.T.ravel() #copy
a_reshaped = a.reshape(-1) #view
a_transposed_reshaped = a.T.reshape(-1) #copy
a_flattened = a.flatten() #copy

print(a_raveled)
print(f'{np.shares_memory(a, a_raveled)} that a_raveled shares memory with a')
print(a_transposed_raveled)
print(f'{np.shares_memory(a, a_transposed_raveled)} that a_transposed_raveled shares memory with a')
print(a_reshaped)
print(f'{np.shares_memory(a, a_reshaped)} that a_reshaped shares memory with a')
print(a_transposed_reshaped)
print(f'{np.shares_memory(a, a_transposed_reshaped)} that a_transposed_reshaped shares memory with a')
print(a_flattened)
print(f'{np.shares_memory(a, a_flattened)} that a_flattened shares memory with a')


def to_c_contiguous(a):
    if a.flags.c_contiguous is True:
        return a
    else:
        return np.ascontiguousarray(a)


if __name__ == '__main__':
    assert np.shares_memory(a, a_raveled)
    assert not np.shares_memory(a, a_transposed_raveled)
    assert np.shares_memory(a, a_reshaped)
    assert not np.shares_memory(a, a_transposed_reshaped)
    assert not np.shares_memory(a, a_flattened)

    b = to_c_contiguous(a)
    assert np.shares_memory(a, b)

    c = a.T
    d = to_c_contiguous(c)
    assert not np.shares_memory(c, d)
    assert d.flags.c_contiguous
    assert np.array_equal(d, c)

    print('all tests passed')

