def safe_divide(a, b, default=0):
    try:
        return a / b if b != 0 else default
    except:
        return default

def clamp(value, min_val, max_val):
    return max(min_val, min(value, max_val))

def percent_of(part, total):
    return (part / total * 100) if total != 0 else 0
