"""
Report Module

Generate reports from rules.
"""

from typing import Dict, Any
from .rules import RuleSet
from .stats import get_rule_statistics


def generate_summary_report(ruleset: RuleSet) -> str:
    """Generate a summary report."""
    stats = get_rule_statistics(ruleset)
    
    lines = []
    lines.append("SELinux Policy Analysis Report")
    lines.append("=" * 50)
    lines.append(f"Total Rules: {stats['total_rules']}")
    lines.append(f"Unique Sources: {stats['unique_sources']}")
    lines.append(f"Unique Targets: {stats['unique_targets']}")
    lines.append(f"Unique Classes: {stats['unique_classes']}")
    
    return '\n'.join(lines)


def generate_full_report(ruleset: RuleSet) -> str:
    """Generate a full report with all details."""
    lines = []
    lines.append(generate_summary_report(ruleset))
    lines.append("\nTop Sources:")
    for src, count in stats['top_sources']:
        lines.append(f"  {src}: {count}")
    return '\n'.join(lines)
