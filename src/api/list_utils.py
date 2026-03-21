def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def group_by(lst, key_func):
    result = {}
    for item in lst:
        key = key_func(item)
        if key not in result:
            result[key] = []
        result[key].append(item)
    return result

def flatten(lst):
    return [item for sublist in lst for item in sublist]
