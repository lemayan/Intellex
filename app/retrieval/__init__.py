"""Retrieval module for DeepScholar."""

from .rag_pipeline import RAGPipeline
from .retriever import DocumentRetriever

__all__ = ["RAGPipeline", "DocumentRetriever"]
