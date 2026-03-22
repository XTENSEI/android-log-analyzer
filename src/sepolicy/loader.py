"""
Loader Module

Load rules from various file formats.
"""

import json
import csv
from typing import List, Dict, Any
from pathlib import Path
from .rules import RuleSet


def load_from_json(filepath: str) -> RuleSet:
    """Load rules from JSON file."""
    ruleset = RuleSet()
    
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    rules = data if isinstance(data, list) else data.get('rules', [])
    
    for rule in rules:
        denial = {
            'source': rule.get('source', ''),
            'target': rule.get('target', ''),
            'class': rule.get('class', ''),
            'permissions': set(rule.get('permissions', [])),
        }
        ruleset.add_denial(denial)
    
    return ruleset


def load_from_csv(filepath: str) -> RuleSet:
    """Load rules from CSV file."""
    ruleset = RuleSet()
    
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            denial = {
                'source': row.get('source', ''),
                'target': row.get('target', ''),
                'class': row.get('class', ''),
                'permissions': set(row.get('permissions', '').split()),
            }
            ruleset.add_denial(denial)
    
    return ruleset


def load_from_text(filepath: str) -> RuleSet:
    """Load rules from plain text TE format."""
    ruleset = RuleSet()
    
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            if line.startswith('allow '):
                parts = line[6:].split(':')
                if len(parts) == 2:
                    src_tgt, cls_perms = parts
                    cls_parts = cls_perms.split()
                    cls = cls_parts[0]
                    perms_str = cls_parts[1] if len(cls_parts) > 1 else ''
                    perms = perms_str.strip('{}').split()
                    
                    src_tgt_parts = src_tgt.split()
                    src = src_tgt_parts[0]
                    tgt = src_tgt_parts[1] if len(src_tgt_parts) > 1 else ''
                    
                    denial = {
                        'source': src,
                        'target': tgt,
                        'class': cls,
                        'permissions': set(perms),
                    }
                    ruleset.add_denial(denial)
    
    return ruleset
