"""
Context Module

Context management for rules processing.
"""

from typing import Optional, Dict, Any


class Context:
    """Processing context."""
    
    def __init__(self):
        self.data: Dict[str, Any] = {}
        self.errors: list = []
        self.warnings: list = []
    
    def set(self, key: str, value: Any) -> None:
        """Set a value."""
        self.data[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a value."""
        return self.data.get(key, default)
    
    def add_error(self, error: str) -> None:
        """Add an error."""
        self.errors.append(error)
    
    def add_warning(self, warning: str) -> None:
        """Add a warning."""
        self.warnings.append(warning)
    
    def has_errors(self) -> bool:
        """Check if there are errors."""
        return len(self.errors) > 0


def create_context() -> Context:
    """Create a new context."""
    return Context()
