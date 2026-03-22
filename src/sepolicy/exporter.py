"""
Exporter Module

Export rules to various formats.
"""

import json
import csv
from typing import Dict, Any
from pathlib import Path
from .rules import RuleSet


def export_to_dict(ruleset: RuleSet) -> Dict[str, Any]:
    """Export rules to dictionary format."""
    return {
        'rules': [
            {
                'source': src,
                'target': tgt,
                'class': cls,
                'permissions': perms,
            }
            for src, tgt, cls, perms in ruleset.get_all_rules()
        ],
        'summary': {
            'total': ruleset.count(),
            'sources': list(ruleset.get_unique_sources()),
            'targets': list(ruleset.get_unique_targets()),
        }
    }


def export_to_text(ruleset: RuleSet) -> str:
    """Export rules to plain text format."""
    lines = []
    for src, tgt, cls, perms in ruleset.get_all_rules():
        lines.append(f"allow {src} {tgt}:{cls} {{ {' '.join(perms)} }};")
    return '\n'.join(lines)


def export_summary(ruleset: RuleSet) -> str:
    """Export a summary of the rules."""
    lines = []
    lines.append("SELinux Policy Rules Summary")
    lines.append("=" * 40)
    lines.append(f"Total Rules: {ruleset.count()}")
    lines.append(f"Unique Sources: {len(ruleset.get_unique_sources())}")
    lines.append(f"Unique Targets: {len(ruleset.get_unique_targets())}")
    return '\n'.join(lines)
