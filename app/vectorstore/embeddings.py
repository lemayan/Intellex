"""Embedding generation and management."""

from typing import List, Optional
import logging
import numpy as np
import hashlib

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None

from config.settings import get_settings
from app.utils.logger import get_logger

logger = get_logger(__name__)
settings = get_settings()


class EmbeddingManager:
    """Manage text embeddings using various providers."""

    def __init__(self, provider: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize embedding manager.

        Args:
            provider: Embedding provider (openai, huggingface, simple)
            model: Model name
        """
        self.provider = provider or settings.embedding_provider or "simple"
        self.embedding_cache = {}
        
        # Set model based on provider
        if self.provider == "openai":
            self.model = model or settings.embedding_model
        elif self.provider == "huggingface":
            self.model = model or settings.huggingface_model
        elif self.provider == "simple":
            self.model = "simple-hash-384"
        else:
            # Default to simple if anything else
            self.provider = "simple"
            self.model = "simple-hash-384"
        
        self._initialize_provider()

    def _initialize_provider(self):
        """Initialize the embedding provider."""
        if self.provider == "openai":
            if not OpenAI:
                logger.warning("openai package not available, falling back to simple embeddings")
                self.provider = "simple"
            else:
                self.client = OpenAI(api_key=settings.openai_api_key)
                logger.info(f"Initialized OpenAI embeddings with model: {self.model}")

        elif self.provider == "huggingface":
            if SentenceTransformer:
                self.model_instance = SentenceTransformer(self.model)
                logger.info(f"Initialized HuggingFace embeddings with model: {self.model}")
            else:
                logger.warning("sentence-transformers not available, falling back to simple embeddings")
                self.provider = "simple"

        if self.provider == "simple":
            logger.info("Using simple hash-based embeddings (no external dependencies)")

    def embed_text(self, text: str) -> np.ndarray:
        """
        Generate embedding for a single text.

        Args:
            text: Text to embed

        Returns:
            Embedding vector
        """
        # Check cache
        if text in self.embedding_cache:
            return self.embedding_cache[text]

        if self.provider == "openai":
            embedding = self._embed_openai([text])[0]
        elif self.provider == "huggingface":
            embedding = self._embed_huggingface([text])[0]
        elif self.provider == "simple":
            embedding = self._embed_simple([text])[0]
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

        # Cache the embedding
        self.embedding_cache[text] = embedding
        return embedding

    def embed_texts(self, texts: List[str], batch_size: int = 100) -> List[np.ndarray]:
        """
        Generate embeddings for multiple texts.

        Args:
            texts: List of texts to embed
            batch_size: Batch size for processing

        Returns:
            List of embedding vectors
        """
        embeddings = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]

            # Filter out cached items
            uncached = [t for t in batch if t not in self.embedding_cache]

            if uncached:
                if self.provider == "openai":
                    batch_embeddings = self._embed_openai(uncached)
                elif self.provider == "huggingface":
                    batch_embeddings = self._embed_huggingface(uncached)
                elif self.provider == "simple":
                    batch_embeddings = self._embed_simple(uncached)
                else:
                    raise ValueError(f"Unsupported provider: {self.provider}")

                # Cache embeddings
                for text, emb in zip(uncached, batch_embeddings):
                    self.embedding_cache[text] = emb

            # Gather all embeddings (cached + new)
            for text in batch:
                embeddings.append(self.embedding_cache[text])

        return embeddings

    def _embed_openai(self, texts: List[str]) -> List[np.ndarray]:
        """Generate embeddings using OpenAI API."""
        try:
            response = self.client.embeddings.create(input=texts, model=self.model)
            return [np.array(item.embedding) for item in response.data]
        except Exception as e:
            logger.error(f"Error generating OpenAI embeddings: {str(e)}")
            raise

    def _embed_huggingface(self, texts: List[str]) -> List[np.ndarray]:
        """Generate embeddings using HuggingFace model."""
        try:
            embeddings = self.model_instance.encode(
                texts, convert_to_numpy=True, show_progress_bar=False
            )
            return [np.array(e) for e in embeddings]
        except Exception as e:
            logger.error(f"Error generating HuggingFace embeddings: {str(e)}")
            raise

    def _embed_simple(self, texts: List[str]) -> List[np.ndarray]:
        """Generate simple hash-based embeddings (no external dependencies)."""
        embeddings = []
        for text in texts:
            # Create a 384-dimensional embedding using hash and character analysis
            hash_obj = hashlib.sha256(text.encode())
            hash_bytes = hash_obj.digest()
            
            # Start with hash values
            embedding = list(hash_bytes[:32]) + [0] * (384 - 32)
            
            # Add character frequency features
            for i, char in enumerate(text[:100]):
                embedding[32 + (i % (384 - 32))] += ord(char) % 256
            
            # Normalize
            embedding = np.array(embedding, dtype=np.float32)
            embedding = embedding / (np.linalg.norm(embedding) + 1e-10)
            embeddings.append(embedding)
        
        return embeddings

    def get_embedding_dimension(self) -> int:
        """Get the dimension of embeddings."""
        if self.provider == "openai":
            # OpenAI text-embedding-3-small is 1536, text-embedding-3-large is 3072
            return 1536 if "small" in self.model else 3072
        elif self.provider == "huggingface":
            # Get from model
            test_embedding = self._embed_huggingface(["test"])[0]
            return len(test_embedding)
        elif self.provider == "simple":
            # Simple embeddings are 384-dimensional
            return 384
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def clear_cache(self):
        """Clear the embedding cache."""
        self.embedding_cache.clear()
        logger.info("Cleared embedding cache")
