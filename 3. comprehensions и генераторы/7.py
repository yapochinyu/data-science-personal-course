# def stats(data):
#     squares = (x**2 for x in data)
#     total = sum(squares)
#     maximum = max(squares)
#     return total, maximum

# print(stats([1, 2, 3]))

# Вызовет ValueError, потому что у нас исчерпан генератор на второй раз


def stats(data):
    squares = [x**2 for x in data]
    total = sum(squares)
    maximum = max(squares)
    return total, maximum

print(stats([1, 2, 3]))

def stats_gen(data):
    total = sum(x**2 for x in data)
    maximum = max(x**2 for x in data) 
    return total, maximum

print(stats_gen([1, 2, 3]))