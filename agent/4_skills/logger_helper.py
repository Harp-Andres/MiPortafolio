"""
Logger Helper - Provides get_logger function for skills

This module provides a get_logger function that skills can use.
Since skills are loaded dynamically with importlib, having a local
logger helper ensures it's available in the skill's namespace.
"""

import logging
from typing import Optional


def get_logger(name: str = "agent", level: Optional[int] = None) -> logging.Logger:
    """
    Get a logger instance with structured logging setup.
    
    Args:
        name: Logger name (usually __name__)
        level: Optional logging level override
    
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    
    if level is not None:
        logger.setLevel(level)
    
    return logger


__all__ = ["get_logger"]
