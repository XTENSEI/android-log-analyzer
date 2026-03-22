import os
import tempfile
import uuid
from pathlib import Path

class TempFileManager:
    def __init__(self):
        self.temp_files = []
    
    def create(self, suffix='', prefix='loganalyzer_'):
        fd, path = tempfile.mkstemp(suffix=suffix, prefix=prefix)
        os.close(fd)
        self.temp_files.append(path)
        return path
    
    def cleanup(self):
        for path in self.temp_files:
            try:
                os.unlink(path)
            except:
                pass
        self.temp_files.clear()
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.cleanup()
