"""
Memory Module

Memory-efficient rule processing.
"""

from typing import Iterator, Tuple, List
from .rules import RuleSet


def stream_rules(ruleset: RuleSet) -> Iterator[Tuple]:
    """Stream rules one at a time."""
    for rule in ruleset.get_all_rules():
        yield rule


def batch_rules(ruleset: RuleSet, batch_size: int = 100) -> List[List[Tuple]]:
    """Process rules in batches."""
    rules = ruleset.get_all_rules()
    batches = []
    for i in range(0, len(rules), batch_size):
        batches.append(rules[i:i + batch_size])
    return batches


def iter_rules(ruleset: RuleSet) -> Iterator[Tuple]:
    """Iterate over rules."""
    return iter(ruleset.get_all_rules())
