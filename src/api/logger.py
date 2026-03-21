import logging
from datetime import datetime

class RequestLogger:
    def __init__(self, filename: str = "api.log"):
        self.filename = filename
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(filename),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def log_request(self, method: str, path: str, status: int, duration_ms: float):
        self.logger.info(f"{method} {path} {status} {duration_ms}ms")
    
    def log_error(self, error: str):
        self.logger.error(error)
    
    def log_warning(self, warning: str):
        self.logger.warning(warning)

logger = RequestLogger()
