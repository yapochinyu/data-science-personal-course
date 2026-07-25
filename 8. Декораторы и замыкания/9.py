from functools import wraps


def debug(func):
    def wrapper(*args, **kwargs):
        print(f'function: {func.__name__}, {args, kwargs}')
        result = func(*args, **kwargs)
        return result
    return wrapper

@debug
def summator(*nums, multiplier=1):
    '''
    сумматор
    '''
    return sum(nums * multiplier)

print(summator.__name__)
print(summator.__doc__)
help(summator)


def debug_b(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f'function: {func.__name__}, {args, kwargs}')
        result = func(*args, **kwargs)
        return result
    return wrapper        



@debug_b
def summer(*nums, multiplier=1):
    '''
    сумматор
    '''
    return sum(nums * multiplier)

print(summer.__name__)
print(summer.__doc__)
help(summer)
