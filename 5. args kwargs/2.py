def describe(*args, **kwargs):
    return f"got {len(args)} positional, {len(kwargs)} keyword: {[name for name in kwargs]}"

print(describe(1, 'a', [2], lr=0.1, epochs=10))