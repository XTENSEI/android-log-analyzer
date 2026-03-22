"""
Timer Module

Timing utilities.
"""

import time
from typing import Optional


class Timer:
    """Simple timer."""
    
    def __init__(self):
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
    
    def start(self):
        self.start_time = time.time()
    
    def stop(self):
        self.end_time = time.time()
    
    def elapsed(self) -> float:
        if self.start_time is None:
            return 0.0
        end = self.end_time or time.time()
        return end - self.start_time


def measure(func):
    """Decorator to measure execution time."""
    def wrapper(*args, **kwargs):
        t = Timer()
        t.start()
        result = func(*args, **kwargs)
        t.stop()
        print(f"{func.__name__} took {t.elapsed():.3f}s")
        return result
    return wrapper
