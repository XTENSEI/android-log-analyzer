"""
Logging Module

Logging utilities for sepolicy patcher.
"""

import logging
import sys
from typing import Optional


def setup_logger(
    name: str = "sepolicy",
    level: int = logging.INFO,
    log_file: Optional[str] = None
) -> logging.Logger:
    """Setup and return a logger."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str = "sepolicy") -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name)
