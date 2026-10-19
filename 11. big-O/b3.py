
def most_frequent(a: list) -> int:
    '''
    Сложность по времени O(n^2)
    Сложность по памяти O(1)
    '''
    
    number = 0
    max_count = 0
    for num in a:
        if (current_count := a.count(num)) > max_count:
            max_count = current_count
            number = num
    return number

def most_frequent_v2(a: list) -> int:
    '''
    Сложность по времени O(n)
    Сложность по памяти O(n)
    '''
    counter = {}
    for num in a:
        if num in counter:
            counter[num] += 1
        else:
            counter[num] = 1
    return max(counter, key=counter.get)



if __name__ == '__main__':
    for f in (most_frequent, most_frequent_v2):
        assert f([4, 7, 4, 7, 7, 1]) == 7, f.__name__
        assert f([5, 3, 5, 3]) == 5, f.__name__
        assert f([9]) == 9, f.__name__
        # победитель не максимальное число
        assert f([1, 1, 2]) == 1, f.__name__
        # ничья: побеждает тот, кто появился раньше (он меньше)
        assert f([3, 5, 3, 5]) == 3, f.__name__
        # отрицательные числа
        assert f([-1, -1, -5]) == -1, f.__name__
        assert f([2, -7, -7, 2]) == 2, f.__name__
        # победитель в конце списка
        assert f([1, 2, 3, 3, 3]) == 3, f.__name__
        # все разные: первый
        assert f([8, 2, 5]) == 8, f.__name__
    print('ok')