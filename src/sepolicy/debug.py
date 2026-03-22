"""
Debug Module

Debug utilities.
"""

from typing import Any


def debug_print(msg: str) -> None:
    """Print debug message."""
    print(f"[DEBUG] {msg}")


def dump_rule(rule: Any) -> str:
    """Dump rule for debugging."""
    return str(rule)
