"""
Sort Module

Sorting utilities for rules.
"""

from typing import List, Tuple
from .rules import RuleSet


def sort_by_source(rules: List[Tuple]) -> List[Tuple]:
    """Sort rules by source domain."""
    return sorted(rules, key=lambda r: r[0])


def sort_by_target(rules: List[Tuple]) -> List[Tuple]:
    """Sort rules by target type."""
    return sorted(rules, key=lambda r: r[1])


def sort_by_class(rules: List[Tuple]) -> List[Tuple]:
    """Sort rules by class."""
    return sorted(rules, key=lambda r: r[2])


def sort_by_permission_count(rules: List[Tuple]) -> List[Tuple]:
    """Sort rules by number of permissions."""
    return sorted(rules, key=lambda r: len(r[3]), reverse=True)


def sort_rules(ruleset: RuleSet, by: str = "source") -> List[Tuple]:
    """Sort rules by specified criteria."""
    rules = ruleset.get_all_rules()
    
    if by == "source":
        return sort_by_source(rules)
    elif by == "target":
        return sort_by_target(rules)
    elif by == "class":
        return sort_by_class(rules)
    elif by == "perms":
        return sort_by_permission_count(rules)
    else:
        return rules
