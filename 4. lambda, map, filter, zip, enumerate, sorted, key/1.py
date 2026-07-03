def sort_by_price(products):
    return sorted(products, key=lambda x: x['price'])


def sort_by_total_value_desc(products):
    return sorted(products, key=lambda x: x['price'] * x['qty'], reverse=True)


def most_expensive(products):
    return max(products, key=lambda x: x['price'])


if __name__ == '__main__':
    products = [
        {'name': 'milk', 'price': 80, 'qty': 3},
        {'name': 'bread', 'price': 45, 'qty': 10},
        {'name': 'cheese', 'price': 450, 'qty': 1}
    ]

    assert sort_by_price(products) == [
        {'name': 'bread', 'price': 45, 'qty': 10},
        {'name': 'milk', 'price': 80, 'qty': 3},
        {'name': 'cheese', 'price': 450, 'qty': 1}
    ]
    assert sort_by_total_value_desc(products) == [
        {'name': 'bread', 'price': 45, 'qty': 10},
        {'name': 'cheese', 'price': 450, 'qty': 1},
        {'name': 'milk', 'price': 80, 'qty': 3}
    ]
    assert most_expensive(products) == {'name': 'cheese', 'price': 450, 'qty': 1}

    print(sort_by_price(products))
    print(sort_by_total_value_desc(products))
    print(most_expensive(products))
