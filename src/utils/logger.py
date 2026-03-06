"""Logging utilities for the bot."""
import logging
import sys
from datetime import datetime
import os

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Create logger
logger = logging.getLogger('OSRS_Bot')
logger.setLevel(logging.DEBUG)

# File handler - all logs
log_filename = f"logs/bot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
file_handler = logging.FileHandler(log_filename)
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
file_handler.setFormatter(file_formatter)

# Console handler - info and above
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
console_handler.setFormatter(console_formatter)

# Add handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def get_logger():
    """Get the logger instance."""
    return logger


def log_debug(msg):
    """Log debug message."""
    logger.debug(msg)


def log_info(msg):
    """Log info message."""
    logger.info(msg)


def log_warning(msg):
    """Log warning message."""
    logger.warning(msg)


def log_error(msg, exc_info=False):
    """Log error message."""
    logger.error(msg, exc_info=exc_info)


def log_critical(msg):
    """Log critical message."""
    logger.critical(msg)


# Print log file location on import
print(f"[LOGGING] Writing detailed logs to: {log_filename}")
