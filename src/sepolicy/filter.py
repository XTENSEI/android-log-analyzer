"""
Filter Module

Advanced filtering for SELinux rules.
"""

from typing import List, Set, Optional, Callable
from .rules import RuleSet, Rule


class RuleFilter:
    """Advanced filtering for rules."""
    
    def filter_by_source(self, ruleset: RuleSet, sources: Set[str]) -> RuleSet:
        """Filter rules by source domains."""
        return ruleset.filter(source_whitelist=sources)
    
    def filter_by_target(self, ruleset: RuleSet, targets: Set[str]) -> RuleSet:
        """Filter rules by target types."""
        filtered = RuleSet(merge_permissions=ruleset.merge_permissions)
        for src, tgt, cls, perms in ruleset.get_all_rules():
            if tgt in targets:
                for perm in perms:
                    denial = {
                        'source': src,
                        'target': tgt,
                        'class': cls,
                        'permissions': {perm},
                    }
                    filtered.add_denial(denial)
        return filtered
    
    def filter_by_class(self, ruleset: RuleSet, classes: Set[str]) -> RuleSet:
        """Filter rules by class."""
        filtered = RuleSet(merge_permissions=ruleset.merge_permissions)
        for src, tgt, cls, perms in ruleset.get_all_rules():
            if cls in classes:
                for perm in perms:
                    denial = {
                        'source': src,
                        'target': tgt,
                        'class': cls,
                        'permissions': {perm},
                    }
                    filtered.add_denial(denial)
        return filtered
    
    def filter_by_permission(self, ruleset: RuleSet, perms: Set[str]) -> RuleSet:
        """Filter rules by permissions."""
        return ruleset.filter(perm_whitelist=perms)


def filter_rules(
    ruleset: RuleSet,
    sources: Optional[Set[str]] = None,
    targets: Optional[Set[str]] = None,
    classes: Optional[Set[str]] = None,
    perms: Optional[Set[str]] = None,
) -> RuleSet:
    """Convenience function to filter rules."""
    filter_obj = RuleFilter()
    result = ruleset
    
    if sources:
        result = filter_obj.filter_by_source(result, sources)
    if targets:
        result = filter_obj.filter_by_target(result, targets)
    if classes:
        result = filter_obj.filter_by_class(result, classes)
    if perms:
        result = filter_obj.filter_by_permission(result, perms)
    
    return result
