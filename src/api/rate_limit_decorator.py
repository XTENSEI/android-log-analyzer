def rate_limit(calls, period):
    import time
    cache = {'calls': [], 'lock': False}
    def decorator(func):
        def wrapper(*args, **kwargs):
            now = time.time()
            cache['calls'] = [c for c in cache['calls'] if now - c < period]
            if len(cache['calls']) >= calls:
                raise Exception('Rate limit exceeded')
            cache['calls'].append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator
