def once(func):
    called = [False]
    result = [None]
    def wrapper(*args, **kwargs):
        if not called[0]:
            result[0] = func(*args, **kwargs)
            called[0] = True
        return result[0]
    return wrapper

@once
def init():
    print("Initialized")
