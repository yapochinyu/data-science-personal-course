def expensive_compute(x):
    return x**x

def get_features(user_id, cache=None):
    if cache is None:
        cache = {}

    if user_id not in cache:
        cache[user_id] = expensive_compute(user_id)
    return cache[user_id]