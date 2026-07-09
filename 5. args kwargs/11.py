def retry(n):
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_execution = None
            for attempt in range(n):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_execution = e
            raise last_execution
        return wrapper
    return decorator


@retry(3)
def flaky(x, y, fail_times=0):
    flaky.calls = getattr(flaky, 'calls', 0) + 1
    if flaky.calls <= fail_times:
        raise ValueError("падение")
    return x + y

print(flaky(2, 3, fail_times=2))