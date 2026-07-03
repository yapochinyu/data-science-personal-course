def rotate_left(lst, k):
    if not lst:
        return []
    k = k % len(lst)
    return lst[k:] + lst[:k]


if __name__ == '__main__':
    assert rotate_left([1, 2, 3, 4, 5], 2) == [3, 4, 5, 1, 2]
    assert rotate_left([1, 2, 3], 0) == [1, 2, 3]
    assert rotate_left([1, 2, 3], 3) == [1, 2, 3]
    assert rotate_left([], 5) == []
    assert rotate_left([1], 10) == [1]

    lst = []
    for n in range(int(input('Сколько элементов в списке: '))):
        lst.append(input('Введите элемент: '))

    k = int(input('Введите параметр сдвига: '))

    print(rotate_left(lst, k))

    # Сложность решения O(n) мы делаем две копии по частям и объединяем,
    # поэтому проходимся по всем элементам один раз, в случае с использованием цикла и pop(0),
    # на каждом вызове мы бы сдвигали влево все элементы на 1, соответственно сложность была бы O(n * k)
