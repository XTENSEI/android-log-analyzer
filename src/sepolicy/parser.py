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

LOGCAT_AVC_PATTERN = re.compile(
    r'avc: +denied +\{ ([^}]+) \} .*?'
    r'(?:for +pid=(-?\d+) )?'
    r'(?:uid=(-?\d+) )?'
    r'(?:name=([^=\s]+) )?'
    r'(?:comm="([^"]+)" )?'
    r'scontext=u:r:([^:]+):s0.*?'
    r'tcontext=u:(?:object_r|r):([^:]+):s0.*?'
    r'tclass=([^\s]+).*?'
    r'(?:app=([^\s]+) )?'
    r'permissive=([01])'
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
    comm: Optional[str] = None
    pid: Optional[int] = None
    app: Optional[str] = None
    permissive: bool = False
    
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
            'comm': self.comm,
            'pid': self.pid,
            'app': self.app,
            'permissive': self.permissive,
        }
    
    def generate_policy_rule(self) -> str:
        """Generate an allow rule for this denial."""
        return f"allow {self.source} {self.target}:{self.tclass} {','.join(self.permissions)};"


class AVCParser:
    """Parser for AVC denial messages."""
    
    def __init__(self):
        self.pattern = AVC_PATTERN
        self.logcat_pattern = LOGCAT_AVC_PATTERN
        self.stats = {
            'total_lines': 0,
            'parsed': 0,
            'unmatched': 0,
        }
    
    def parse_line(self, line: str) -> Optional[AVCDenial]:
        """Parse a single log line into an AVC denial."""
        self.stats['total_lines'] += 1
        
        denial = self._parse_logcat_pattern(line)
        if denial:
            self.stats['parsed'] += 1
            return denial
        
        denial = self._parse_with_pattern(line, self.pattern)
        if denial:
            self.stats['parsed'] += 1
            return denial
        
        self.stats['unmatched'] += 1
        return None
    
    def _parse_with_pattern(self, line: str, pattern: re.Pattern) -> Optional[AVCDenial]:
        """Parse using a specific pattern."""
        match = pattern.search(line)
        if not match:
            return None
        
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
    
    def _parse_logcat_pattern(self, line: str) -> Optional[AVCDenial]:
        """Parse using the logcat AVC pattern."""
        match = self.logcat_pattern.search(line)
        if not match:
            return None
        
        perms_str = match.group(1).strip()
        perms = set(perms_str.replace(',', ' ').split())
        
        pid_str = match.group(2)
        pid = int(pid_str) if pid_str else None
        
        permissive_str = match.group(10)
        permissive = permissive_str == '1' if permissive_str else False
        
        return AVCDenial(
            source=match.group(6),
            target=match.group(7),
            tclass=match.group(8),
            permissions=perms,
            comm=match.group(5),
            pid=pid,
            app=match.group(9) if match.group(9) else None,
            permissive=permissive,
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
