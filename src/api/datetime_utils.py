from datetime import datetime, timedelta

def format_date(dt, format='%Y-%m-%d %H:%M:%S'):
    return dt.strftime(format)

def parse_date(s):
    for fmt in ['%Y-%m-%d', '%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S']:
        try:
            return datetime.strptime(s, fmt)
        except:
            continue
    return None

def time_ago(dt):
    delta = datetime.now() - dt
    if delta.days > 365:
        return f"{delta.days // 365} years ago"
    elif delta.days > 30:
        return f"{delta.days // 30} months ago"
    elif delta.days > 0:
        return f"{delta.days} days ago"
    elif delta.seconds > 3600:
        return f"{delta.seconds // 3600} hours ago"
    elif delta.seconds > 60:
        return f"{delta.seconds // 60} minutes ago"
    else:
        return f"{delta.seconds} seconds ago"
