"""
Path Module

Path utilities.
"""

import os
from pathlib import Path
from typing import List


def find_logs(directory: str, pattern: str = "*.log") -> List[str]:
    """Find all log files in a directory."""
    path = Path(directory)
    return [str(f) for f in path.glob(pattern)]


def ensure_directory(path: str) -> None:
    """Ensure directory exists."""
    os.makedirs(path, exist_ok=True)


def get_file_size(path: str) -> int:
    """Get file size in bytes."""
    return os.path.getsize(path)
