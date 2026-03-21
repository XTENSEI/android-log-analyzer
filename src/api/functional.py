def compose(*funcs):
    def composed(x):
        for func in reversed(funcs):
            x = func(x)
        return x
    return composed

def pipe(x, *funcs):
    return compose(*funcs)(x)
