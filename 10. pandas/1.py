import numpy as np
from time import perf_counter

def sum_loop(a: list[int], b: list[int]) -> list[int]:
    if len(a) == len(b):
        result = []
        for i in range(len(a)):
            result.append(a[i] + b[i])
        return result
    else:
        raise ValueError("Массивы разной длины, поэлементной суммы не выйдет")

def sum_vec(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    if len(a) == len(b):
        return a + b
    else:
        raise ValueError("Массивы разной длины, поэлементной суммы не выйдет")

if __name__ == '__main__':
    a = [1, 2, 3]
    b = [10, 20, 30]
    assert sum_loop(a, b) == [11, 22, 33]
    assert np.array_equal(sum_vec(np.array(a), np.array(b)), [11, 22, 33])
    try:
        sum_loop([1, 2], [1])
        assert False, "ожидался ValueError"
    except ValueError:
        pass
    try:
        sum_vec(np.array([1, 2]), np.array([1]))
        assert False, "ожидался ValueError"
    except ValueError:
        pass


    n = 1_000_000
    lst1 = list(range(n))
    arr1 = np.arange(n)
    lst2 = list(range(n))
    arr2 = np.arange(n)

    res_lst = sum_loop(lst1, lst2)
    start_time_lst = perf_counter()
    res_lst = sum_loop(lst1, lst2)
    end_time_lst = perf_counter()
    execution_time_lst = end_time_lst - start_time_lst

    res_arr = sum_vec(arr1, arr2)
    start_time_arr = perf_counter()
    res_arr = sum_vec(arr1, arr2)
    end_time_arr = perf_counter()
    execution_time_arr = end_time_arr - start_time_arr


    print('lst:', execution_time_lst)
    print('array:', execution_time_arr)
    print(execution_time_lst / execution_time_arr)