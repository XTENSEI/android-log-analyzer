"""
Compare Module

Compare two rule sets.
"""

from typing import Tuple
from .rules import RuleSet


def compare_rules(old: RuleSet, new: RuleSet) -> dict:
    """Compare two rule sets and return differences."""
    old_set = set(old.get_all_rules())
    new_set = set(new.get_all_rules())
    
    added = new_set - old_set
    removed = old_set - new_set
    
    return {
        "added": list(added),
        "removed": list(removed),
        "added_count": len(added),
        "removed_count": len(removed),
    }
