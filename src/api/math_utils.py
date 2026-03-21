def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))

def lerp(start, end, t):
    return start + (end - start) * t

def map_range(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
