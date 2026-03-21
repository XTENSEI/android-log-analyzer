def ensure_list(val):
    return val if isinstance(val, list) else [val]

def ensure_tuple(val):
    return val if isinstance(val, tuple) else (val,)

def ensure_dict(val):
    return val if isinstance(val, dict) else {}
