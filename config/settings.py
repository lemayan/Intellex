"""Configuration settings for DeepScholar."""

import os
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # LLM Configuration
    llm_provider: str = Field("openai", env="LLM_PROVIDER")
    openai_api_key: Optional[str] = Field(None, env="OPENAI_API_KEY")
    openai_model: str = Field("gpt-4-turbo-preview", env="OPENAI_MODEL")
    gemini_api_key: Optional[str] = Field(None, env="GEMINI_API_KEY")
    gemini_model: str = Field("gemini-pro", env="GEMINI_MODEL")

    # Embedding Configuration
    embedding_provider: str = Field("simple", env="EMBEDDING_PROVIDER")
    embedding_model: str = Field("simple-hash-384", env="EMBEDDING_MODEL")
    huggingface_model: str = Field(
        "sentence-transformers/all-MiniLM-L6-v2", env="HUGGINGFACE_MODEL"
    )

    # Vector Database
    vectordb_type: str = Field("faiss", env="VECTORDB_TYPE")
    vectordb_path: str = Field("./data/embeddings/faiss_db", env="VECTORDB_PATH")

    # Web Search
    web_search_provider: str = Field("tavily", env="WEB_SEARCH_PROVIDER")
    tavily_api_key: Optional[str] = Field(None, env="TAVILY_API_KEY")
    serpapi_api_key: Optional[str] = Field(None, env="SERPAPI_API_KEY")
    google_search_api_key: Optional[str] = Field(None, env="GOOGLE_SEARCH_API_KEY")
    google_search_engine_id: Optional[str] = Field(None, env="GOOGLE_SEARCH_ENGINE_ID")

    # Memory Configuration
    memory_type: str = Field("hybrid", env="MEMORY_TYPE")
    memory_max_tokens: int = Field(4000, env="MEMORY_MAX_TOKENS")
    session_memory_dir: str = Field("./data/memory/sessions", env="SESSION_MEMORY_DIR")
    persistent_memory_dir: str = Field(
        "./data/memory/persistent", env="PERSISTENT_MEMORY_DIR"
    )

    # Document Processing
    document_chunk_size: int = Field(1000, env="DOCUMENT_CHUNK_SIZE")
    document_chunk_overlap: int = Field(200, env="DOCUMENT_CHUNK_OVERLAP")
    max_upload_size_mb: int = Field(100, env="MAX_UPLOAD_SIZE_MB")

    # RAG Configuration
    retrieval_top_k: int = Field(5, env="RETRIEVAL_TOP_K")
    retrieval_similarity_threshold: float = Field(
        0.3, env="RETRIEVAL_SIMILARITY_THRESHOLD"
    )
    context_window_tokens: int = Field(2000, env="CONTEXT_WINDOW_TOKENS")
    enable_reranking: bool = Field(True, env="ENABLE_RERANKING")

    # Logging
    log_level: str = Field("INFO", env="LOG_LEVEL")
    log_dir: str = Field("./logs", env="LOG_DIR")

    # Application
    debug: bool = Field(False, env="DEBUG")
    environment: str = Field("production", env="ENVIRONMENT")
    port: int = Field(8501, env="PORT")
    host: str = Field("0.0.0.0", env="HOST")

    class Config:
        """Pydantic config."""

        env_file = ".env"
        case_sensitive = False

    @property
    def is_production(self) -> bool:
        """Check if environment is production."""
        return self.environment.lower() == "production"

    @property
    def is_debug(self) -> bool:
        """Check if debug mode is enabled."""
        return self.debug or not self.is_production


def get_settings() -> Settings:
    """Get application settings."""
    return Settings()
