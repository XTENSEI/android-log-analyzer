def memoize(func):
    cache = {}
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

def once(func):
    called = [False]
    result = [None]
    def wrapper(*args):
        if not called[0]:
            result[0] = func(*args)
            called[0] = True
        return result[0]
    return wrapper
