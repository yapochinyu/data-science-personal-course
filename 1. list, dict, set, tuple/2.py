def rotate_left(lst, k):
    if not lst:
        return []
    k = k % len(lst)
    return lst[k:] + lst[:k]

lst = []
for n in range(int(input('Сколько элементов в списке: '))):
    lst.append(input('Введите элемент: '))

k = int(input('Введите параметр сдвига: '))


print(rotate_left(lst, k))



# Сложность решения константная благодаря использованию срезов
# и операций объединения, при использовании цикла 
# сложность бы возрастала с увеличением количества элементов списка