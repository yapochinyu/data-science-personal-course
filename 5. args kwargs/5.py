import inspect

config = {'n_estimators': 100, 'max_depth': 5, 'comment': 'best run'}

def make_model(n_estimators, max_depth, random_state=42):
    print("ЯХАУ")
    return None

try:
    make_model(**config)
except TypeError:
    print('функция падает с ошибкой, так как ей переданы keyword аргументы, которые не определены при ее создании.')


def safe_call(func, config):
    allowed = set(inspect.signature(func).parameters)
    return func(**{k: v for k, v in config.items() if k in allowed})

safe_call(make_model, config)