"""
Ext Module

Extension utilities.
"""

from typing import Any


def extend(obj: Any, methods: dict) -> None:
    """Extend object with methods."""
    for name, method in methods.items():
        setattr(obj, name, method)
