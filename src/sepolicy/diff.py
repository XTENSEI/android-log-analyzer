"""
Diff Module

Compare and diff SELinux rule sets.
"""

from typing import List, Set, Tuple, Dict
from .rules import RuleSet


class RuleDiff:
    """Compare two rule sets and find differences."""
    
    def __init__(self, old_ruleset: RuleSet, new_ruleset: RuleSet):
        self.old = old_ruleset
        self.new = new_ruleset
        self._compute_diff()
    
    def _compute_diff(self) -> None:
        """Compute the differences between rule sets."""
        old_set = set(self.old.get_all_rules())
        new_set = set(self.new.get_all_rules())
        
        self.added = new_set - old_set
        self.removed = old_set - new_set
        self.common = old_set & new_set
    
    def get_added_rules(self) -> List[Tuple]:
        """Get rules that were added."""
        return sorted(self.added)
    
    def get_removed_rules(self) -> List[Tuple]:
        """Get rules that were removed."""
        return sorted(self.removed)
    
    def get_summary(self) -> Dict:
        """Get a summary of the differences."""
        return {
            'added_count': len(self.added),
            'removed_count': len(self.removed),
            'common_count': len(self.common),
        }


def diff_rules(old_ruleset: RuleSet, new_ruleset: RuleSet) -> RuleDiff:
    """Compute diff between two rule sets."""
    return RuleDiff(old_ruleset, new_ruleset)
