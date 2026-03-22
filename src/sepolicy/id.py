"""
ID Module

Unique ID generation for rules.
"""

import uuid
from typing import Dict


class IDGenerator:
    """Generate unique IDs."""
    
    def __init__(self):
        self.ids: Dict[str, str] = {}
    
    def generate(self, key: str) -> str:
        """Generate ID for a key."""
        if key not in self.ids:
            self.ids[key] = str(uuid.uuid4())[:8]
        return self.ids[key]
    
    def get(self, key: str) -> str:
        """Get ID for a key."""
        return self.ids.get(key, "")


generator = IDGenerator()
