import numpy as np
import sys

def sizely(values: list[int]) -> tuple[int, int]:

    list_size = sys.getsizeof(values)

    seen = set()
    for x in values:
        if id(x) not in seen:
            list_size += sys.getsizeof(x)
            seen.add(id(x))

    array_size = np.array(values, dtype='int64').nbytes

    return list_size, array_size


if __name__ == '__main__':
    # пример из задачи: массив должен весить ровно 5 * 8 = 40 байт
    l_size, a_size = sizely([10, 20, 30, 40, 50])
    assert a_size == 40

    # маленькие целые кешируются CPython (-5..256) — один и тот же объект
    # переиспользуется много раз, значит должен учитываться один раз
    values_small = [1] * 1000
    l_size_small, _ = sizely(values_small)
    expected = sys.getsizeof(values_small) + sys.getsizeof(1)
    assert l_size_small == expected

    # наивный (неправильный) подсчёт умножил бы размер числа на 1000 —
    # честный результат должен быть заметно меньше
    naive = sys.getsizeof(values_small) + sys.getsizeof(1) * 1000
    assert l_size_small < naive

    # большие целые вне диапазона кеша обычно не переиспользуются между
    # собой, поэтому размер должен расти почти пропорционально их числу
    values_big = [1_000_000 + i for i in range(1000)]
    l_size_big, _ = sizely(values_big)
    assert l_size_big > sys.getsizeof(values_big) + sys.getsizeof(1_000_000) * 500

    print("all tests passed")