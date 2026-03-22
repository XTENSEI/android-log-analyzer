"""
AVC Denial Parser Module

Parses SELinux AVC denial messages from Android logs.
"""

import re
from dataclasses import dataclass, field
from typing import Optional, Set, Dict, Any
from datetime import datetime


AVC_PATTERN = re.compile(
    r'avc: +denied +\{ ([^}]+) \} .*?'
    r'(?:ioctlcmd=([0-9a-fx]+) )?.*?'
    r'scontext=u:r:([^:]+):s0.*?'
    r'tcontext=u:(?:object_r|r):([^:]+):s0.*?'
    r'tclass=([^\s]+).*?'
    r'(?:path="([^"]+)")?'
)

IOCTL_MAP = {
    '0x671e': 'perf_event ioctl',
    '0x5401': 'TCGETS',
    '0x5402': 'TCSETS',
    '0x5413': 'TIOCGWINSZ',
}


@dataclass
class AVCDenial:
    """Represents a single AVC denial entry."""
    source: str
    target: str
    tclass: str
    permissions: Set[str]
    ioctlcmd: Optional[str] = None
    path: Optional[str] = None
    raw: str = ""
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'source': self.source,
            'target': self.target,
            'class': self.tclass,
            'permissions': list(self.permissions),
            'ioctlcmd': self.ioctlcmd,
            'path': self.path,
            'raw': self.raw,
            'timestamp': self.timestamp,
        }


class AVCParser:
    """Parser for AVC denial messages."""
    
    def __init__(self):
        self.pattern = AVC_PATTERN
        self.stats = {
            'total_lines': 0,
            'parsed': 0,
            'unmatched': 0,
        }
    
    def parse_line(self, line: str) -> Optional[AVCDenial]:
        """Parse a single log line into an AVC denial."""
        self.stats['total_lines'] += 1
        
        match = self.pattern.search(line)
        if not match:
            self.stats['unmatched'] += 1
            return None
        
        self.stats['parsed'] += 1
        
        perms_str = match.group(1).strip()
        perms = set(perms_str.replace(',', ' ').split())
        
        return AVCDenial(
            source=match.group(3),
            target=match.group(4),
            tclass=match.group(5),
            permissions=perms,
            ioctlcmd=match.group(2),
            path=match.group(6),
            raw=line.strip(),
        )
    
    def parse_file(self, filepath: str) -> list:
        """Parse all AVC denials from a file."""
        denials = []
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                denial = self.parse_line(line)
                if denial:
                    denials.append(denial)
        return denials
    
    def get_stats(self) -> Dict[str, int]:
        """Get parsing statistics."""
        return self.stats.copy()


def parse_avc_line(line: str) -> Optional[Dict[str, Any]]:
    """
    Convenience function to parse a single AVC line.
    Returns a dictionary or None if not an AVC line.
    """
    parser = AVCParser()
    denial = parser.parse_line(line)
    if denial:
        return denial.to_dict()
    return None


def decode_ioctl(cmd: str) -> str:
    """Decode an ioctl command code to a human-readable name."""
    return IOCTL_MAP.get(cmd.lower(), f"unknown({cmd})")
