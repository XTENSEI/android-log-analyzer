from datetime import datetime
import time

class RateLimiter:
    def __init__(self, max_calls, period):
        self.max_calls = max_calls
        self.period = period
        self.calls = []
    
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            now = time.time()
            self.calls = [c for c in self.calls if now - c < self.period]
            
            if len(self.calls) >= self.max_calls:
                raise Exception(f"Rate limit exceeded. Max {self.max_calls} calls per {self.period}s")
            
            self.calls.append(now)
            return func(*args, **kwargs)
        return wrapper
