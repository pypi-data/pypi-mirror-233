import logging
from .config import LOGGING_LEVEL

# Setting up logging configuration
logging.basicConfig(level=LOGGING_LEVEL, format='%(levelname)s: %(message)s')

def set_logger_level(level):
    """
    Set the logger's level based on user input.
    
    Args:
        level (str): The desired logging level, e.g., 'DEBUG', 'INFO', 'WARNING', etc.
    """
    valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    
    if level.upper() not in valid_levels:
        raise ValueError(f"Invalid log level: {level}. Valid levels: {', '.join(valid_levels)}")
    
    logging.getLogger().setLevel(getattr(logging, level.upper()))

def log_debug(message):
    logging.debug(message)

def log_info(message):
    logging.info(message)

def log_warning(message):
    logging.warning(message)

def log_error(message):
    logging.error(message)

def log_critical(message):
    logging.critical(message)
