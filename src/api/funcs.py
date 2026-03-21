def identity(x):
    return x

def constant(x):
    return lambda *args, **kwargs: x
