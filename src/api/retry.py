def retry(max_attempts=3, delay=1, backoff=2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            current_delay = delay
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    import time
                    time.sleep(current_delay)
                    current_delay *= backoff
        return wrapper
    return decorator
