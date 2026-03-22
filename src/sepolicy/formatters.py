"""
Output Formatters Module

Provides various output formats for SELinux rules:
- CIL (Common Intermediate Language)
- TE (Type Enforcement)
- JSON
- CSV
- Markdown
"""

import json
import csv
from typing import List, Tuple, Dict, Any, Optional
from pathlib import Path
from datetime import datetime


def format_cil(src: str, tgt: str, cls: str, perms: List[str]) -> List[str]:
    """Format rule(s) in CIL format."""
    return [f'(allow {src} {tgt} ({cls} ({perm})))' for perm in perms]


def format_te(src: str, tgt: str, cls: str, perms: List[str]) -> List[str]:
    """Format rule(s) in Type Enforcement format."""
    if len(perms) == 1:
        return [f'allow {src} {tgt}:{cls} {perms[0]};']
    return [f'allow {src} {tgt}:{cls} {{ {" ".join(perms)} }};']


def format_rules_cil(rules: List[Tuple[str, str, str, List[str]]]) -> List[str]:
    """Format all rules in CIL format."""
    lines = []
    for src, tgt, cls, perms in sorted(rules):
        lines.extend(format_cil(src, tgt, cls, perms))
    return lines


def format_rules_te(rules: List[Tuple[str, str, str, List[str]]]) -> List[str]:
    """Format all rules in TE format."""
    lines = []
    for src, tgt, cls, perms in sorted(rules):
        lines.extend(format_te(src, tgt, cls, perms))
    return lines


def write_rules_file(
    rules: List[Tuple[str, str, str, List[str]]],
    output_path: str,
    format_type: str = 'cil',
    header: bool = True,
    comments: Optional[List[str]] = None,
) -> None:
    """Write rules to a file in the specified format."""
    if format_type == 'cil':
        lines = format_rules_cil(rules)
    elif format_type == 'te':
        lines = format_rules_te(rules)
    else:
        raise ValueError(f"Unsupported format: {format_type}")
    
    with open(output_path, 'w') as f:
        if header:
            f.write(f"# SELinux policy generated on {datetime.now().isoformat()}\n")
            f.write("# Review and adjust permissions as needed.\n\n")
        
        if comments:
            for comment in comments:
                f.write(f"# {comment}\n")
            f.write("\n")
        
        for line in lines:
            f.write(f"{line}\n")


def export_json(ruleset, outfile: str, include_metadata: bool = False) -> None:
    """Export rules to JSON format."""
    data = []
    for rule in ruleset.get_rule_objects():
        entry = rule.to_dict()
        if include_metadata:
            entry['metadata'] = [
                {'raw': raw, 'timestamp': ts}
                for raw, ts in rule.metadata
            ]
        data.append(entry)
    
    with open(outfile, 'w') as f:
        json.dump(data, f, indent=2)


def export_csv(ruleset, outfile: str) -> None:
    """Export rules to CSV format."""
    with open(outfile, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['source', 'target', 'class', 'permissions'])
        for src, tgt, cls, perms in ruleset.get_all_rules():
            writer.writerow([src, tgt, cls, ' '.join(perms)])


def export_markdown(ruleset, outfile: str) -> None:
    """Export rules to Markdown table format."""
    with open(outfile, 'w') as f:
        f.write("# SELinux Allow Rules\n\n")
        f.write("| Source | Target | Class | Permissions |\n")
        f.write("|--------|--------|-------|-------------|\n")
        for src, tgt, cls, perms in ruleset.get_all_rules():
            f.write(f"| {src} | {tgt} | {cls} | {' '.join(perms)} |\n")


def export_rules(
    ruleset,
    outfile: str,
    format_type: str = 'cil',
    include_metadata: bool = False,
) -> None:
    """Export rules in the specified format."""
    if format_type == 'json':
        export_json(ruleset, outfile, include_metadata)
    elif format_type == 'csv':
        export_csv(ruleset, outfile)
    elif format_type == 'md':
        export_markdown(ruleset, outfile)
    else:
        write_rules_file(ruleset.get_all_rules(), outfile, format_type)
