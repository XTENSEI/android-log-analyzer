def validate(**rules):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for param, validator in rules.items():
                if param in kwargs:
                    if not validator(kwargs[param]):
                        raise ValueError(f"Invalid {param}")
            return func(*args, **kwargs)
        return wrapper
    return decorator
