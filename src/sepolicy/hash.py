"""
Hash Module

Hash utilities.
"""

import hashlib


def hash_rule(source: str, target: str, tclass: str) -> str:
    """Generate hash for a rule."""
    s = f"{source}:{target}:{tclass}"
    return hashlib.md5(s.encode()).hexdigest()[:8]


def hash_content(content: str) -> str:
    """Hash content string."""
    return hashlib.sha256(content.encode()).hexdigest()
