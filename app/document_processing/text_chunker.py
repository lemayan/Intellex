"""Text chunking utilities for RAG pipeline."""

from typing import List
import re


class TextChunker:
    """Split text into overlapping chunks for RAG."""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize text chunker.

        Args:
            chunk_size: Size of each chunk in characters
            chunk_overlap: Number of overlapping characters between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into overlapping chunks.

        Args:
            text: Text to chunk

        Returns:
            List of text chunks
        """
        if not text or len(text) == 0:
            return []

        chunks = []
        stride = self.chunk_size - self.chunk_overlap

        # Create chunks with overlap
        for i in range(0, len(text), stride):
            chunk = text[i : i + self.chunk_size]
            if chunk.strip():  # Only add non-empty chunks
                chunks.append(chunk)

            # Stop if we've reached the end
            if i + self.chunk_size >= len(text):
                break

        return chunks

    def chunk_by_sentences(self, text: str) -> List[str]:
        """
        Split text into chunks by sentences (more semantically meaningful).

        Args:
            text: Text to chunk

        Returns:
            List of text chunks
        """
        # Split into sentences
        sentences = re.split(r"(?<=[.!?])\s+", text)
        sentences = [s.strip() for s in sentences if s.strip()]

        chunks = []
        current_chunk = ""

        for sentence in sentences:
            # Check if adding this sentence would exceed chunk size
            if len(current_chunk) + len(sentence) + 1 > self.chunk_size:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                if current_chunk:
                    current_chunk += " " + sentence
                else:
                    current_chunk = sentence

        # Add last chunk
        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    def chunk_by_paragraphs(self, text: str) -> List[str]:
        """
        Split text into chunks by paragraphs.

        Args:
            text: Text to chunk

        Returns:
            List of text chunks
        """
        # Split by double newlines (paragraphs)
        paragraphs = text.split("\n\n")
        paragraphs = [p.strip() for p in paragraphs if p.strip()]

        chunks = []
        current_chunk = ""

        for paragraph in paragraphs:
            if len(current_chunk) + len(paragraph) + 2 > self.chunk_size:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = paragraph
            else:
                if current_chunk:
                    current_chunk += "\n\n" + paragraph
                else:
                    current_chunk = paragraph

        # Add last chunk
        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks
