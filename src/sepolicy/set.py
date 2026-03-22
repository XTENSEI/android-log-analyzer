"""
Set Module

Set utilities.
"""

from typing import Set, List


def union_sets(*sets: Set) -> Set:
    """Union of multiple sets."""
    result = set()
    for s in sets:
        result |= s
    return result


def intersection_sets(*sets: Set) -> Set:
    """Intersection of multiple sets."""
    result = sets[0] if sets else set()
    for s in sets[1:]:
        result &= s
    return result
