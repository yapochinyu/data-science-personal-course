matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

lst = [x for row in matrix for x in row]

even = [x for row in matrix for x in row if x % 2 == 0]

lst_2 = []

for row in matrix:
    for x in row:
        lst_2.append(x)


print(lst)
print(even)
print(lst_2)