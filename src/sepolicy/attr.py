"""
Attr Module

Attribute handling.
"""

class Attr:
    """Attribute container."""
    
    def __init__(self, name, value):
        self.name = name
        self.value = value
    
    def __repr__(self):
        return f"Attr({self.name}={self.value})"
