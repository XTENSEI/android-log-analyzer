"""
Parse Module

Parse helper functions.
"""

from typing import Optional, Tuple


def parse_rule_line(line: str) -> Optional[Tuple[str, str, str, list]]:
    """Parse a single allow rule line."""
    if not line.strip().startswith('allow '):
        return None
    
    parts = line[6:].strip().split(':')
    if len(parts) != 2:
        return None
    
    src_tgt, cls_perms = parts
    cls_parts = cls_perms.strip().split()
    cls = cls_parts[0]
    perms = cls_parts[1].strip('{}').split() if len(cls_parts) > 1 else []
    
    st_parts = src_tgt.strip().split()
    src = st_parts[0]
    tgt = st_parts[1] if len(st_parts) > 1 else ''
    
    return (src, tgt, cls, perms)
