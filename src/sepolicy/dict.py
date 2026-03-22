"""
Dict Module

Dictionary utilities.
"""

from typing import Dict, Any, List


def merge_dicts(*dicts: Dict) -> Dict:
    """Merge multiple dictionaries."""
    result = {}
    for d in dicts:
        result.update(d)
    return result


def filter_dict(d: Dict, keys: List[str]) -> Dict:
    """Filter dictionary by keys."""
    return {k: v for k, v in d.items() if k in keys}
