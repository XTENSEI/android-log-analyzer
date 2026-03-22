"""
Utility Functions Module

Common utility functions for the sepolicy patcher.
"""

import os
import sys
import hashlib
from typing import List, Set, Optional
from datetime import datetime


def ensure_dir(path: str) -> None:
    """Ensure a directory exists."""
    os.makedirs(path, exist_ok=True)


def get_timestamp() -> str:
    """Get current timestamp as ISO format string."""
    return datetime.now().isoformat()


def format_size(size: int) -> str:
    """Format byte size to human readable string."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def compute_hash(content: str, algorithm: str = "md5") -> str:
    """Compute hash of content."""
    if algorithm == "md5":
        return hashlib.md5(content.encode()).hexdigest()
    elif algorithm == "sha1":
        return hashlib.sha1(content.encode()).hexdigest()
    elif algorithm == "sha256":
        return hashlib.sha256(content.encode()).hexdigest()
    raise ValueError(f"Unknown algorithm: {algorithm}")


def parse_perms_str(perms_str: str) -> Set[str]:
    """Parse permission string to set."""
    return set(perms_str.replace(',', ' ').split())


def format_perms(perms: Set[str]) -> str:
    """Format permissions set to string."""
    return '{ ' + ' '.join(sorted(perms)) + ' }'


def is_android_device() -> bool:
    """Check if running on Android."""
    return os.path.exists("/system/build.prop")


def get_android_version() -> Optional[str]:
    """Get Android version if on Android device."""
    try:
        with open("/system/build.prop", "r") as f:
            for line in f:
                if line.startswith("ro.build.version.release"):
                    return line.split("=")[1].strip()
    except:
        pass
    return None


def print_progress(current: int, total: int, prefix: str = "", bar_length: int = 40) -> None:
    """Print a progress bar."""
    if total == 0:
        return
    percent = current / total
    filled = int(bar_length * percent)
    bar = "=" * filled + "-" * (bar_length - filled)
    sys.stdout.write(f"\r{prefix} [{bar}] {int(percent * 100)}%")
    sys.stdout.flush()
    if current == total:
        print()


def truncate_string(s: str, max_len: int = 50, suffix: str = "...") -> str:
    """Truncate string to max length."""
    if len(s) <= max_len:
        return s
    return s[:max_len - len(suffix)] + suffix
