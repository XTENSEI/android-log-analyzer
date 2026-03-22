"""
Batch Module

Batch processing utilities.
"""

from typing import List
from pathlib import Path
from .parser import AVCParser
from .rules import RuleSet


def process_files(filepaths: List[str], merge: bool = False) -> RuleSet:
    """Process multiple files and return combined rules."""
    ruleset = RuleSet(merge_permissions=merge)
    parser = AVCParser()
    
    for filepath in filepaths:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                denial = parser.parse_line(line)
                if denial:
                    ruleset.add_denial(denial.to_dict())
    
    return ruleset


def process_directory(dirpath: str, pattern: str = "*.log", merge: bool = False) -> RuleSet:
    """Process all matching files in a directory."""
    path = Path(dirpath)
    files = list(path.glob(pattern))
    filepaths = [str(f) for f in files]
    return process_files(filepaths, merge)
