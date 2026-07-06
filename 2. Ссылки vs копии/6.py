def zeros_matrix(rows, cols):
    return [[0] * cols for _ in range(rows)]


if __name__ == '__main__':
    m = zeros_matrix(3, 3)
    assert m == [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    m[0][0] = 1
    assert m == [[1, 0, 0], [0, 0, 0], [0, 0, 0]], "изменилась не одна ячейка"
    assert m[1] == [0, 0, 0], "строки не должны быть общим объектом"

    assert m[0] is not m[1], "[[0]*cols]*rows дал бы общий объект для всех строк"

    assert zeros_matrix(0, 5) == []
    assert zeros_matrix(2, 0) == [[], []]

    print("все тесты прошли")
