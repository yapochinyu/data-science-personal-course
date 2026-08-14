# - (8,1,6)+(7,1) = (8, 7, 6) смысл операции сложно мне понять
# - (3,)+(4,) упадет исправить через a[:, None] таблица всех пар
# - (5,4)+(4,) = (5, 4) вектор прибавляется к каждой строке
# - (5,4)+(5,) упадет, потому что правые оси не равны правка скорее всего b[:, None]
# - (2,3)+(3,2) упадет правки либо a[:, :, None] + b либо a[None, :, :]

def broadcast_cost(shape_a: tuple, shape_b: tuple, itemsize) -> tuple:

    ndim = max(shape_a, shape_b)

    shape_a = (1,) * (ndim - len(shape_a)) + shape_a
    shape_b = (1,) * (ndim - len(shape_b)) + shape_b

    result_shape = []

    for dim_a, dim_b in zip(shape_a, shape_b):
        if dim_a == dim_b:
            result_shape.append(dim_a)
        elif dim_a == 1:
            result_shape.append(dim_b)
        elif dim_b == 1:
            result_shape.append(dim_a)
        else:
            print(f'shapes {shape_a} and {shape_b} are not broadcastable')

    result_shape = tuple(result_shape)

    num_elements = 1
    for dim in result_shape:
        num_elements *= dim

    num_bytes = num_elements * itemsize

    return result_shape, num_bytes