def try_except(func, default=None, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except:
        return default

def silent(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except:
        return None
