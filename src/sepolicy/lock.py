"""
Lock Module

Thread-safe operations.
"""

import threading


class Lock:
    """Thread lock wrapper."""
    
    def __init__(self):
        self._lock = threading.Lock()
    
    def acquire(self):
        return self._lock.acquire()
    
    def release(self):
        return self._lock.release()
    
    def __enter__(self):
        self._lock.acquire()
        return self
    
    def __exit__(self, *args):
        self._lock.release()


class RWLock:
    """Read-write lock."""
    
    def __init__(self):
        self._readers = 0
        self._writers = 0
        self._lock = threading.Lock()
    
    def read_acquire(self):
        with self._lock:
            while self._writers > 0:
                self._lock.release()
                self._lock.acquire()
            self._readers += 1
    
    def read_release(self):
        with self._lock:
            self._readers -= 1
    
    def write_acquire(self):
        self._lock.acquire()
        while self._readers > 0:
            pass
    
    def write_release(self):
        self._lock.release()
