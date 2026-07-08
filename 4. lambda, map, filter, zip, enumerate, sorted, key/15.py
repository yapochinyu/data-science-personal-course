items = [
    {'name': 'laptop', 'price': 1500},
    {'name': 'mouse', 'price': 25},
    {'name': 'monitor', 'price': 1200},
    {'name': 'keyboard', 'price': 60},
    {'name': 'server', 'price': 5000},
]

get_price = lambda item: item['price'] # непонятно, зачем этот промежуточный шаг присваивания имени функции
prices = list(map(get_price, items)) # 
expensive = list(filter(lambda item: item['price'] > 1000, items)) # почему бы тогда здесь не использовать get_price
names = list(map(lambda item: item['name'], expensive)) # очень дорогое использование инструментов, проще и читаемее через comprehensions
print(names)

names = [item['name'] for item in items if item['price'] > 1000]
print(names)

