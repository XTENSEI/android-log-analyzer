def require(cond, msg="Assertion failed"):
    if not cond:
        raise ValueError(msg)
