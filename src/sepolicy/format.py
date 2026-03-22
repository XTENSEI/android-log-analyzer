"""
Format Module

Format detection and handling.
"""

import os
from pathlib import Path


def detect_format(filepath: str) -> str:
    """Detect the format of a file based on extension."""
    ext = Path(filepath).suffix.lower()
    
    if ext == '.json':
        return 'json'
    elif ext in ['.te', '.mod']:
        return 'te'
    elif ext == '.cil':
        return 'cil'
    elif ext == '.csv':
        return 'csv'
    elif ext == '.md':
        return 'md'
    else:
        return 'log'


def get_format_from_content(content: str) -> str:
    """Detect format from file content."""
    content = content.strip()
    
    if content.startswith('[') or content.startswith('{'):
        return 'json'
    elif 'allow ' in content:
        return 'te'
    elif '(allow ' in content:
        return 'cil'
    else:
        return 'unknown'
