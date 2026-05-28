"""DeepScholar - AI Research Assistant Application."""

__version__ = "1.0.0"
__author__ = "DeepScholar Team"
__description__ = "Production-grade AI Research Assistant with RAG and LLM Orchestration"

from config.settings import get_settings
from app.agents import ResearchAgent, LLMOrchestrator
from app.memory import ConversationMemory, MemoryManager
from app.retrieval import RAGPipeline
from app.vectorstore import VectorStore, EmbeddingManager
from app.document_processing import DocumentProcessor
from app.web_search import WebSearcher
from app.reporting import ReportGenerator

__all__ = [
    "ResearchAgent",
    "LLMOrchestrator",
    "ConversationMemory",
    "MemoryManager",
    "RAGPipeline",
    "VectorStore",
    "EmbeddingManager",
    "DocumentProcessor",
    "WebSearcher",
    "ReportGenerator",
    "get_settings",
]
