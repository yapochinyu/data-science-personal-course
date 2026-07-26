REGISTRY = {}

def register(name):
    def decorator(func):
        REGISTRY[name] = func
        return func
    return decorator


@register('normalize')
def normalize(data):
    return [x / max(data) for x in data]


@register('clip')
def clip(data, low=0, high=1):
    return [min(max(x, low), high) for x in data]


@register('double')
def double(data):
    return [x * 2 for x in data]


def apply_pipeline(data, steps):
    for step in steps:
        if step not in REGISTRY:
            raise ValueError(f'неизвестный шаг: {step}')
        data = REGISTRY[step](data)
    return data


# register может вернуть функцию без обёртки, потому что декоратору не
# обязательно менять поведение функции — здесь его задача исчерпывается
# побочным эффектом (записью в REGISTRY) в момент определения функции.
# Вызов функции остаётся прежним, никакой обёртки не требуется.


if __name__ == '__main__':
    assert apply_pipeline([1, 2, 4], ['normalize']) == [0.25, 0.5, 1.0]
    assert apply_pipeline([-1, 0.5, 2], ['clip']) == [0, 0.5, 1]
    assert apply_pipeline([1, 2], ['double']) == [2, 4]
    assert apply_pipeline([1, 2, 4], ['normalize', 'clip']) == [0.25, 0.5, 1.0]

    try:
        apply_pipeline([1], ['unknown'])
        assert False, 'ожидался ValueError'
    except ValueError:
        pass

    print('OK')

            