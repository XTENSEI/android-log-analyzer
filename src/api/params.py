def defaults(**kwargs):
    def decorator(func):
        def wrapper(*args, **opts):
            for k, v in kwargs.items():
                if k not in opts:
                    opts[k] = v
            return func(*args, **opts)
        return wrapper
    return decorator
