"""
Watch Module

Watch log files for changes and process new lines.
"""

import time
from typing import Callable, Optional
from pathlib import Path


class LogWatcher:
    """Watch a log file for new lines."""
    
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.position = 0
        self.running = False
    
    def start(self, callback: Callable[[str], None], interval: float = 1.0):
        """Start watching the file."""
        self.running = True
        path = Path(self.filepath)
        
        if path.exists():
            self.position = path.stat().st_size
        
        while self.running:
            if path.exists():
                size = path.stat().st_size
                if size > self.position:
                    with open(self.filepath, 'r') as f:
                        f.seek(self.position)
                        for line in f:
                            callback(line.strip())
                    self.position = size
            time.sleep(interval)
    
    def stop(self):
        """Stop watching."""
        self.running = False
