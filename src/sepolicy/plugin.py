"""
Plugin Module

Plugin system for extending functionality.
"""

from typing import Dict, Callable, Any


class PluginRegistry:
    """Registry for plugins."""
    
    def __init__(self):
        self.plugins: Dict[str, Callable] = {}
    
    def register(self, name: str, func: Callable) -> None:
        """Register a plugin."""
        self.plugins[name] = func
    
    def unregister(self, name: str) -> None:
        """Unregister a plugin."""
        if name in self.plugins:
            del self.plugins[name]
    
    def get(self, name: str) -> Callable:
        """Get a plugin by name."""
        return self.plugins.get(name)
    
    def list_plugins(self) -> list:
        """List all registered plugins."""
        return list(self.plugins.keys())


registry = PluginRegistry()
