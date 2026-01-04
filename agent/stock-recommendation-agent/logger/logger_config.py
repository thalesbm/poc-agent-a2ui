"""
Simple logging system for demo purposes.
"""

import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S'
)

def get_logger(name: str) -> logging.Logger:
    """
    Returns a simple logger instance.
    
    Args:
        name: Logger name (typically __name__ of the calling module)
        
    Returns:
        A configured logger instance
    """
    return logging.getLogger(name)