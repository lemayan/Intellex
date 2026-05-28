"""Validation utilities for DeepScholar."""

import os
from pathlib import Path
from typing import List, Optional
from urllib.parse import urlparse


def validate_file(file_path: str, allowed_extensions: Optional[List[str]] = None) -> bool:
    """
    Validate if file exists and has allowed extension.

    Args:
        file_path: Path to file
        allowed_extensions: List of allowed extensions (e.g., ['.pdf', '.txt'])

    Returns:
        True if valid, False otherwise
    """
    path = Path(file_path)

    if not path.exists():
        return False

    if not path.is_file():
        return False

    if allowed_extensions:
        return path.suffix.lower() in [ext.lower() for ext in allowed_extensions]

    return True


def validate_url(url: str) -> bool:
    """
    Validate if string is a valid URL.

    Args:
        url: URL string to validate

    Returns:
        True if valid URL, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def validate_api_keys(required_keys: List[str]) -> bool:
    """
    Validate if required API keys are set.

    Args:
        required_keys: List of environment variable names

    Returns:
        True if all keys are set, False otherwise
    """
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    if missing_keys:
        print(f"Missing API keys: {', '.join(missing_keys)}")
        return False
    return True


def validate_document_size(file_path: str, max_size_mb: int = 100) -> bool:
    """
    Validate document file size.

    Args:
        file_path: Path to file
        max_size_mb: Maximum size in MB

    Returns:
        True if size is valid, False otherwise
    """
    try:
        file_size_mb = Path(file_path).stat().st_size / (1024 * 1024)
        return file_size_mb <= max_size_mb
    except Exception:
        return False
