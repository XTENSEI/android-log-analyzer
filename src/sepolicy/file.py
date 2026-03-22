"""
File Module

File I/O utilities.
"""

from pathlib import Path


def read_file(path: str) -> str:
    """Read entire file."""
    with open(path, 'r') as f:
        return f.read()


def write_file(path: str, content: str) -> None:
    """Write content to file."""
    with open(path, 'w') as f:
        f.write(content)
