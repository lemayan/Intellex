"""Vector database module for DeepScholar."""

from .embeddings import EmbeddingManager
from .vector_store import VectorStore

__all__ = ["EmbeddingManager", "VectorStore"]
