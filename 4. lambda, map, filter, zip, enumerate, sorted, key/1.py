products = [
    {'name': 'milk', 'price': 80, 'qty': 3},
    {'name': 'bread', 'price': 45, 'qty': 10},
    {'name': 'cheese', 'price': 450, 'qty': 1}
    ]

print(sorted(products, key=lambda x: x['price']))

print(sorted(products, key=lambda x: x['price'] * x['qty'], reverse=True))

print(max(products, key=lambda x: x['price']))