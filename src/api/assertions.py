def require(cond, msg="Assertion failed"):
    if not cond:
        raise ValueError(msg)

def assert_type(val, expected_type, name="value"):
    if not isinstance(val, expected_type):
        raise TypeError(f"{name} must be {expected_type}")
