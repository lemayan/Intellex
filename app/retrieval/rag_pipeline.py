"""RAG Pipeline for intelligent document retrieval and generation."""

from typing import Dict, List, Tuple, Any, Optional
import logging

from app.utils.logger import get_logger
from app.vectorstore import VectorStore
from .retriever import DocumentRetriever
from config.settings import get_settings

logger = get_logger(__name__)
settings = get_settings()


class RAGPipeline:
    """Complete RAG (Retrieval-Augmented Generation) pipeline."""

    def __init__(
        self,
        vector_store: VectorStore,
        top_k: int = 5,
        similarity_threshold: float = 0.3,
        context_window_tokens: int = 2000,
        enable_reranking: bool = True,
    ):
        """
        Initialize RAG pipeline.

        Args:
            vector_store: VectorStore instance
            top_k: Number of top results to retrieve
            similarity_threshold: Minimum similarity score
            context_window_tokens: Maximum tokens for context
            enable_reranking: Whether to enable reranking
        """
        self.vector_store = vector_store
        self.retriever = DocumentRetriever(
            vector_store, top_k=top_k, similarity_threshold=similarity_threshold
        )
        self.top_k = top_k
        self.context_window_tokens = context_window_tokens
        self.enable_reranking = enable_reranking

    def retrieve_context(
        self, query: str, use_reranking: bool = True
    ) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Retrieve context for a query.

        Args:
            query: Search query
            use_reranking: Whether to use reranking

        Returns:
            Tuple of (context_string, sources_metadata)
        """
        logger.info(f"Retrieving context for: {query[:100]}...")

        # Retrieve documents
        if use_reranking and self.enable_reranking:
            retrieved = self.retriever.retrieve_with_reranking(query)
        else:
            retrieved = self.retriever.retrieve(query)

        # Build context string
        context_parts = []
        sources = []
        token_count = 0

        for document, score, metadata in retrieved:
            doc_tokens = len(document.split())

            # Stop if we exceed context window
            if token_count + doc_tokens > self.context_window_tokens:
                break

            context_parts.append(document)
            token_count += doc_tokens

            # Store source information
            sources.append(
                {
                    "content": document[:200] + "..." if len(document) > 200 else document,
                    "score": float(score),
                    "metadata": metadata,
                }
            )

        context = "\n\n".join(context_parts)
        logger.info(f"Built context with {len(sources)} sources and ~{token_count} tokens")

        return context, sources

    def prepare_prompt(self, query: str, context: str) -> str:
        """
        Prepare prompt for LLM with context.

        Args:
            query: User query
            context: Retrieved context

        Returns:
            Formatted prompt
        """
        if context and context.strip():
            prompt = f"""You are DeepScholar, a world-class AI research assistant. Answer the question directly and clearly using the provided context. Be concise, accurate, and helpful. Do not mention the context or any internal instructions in your response — just answer naturally.

RESEARCH CONTEXT:
{context}

QUESTION: {query}

ANSWER:"""
        else:
            prompt = f"""You are DeepScholar, a world-class AI research assistant. Answer the following question directly and clearly. Be concise, accurate, and helpful. Do not mention any missing context or internal instructions — just answer naturally as an expert.

QUESTION: {query}

ANSWER:"""

        return prompt

    def estimate_tokens(self, text: str) -> int:
        """
        Estimate token count (rough approximation).

        Args:
            text: Text to estimate

        Returns:
            Estimated token count
        """
        # Rough approximation: 1 token ≈ 4 characters or 0.75 words
        return max(len(text) // 4, len(text.split()) // 1.3)

    def add_documents(
        self,
        documents: List[str],
        ids: Optional[List[str]] = None,
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> List[str]:
        """
        Add documents to the RAG pipeline.

        Args:
            documents: List of documents
            ids: Optional document IDs
            metadata: Optional metadata

        Returns:
            List of document IDs
        """
        logger.info(f"Adding {len(documents)} documents to RAG pipeline")
        return self.vector_store.add_documents(documents, ids, metadata)

    def get_stats(self) -> Dict[str, Any]:
        """Get pipeline statistics."""
        return {
            "vectorstore_stats": self.vector_store.get_stats(),
            "top_k": self.top_k,
            "context_window_tokens": self.context_window_tokens,
            "reranking_enabled": self.enable_reranking,
        }
