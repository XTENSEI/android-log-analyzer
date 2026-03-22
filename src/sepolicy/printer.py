"""
Printer Module

Pretty printing for rules.
"""

from typing import List, Tuple
from .rules import RuleSet


def print_rules_table(ruleset: RuleSet) -> None:
    """Print rules in table format."""
    print("\n{:<20} {:<20} {:<15} {}".format("Source", "Target", "Class", "Permissions"))
    print("-" * 70)
    
    for src, tgt, cls, perms in ruleset.get_all_rules():
        print("{:<20} {:<20} {:<15} {}".format(
            src[:20], tgt[:20], cls[:15], ', '.join(perms)
        ))


def print_rule(rule: Tuple[str, str, str, List[str]]) -> None:
    """Print a single rule."""
    src, tgt, cls, perms = rule
    print(f"allow {src} {tgt}:{cls} {{ {' '.join(perms)} }};")


def print_rules_list(ruleset: RuleSet, limit: int = 20) -> None:
    """Print rules in list format."""
    rules = ruleset.get_all_rules()
    for i, rule in enumerate(rules[:limit]):
        print_rule(rule)
    if len(rules) > limit:
        print(f"... and {len(rules) - limit} more rules")
