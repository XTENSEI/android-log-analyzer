"""
Group Module

Group rules by various criteria.
"""

from typing import Dict, List
from collections import defaultdict
from .rules import RuleSet


class RuleGrouper:
    """Group rules by different criteria."""
    
    def by_source(self, ruleset: RuleSet) -> Dict[str, List]:
        """Group rules by source domain."""
        groups = defaultdict(list)
        for src, tgt, cls, perms in ruleset.get_all_rules():
            groups[src].append((src, tgt, cls, perms))
        return dict(groups)
    
    def by_target(self, ruleset: RuleSet) -> Dict[str, List]:
        """Group rules by target type."""
        groups = defaultdict(list)
        for src, tgt, cls, perms in ruleset.get_all_rules():
            groups[tgt].append((src, tgt, cls, perms))
        return dict(groups)
    
    def by_class(self, ruleset: RuleSet) -> Dict[str, List]:
        """Group rules by class."""
        groups = defaultdict(list)
        for src, tgt, cls, perms in ruleset.get_all_rules():
            groups[cls].append((src, tgt, cls, perms))
        return dict(groups)


def group_by_source(ruleset: RuleSet) -> Dict[str, List]:
    """Group rules by source."""
    grouper = RuleGrouper()
    return grouper.by_source(ruleset)


def group_by_target(ruleset: RuleSet) -> Dict[str, List]:
    """Group rules by target."""
    grouper = RuleGrouper()
    return grouper.by_target(ruleset)


def group_by_class(ruleset: RuleSet) -> Dict[str, List]:
    """Group rules by class."""
    grouper = RuleGrouper()
    return grouper.by_class(ruleset)
