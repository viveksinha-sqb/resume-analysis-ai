import logging
import sys
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name: str = "resume_ai"):
    """
    Sets up a centralized logger with console and file handlers.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Prevent adding handlers multiple times
    if logger.hasHandlers():
        return logger

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File Handler
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    file_handler = RotatingFileHandler(
        "logs/app.log", maxBytes=10485760, backupCount=5
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

logger = setup_logger()
