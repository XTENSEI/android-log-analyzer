def union(*sets):
    result = set()
    for s in sets:
        result |= set(s)
    return result

def intersection(*sets):
    result = sets[0] if sets else set()
    for s in sets[1:]:
        result &= set(s)
    return result

def difference(a, b):
    return set(a) - set(b)
