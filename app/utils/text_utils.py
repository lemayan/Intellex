"""Text processing utilities."""

import re
from typing import List


def truncate_text(text: str, max_length: int = 500, suffix: str = "...") -> str:
    """
    Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to append

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def clean_text(text: str) -> str:
    """
    Clean text by removing extra whitespace and special characters.

    Args:
        text: Text to clean

    Returns:
        Cleaned text
    """
    # Remove extra whitespace
    text = " ".join(text.split())
    # Remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)
    return text.strip()


def split_text_into_sentences(text: str) -> List[str]:
    """
    Split text into sentences.

    Args:
        text: Text to split

    Returns:
        List of sentences
    """
    # Simple sentence splitting
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return [s.strip() for s in sentences if s.strip()]


def extract_keywords(text: str, num_keywords: int = 10) -> List[str]:
    """
    Extract keywords from text using simple TF-IDF approach.

    Args:
        text: Text to analyze
        num_keywords: Number of keywords to extract

    Returns:
        List of keywords
    """
    words = re.findall(r"\b[a-z]+\b", text.lower())
    word_freq = {}

    for word in words:
        if len(word) > 3:  # Filter short words
            word_freq[word] = word_freq.get(word, 0) + 1

    # Sort by frequency
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    return [word for word, _ in sorted_words[:num_keywords]]


def calculate_similarity_score(text1: str, text2: str) -> float:
    """
    Calculate simple text similarity score.

    Args:
        text1: First text
        text2: Second text

    Returns:
        Similarity score between 0 and 1
    """
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())

    if not words1 or not words2:
        return 0.0

    intersection = len(words1.intersection(words2))
    union = len(words1.union(words2))

    return intersection / union if union > 0 else 0.0
