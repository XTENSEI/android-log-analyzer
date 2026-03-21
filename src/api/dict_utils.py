def merge_dicts(*dicts):
    result = {}
    for d in dicts:
        result.update(d)
    return result

def deep_get(d, path, default=None):
    keys = path.split('.')
    for key in keys:
        if isinstance(d, dict) and key in d:
            d = d[key]
        else:
            return default
    return d

def deep_set(d, path, value):
    keys = path.split('.')
    for key in keys[:-1]:
        if key not in d:
            d[key] = {}
        d = d[key]
    d[keys[-1]] = value
