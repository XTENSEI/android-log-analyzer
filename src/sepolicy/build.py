"""
Build Module

Build output from rules.
"""

from typing import Dict, Any
from .rules import RuleSet
from .formatters import format_cil, format_te


def build_cil(ruleset: RuleSet) -> str:
    """Build CIL output."""
    lines = ["# SELinux policy"]
    for src, tgt, cls, perms in ruleset.get_all_rules():
        lines.extend(format_cil(src, tgt, cls, perms))
    return '\n'.join(lines)


def build_te(ruleset: RuleSet) -> str:
    """Build TE output."""
    lines = ["# SELinux policy"]
    for src, tgt, cls, perms in ruleset.get_all_rules():
        lines.extend(format_te(src, tgt, cls, perms))
    return '\n'.join(lines)
