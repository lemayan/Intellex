"""Logging utilities for DeepScholar."""

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logger(
    name: str,
    log_dir: str = "./logs",
    log_level: str = "INFO",
    console_output: bool = True,
) -> logging.Logger:
    """
    Setup logger with file and console handlers.

    Args:
        name: Logger name
        log_dir: Directory to store log files
        log_level: Logging level
        console_output: Whether to output to console

    Returns:
        Configured logger instance
    """
    # Create log directory
    Path(log_dir).mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))

    # Remove existing handlers
    logger.handlers.clear()

    # Log format
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # File handler
    file_handler = logging.FileHandler(f"{log_dir}/{name}.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console handler
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name)
