def format_bytes(bytes, precision=2):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024.0:
            return f"{bytes:.{precision}f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.{precision}f} PB"

def format_number(num, precision=0):
    return f"{num:,.{precision}f}"

def format_percent(value, total, precision=1):
    if total == 0:
        return "0%"
    return f"{(value / total * 100):.{precision}f}%"
