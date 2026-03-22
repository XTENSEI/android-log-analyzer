"""
String Module

String utilities.
"""

from typing import List


def normalize_source(s: str) -> str:
    """Normalize source domain name."""
    return s.strip().lower().replace('_', '_')


def normalize_target(s: str) -> str:
    """Normalize target type name."""
    return s.strip().lower().replace('_', '_')


def split_permissions(perms: str) -> List[str]:
    """Split permissions string into list."""
    return perms.replace(',', ' ').split()
