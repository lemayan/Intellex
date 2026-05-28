"""Vector store implementation using FAISS and ChromaDB."""

from typing import List, Dict, Tuple, Optional, Any
import json
import logging
from pathlib import Path
import numpy as np

try:
    import faiss
except ImportError:
    faiss = None

try:
    import chromadb
except ImportError:
    chromadb = None

from config.settings import get_settings
from app.utils.logger import get_logger
from .embeddings import EmbeddingManager

logger = get_logger(__name__)
settings = get_settings()


class VectorStore:
    """Vector store for semantic search and retrieval."""

    def __init__(
        self,
        db_type: Optional[str] = None,
        db_path: Optional[str] = None,
        embedding_manager: Optional[EmbeddingManager] = None,
    ):
        """
        Initialize vector store.

        Args:
            db_type: Database type (faiss or chroma)
            db_path: Path to store database
            embedding_manager: EmbeddingManager instance
        """
        self.db_type = db_type or settings.vectordb_type
        self.db_path = db_path or settings.vectordb_path
        self.embedding_manager = embedding_manager or EmbeddingManager()
        self.metadata_store = {}
        self.index = None
        self.documents = []
        self.ids = []

        self._initialize_store()

    def _initialize_store(self):
        """Initialize the vector store backend."""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

        if self.db_type == "faiss":
            self._initialize_faiss()
        elif self.db_type == "chroma":
            self._initialize_chroma()
        else:
            raise ValueError(f"Unsupported vector database type: {self.db_type}")

        logger.info(f"Initialized {self.db_type} vector store at {self.db_path}")

    def _initialize_faiss(self):
        """Initialize FAISS index."""
        if not faiss:
            raise ImportError("faiss-cpu or faiss-gpu is required for FAISS backend")

        # Check if index already exists
        index_path = f"{self.db_path}/index.faiss"
        metadata_path = f"{self.db_path}/metadata.json"

        if Path(index_path).exists():
            try:
                self.index = faiss.read_index(index_path)
                with open(metadata_path, "r") as f:
                    data = json.load(f)
                    self.documents = data.get("documents", [])
                    self.ids = data.get("ids", [])
                    self.metadata_store = data.get("metadata", {})
                logger.info("Loaded existing FAISS index")
            except Exception as e:
                logger.warning(f"Could not load existing FAISS index: {str(e)}")
                self._create_faiss_index()
        else:
            self._create_faiss_index()

    def _create_faiss_index(self):
        """Create new FAISS index."""
        embedding_dim = self.embedding_manager.get_embedding_dimension()
        self.index = faiss.IndexFlatL2(embedding_dim)
        logger.info(f"Created new FAISS index with dimension {embedding_dim}")

    def _initialize_chroma(self):
        """Initialize ChromaDB."""
        if not chromadb:
            raise ImportError("chromadb is required for ChromaDB backend")

        try:
            self.chroma_client = chromadb.PersistentClient(path=self.db_path)
            self.chroma_collection = self.chroma_client.get_or_create_collection(
                name="deepscholar_documents"
            )
            logger.info("Initialized ChromaDB")
        except Exception as e:
            logger.error(f"Error initializing ChromaDB: {str(e)}")
            raise

    def add_documents(
        self,
        documents: List[str],
        ids: Optional[List[str]] = None,
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> List[str]:
        """
        Add documents to the vector store.

        Args:
            documents: List of documents
            ids: Optional document IDs
            metadata: Optional metadata for each document

        Returns:
            List of document IDs
        """
        if not documents:
            return []

        # Generate IDs if not provided
        if ids is None:
            ids = [f"doc_{i}_{hash(doc) % 10000}" for i, doc in enumerate(documents)]

        # Generate embeddings
        logger.info(f"Generating embeddings for {len(documents)} documents")
        embeddings = self.embedding_manager.embed_texts(documents)

        if self.db_type == "faiss":
            self._add_to_faiss(documents, ids, embeddings, metadata)
        elif self.db_type == "chroma":
            self._add_to_chroma(documents, ids, embeddings, metadata)

        logger.info(f"Added {len(documents)} documents to vector store")
        return ids

    def _add_to_faiss(
        self,
        documents: List[str],
        ids: List[str],
        embeddings: List[np.ndarray],
        metadata: Optional[List[Dict[str, Any]]] = None,
    ):
        """Add documents to FAISS index."""
        # Convert to numpy array
        embeddings_array = np.array(embeddings).astype("float32")

        # Add to index
        self.index.add(embeddings_array)

        # Store documents and metadata
        self.documents.extend(documents)
        self.ids.extend(ids)

        if metadata:
            for doc_id, meta in zip(ids, metadata):
                self.metadata_store[doc_id] = meta
        else:
            for doc_id in ids:
                self.metadata_store[doc_id] = {}

        # Save to disk
        self._save_faiss_index()

    def _add_to_chroma(
        self,
        documents: List[str],
        ids: List[str],
        embeddings: List[np.ndarray],
        metadata: Optional[List[Dict[str, Any]]] = None,
    ):
        """Add documents to ChromaDB."""
        # Convert embeddings to lists
        embeddings_lists = [emb.tolist() for emb in embeddings]

        # Prepare metadata
        meta_list = metadata or [{} for _ in documents]

        try:
            self.chroma_collection.add(
                documents=documents,
                embeddings=embeddings_lists,
                metadatas=meta_list,
                ids=ids,
            )
        except Exception as e:
            logger.error(f"Error adding to ChromaDB: {str(e)}")
            raise

    def search(
        self, query: str, top_k: int = 5, threshold: float = 0.3
    ) -> List[Tuple[str, float, Dict]]:
        """
        Search for relevant documents.

        Args:
            query: Search query
            top_k: Number of results to return
            threshold: Similarity threshold

        Returns:
            List of (document, score, metadata) tuples
        """
        # Generate query embedding
        query_embedding = self.embedding_manager.embed_text(query)

        if self.db_type == "faiss":
            return self._search_faiss(query_embedding, top_k, threshold)
        elif self.db_type == "chroma":
            return self._search_chroma(query, top_k, threshold)

    def _search_faiss(
        self, query_embedding: np.ndarray, top_k: int, threshold: float
    ) -> List[Tuple[str, float, Dict]]:
        """Search FAISS index."""
        if self.index.ntotal == 0:
            return []

        # Reshape for FAISS
        query_vector = np.array([query_embedding]).astype("float32")

        # Search
        distances, indices = self.index.search(query_vector, min(top_k, self.index.ntotal))

        results = []
        for distance, idx in zip(distances[0], indices[0]):
            # Convert L2 distance to similarity score
            similarity = 1 / (1 + float(distance))

            if similarity >= threshold:
                doc_id = self.ids[idx]
                document = self.documents[idx]
                metadata = self.metadata_store.get(doc_id, {})

                results.append((document, similarity, metadata))

        return results

    def _search_chroma(
        self, query: str, top_k: int, threshold: float
    ) -> List[Tuple[str, float, Dict]]:
        """Search ChromaDB."""
        try:
            results = self.chroma_collection.query(
                query_texts=[query], n_results=top_k, where=None
            )

            formatted_results = []
            if results and "documents" in results and results["documents"]:
                for docs, distances, metadatas in zip(
                    results["documents"], results["distances"], results["metadatas"]
                ):
                    for doc, distance, metadata in zip(docs, distances, metadatas):
                        # Convert distance to similarity score
                        similarity = 1 / (1 + float(distance))

                        if similarity >= threshold:
                            formatted_results.append((doc, similarity, metadata))

            return formatted_results
        except Exception as e:
            logger.error(f"Error searching ChromaDB: {str(e)}")
            return []

    def delete_document(self, doc_id: str) -> bool:
        """Delete a document from the vector store."""
        try:
            if self.db_type == "faiss":
                if doc_id in self.ids:
                    idx = self.ids.index(doc_id)
                    self.ids.pop(idx)
                    self.documents.pop(idx)
                    if doc_id in self.metadata_store:
                        del self.metadata_store[doc_id]
                    self._save_faiss_index()
                    return True
                return False

            elif self.db_type == "chroma":
                self.chroma_collection.delete(ids=[doc_id])
                return True
        except Exception as e:
            logger.error(f"Error deleting document: {str(e)}")
            return False

    def _save_faiss_index(self):
        """Save FAISS index to disk."""
        try:
            Path(self.db_path).mkdir(parents=True, exist_ok=True)
            faiss.write_index(self.index, f"{self.db_path}/index.faiss")

            # Save metadata
            metadata = {
                "documents": self.documents,
                "ids": self.ids,
                "metadata": self.metadata_store,
            }
            with open(f"{self.db_path}/metadata.json", "w") as f:
                json.dump(metadata, f)

            logger.info("Saved FAISS index to disk")
        except Exception as e:
            logger.error(f"Error saving FAISS index: {str(e)}")

    def get_stats(self) -> Dict[str, Any]:
        """Get vector store statistics."""
        if self.db_type == "faiss":
            return {
                "type": "faiss",
                "total_documents": len(self.documents),
                "index_size": self.index.ntotal,
                "embedding_dimension": self.index.d,
            }
        elif self.db_type == "chroma":
            return {
                "type": "chroma",
                "total_documents": self.chroma_collection.count(),
            }
