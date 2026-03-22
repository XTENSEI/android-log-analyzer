"""
Base Module

Base classes.
"""

from typing import Any


class Base:
    """Base class."""
    
    def __init__(self):
        self.data = {}
    
    def to_dict(self) -> dict:
        return self.data
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Base':
        obj = cls()
        obj.data = data
        return obj
