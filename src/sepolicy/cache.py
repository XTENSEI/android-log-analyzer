"""
Cache Module

Simple caching for parsed rules.
"""

import json
import os
from typing import Optional, Dict, Any
from pathlib import Path
from .rules import RuleSet


CACHE_DIR = os.path.expanduser("~/.cache/sepolicy_patcher")


class Cache:
    """Simple file-based cache for rules."""
    
    def __init__(self, cache_dir: str = CACHE_DIR):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def get_cache_path(self, key: str) -> str:
        """Get path for a cache key."""
        return os.path.join(self.cache_dir, f"{key}.json")
    
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """Get cached data."""
        path = self.get_cache_path(key)
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        return None
    
    def set(self, key: str, data: Dict[str, Any]) -> None:
        """Set cached data."""
        path = self.get_cache_path(key)
        with open(path, 'w') as f:
            json.dump(data, f)
    
    def delete(self, key: str) -> None:
        """Delete cached data."""
        path = self.get_cache_path(key)
        if os.path.exists(path):
            os.remove(path)
    
    def clear(self) -> None:
        """Clear all cached data."""
        for f in os.listdir(self.cache_dir):
            if f.endswith('.json'):
                os.remove(os.path.join(self.cache_dir, f))
