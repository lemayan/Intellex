"""Document retriever for RAG."""

from typing import List, Tuple, Dict, Any, Optional
import logging
from app.vectorstore import VectorStore
from app.utils.logger import get_logger
from config.settings import get_settings

logger = get_logger(__name__)
settings = get_settings()


class DocumentRetriever:
    """Retrieve relevant documents from vector store."""

    def __init__(
        self,
        vector_store: VectorStore,
        top_k: int = 5,
        similarity_threshold: float = 0.3,
    ):
        """
        Initialize document retriever.

        Args:
            vector_store: VectorStore instance
            top_k: Number of top results to retrieve
            similarity_threshold: Minimum similarity score
        """
        self.vector_store = vector_store
        self.top_k = top_k
        self.similarity_threshold = similarity_threshold

    def retrieve(self, query: str) -> List[Tuple[str, float, Dict]]:
        """
        Retrieve relevant documents for a query.

        Args:
            query: Search query

        Returns:
            List of (document, score, metadata) tuples
        """
        logger.info(f"Retrieving documents for query: {query[:100]}...")

        results = self.vector_store.search(
            query=query, top_k=self.top_k, threshold=self.similarity_threshold
        )

        logger.info(f"Retrieved {len(results)} relevant documents")
        return results

    def retrieve_with_reranking(
        self, query: str, rerank_top_k: Optional[int] = None
    ) -> List[Tuple[str, float, Dict]]:
        """
        Retrieve documents with reranking.

        Args:
            query: Search query
            rerank_top_k: Number of documents to return after reranking

        Returns:
            List of (document, score, metadata) tuples
        """
        # Initial retrieval
        initial_results = self.retrieve(query)

        if not initial_results:
            return []

        # Simple reranking based on query-document overlap
        reranked = self._rerank_results(query, initial_results)

        # Return top-k after reranking
        final_k = rerank_top_k or self.top_k
        return reranked[:final_k]

    @staticmethod
    def _rerank_results(
        query: str, results: List[Tuple[str, float, Dict]]
    ) -> List[Tuple[str, float, Dict]]:
        """
        Rerank results based on relevance.

        Args:
            query: Search query
            results: Initial results

        Returns:
            Reranked results
        """
        query_terms = set(query.lower().split())

        def compute_relevance_score(document: str, original_score: float) -> float:
            """Compute relevance score combining similarity and term overlap."""
            doc_terms = set(document.lower().split())
            overlap = len(query_terms.intersection(doc_terms)) / len(query_terms)
            return original_score * 0.6 + overlap * 0.4

        # Recompute scores
        reranked = [
            (doc, compute_relevance_score(doc, score), meta)
            for doc, score, meta in results
        ]

        # Sort by new scores
        return sorted(reranked, key=lambda x: x[1], reverse=True)

    def get_context(self, query: str, max_tokens: int = 2000) -> str:
        """
        Get context from retrieved documents.

        Args:
            query: Search query
            max_tokens: Maximum tokens for context

        Returns:
            Context string
        """
        documents = self.retrieve(query)

        context_parts = []
        token_count = 0

        for doc, score, meta in documents:
            # Estimate tokens (rough approximation)
            doc_tokens = len(doc.split())

            if token_count + doc_tokens > max_tokens:
                break

            context_parts.append(doc)
            token_count += doc_tokens

        return "\n\n".join(context_parts)
