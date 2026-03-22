"""
Convert Module

Conversion utilities between formats.
"""

from typing import Dict, Any
from .rules import RuleSet
from .formatters import format_cil, format_te


def rules_to_cil(ruleset: RuleSet) -> str:
    """Convert rules to CIL format string."""
    lines = []
    for src, tgt, cls, perms in ruleset.get_all_rules():
        lines.extend(format_cil(src, tgt, cls, perms))
    return '\n'.join(lines)


def rules_to_te(ruleset: RuleSet) -> str:
    """Convert rules to TE format string."""
    lines = []
    for src, tgt, cls, perms in ruleset.get_all_rules():
        lines.extend(format_te(src, tgt, cls, perms))
    return '\n'.join(lines)


def rules_to_dict(ruleset: RuleSet) -> Dict[str, Any]:
    """Convert rules to dictionary."""
    return {
        "rules": [
            {"source": src, "target": tgt, "class": cls, "permissions": list(perms)}
            for src, tgt, cls, perms in ruleset.get_all_rules()
        ]
    }
