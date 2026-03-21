import json
import time
from typing import Dict, Any

class Cache:
    def __init__(self, ttl_seconds: int = 300):
        self.cache: Dict[str, tuple] = {}
        self.ttl = ttl_seconds
    
    def get(self, key: str) -> Any:
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return value
            del self.cache[key]
        return None
    
    def set(self, key: str, value: Any):
        self.cache[key] = (value, time.time())
    
    def clear(self):
        self.cache.clear()
    
    def size(self) -> int:
        return len(self.cache)

cache = Cache()
