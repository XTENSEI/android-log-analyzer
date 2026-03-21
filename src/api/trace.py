def trace(func):
    def wrapper(*args, **kwargs):
        print(f"TRACE: {func.__name__}({args}, {kwargs})")
        result = func(*args, **kwargs)
        print(f"TRACE: {func.__name__} -> {result}")
        return result
    return wrapper
