"""
Test Module

Testing utilities.
"""

from .rules import RuleSet


def create_test_ruleset() -> RuleSet:
    """Create a test ruleset."""
    rs = RuleSet()
    rs.add_denial({
        'source': 'test_app',
        'target': 'test_file',
        'class': 'file',
        'permissions': {'read', 'write'},
    })
    return rs
