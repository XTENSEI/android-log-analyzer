"""
Mixin Module

Mixin classes for rules.
"""

class RuleMixin:
    """Mixin for rule objects."""
    
    def to_short_string(self):
        return str(self)


class CacheMixin:
    """Mixin for cache operations."""
    
    def clear_cache(self):
        pass
