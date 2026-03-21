def trace(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}({args}, {kwargs})")
        return func(*args, **kwargs)
    return wrapper
