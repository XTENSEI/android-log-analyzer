"""
Merger Module

Merges multiple rule sets together.
"""

from typing import List
from .rules import RuleSet


class RuleMerger:
    """Merge multiple rule sets into one."""
    
    def merge(self, rulesets: List[RuleSet], merge_perms: bool = False) -> RuleSet:
        """Merge multiple rule sets."""
        merged = RuleSet(merge_permissions=merge_perms)
        
        for rs in rulesets:
            for src, tgt, cls, perms in rs.get_all_rules():
                for perm in perms:
                    denial = {
                        'source': src,
                        'target': tgt,
                        'class': cls,
                        'permissions': {perm},
                        'raw': '<merged>',
                    }
                    merged.add_denial(denial)
        
        return merged


def merge_rulesets(rulesets: List[RuleSet], merge_perms: bool = False) -> RuleSet:
    """Merge multiple rule sets."""
    merger = RuleMerger()
    return merger.merge(rulesets, merge_perms)
