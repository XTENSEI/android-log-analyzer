from typing import Optional
from pydantic import BaseModel

class Config:
    def __init__(self):
        self.binary_path: str = "../core/target/release/loganalyzer"
        self.max_file_size_mb: int = 500
        self.timeout_seconds: int = 300
        self.cache_ttl_seconds: int = 300
        self.api_host: str = "0.0.0.0"
        self.api_port: int = 8000

config = Config()
