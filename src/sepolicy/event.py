"""
Event Module

Event handling system.
"""

from typing import Callable, Dict, List
from dataclasses import dataclass, field


@dataclass
class Event:
    """An event."""
    name: str
    data: Dict = field(default_factory=dict)


class EventEmitter:
    """Simple event emitter."""
    
    def __init__(self):
        self.listeners: Dict[str, List[Callable]] = {}
    
    def on(self, event: str, callback: Callable) -> None:
        """Register an event listener."""
        if event not in self.listeners:
            self.listeners[event] = []
        self.listeners[event].append(callback)
    
    def off(self, event: str, callback: Callable) -> None:
        """Remove an event listener."""
        if event in self.listeners:
            self.listeners[event] = [cb for cb in self.listeners[event] if cb != callback]
    
    def emit(self, event: str, data: Dict = None) -> None:
        """Emit an event."""
        if event in self.listeners:
            e = Event(event, data or {})
            for cb in self.listeners[event]:
                cb(e)


emitter = EventEmitter()
