"""DeepScholar FastAPI Backend - Lazy initialization for fast startup."""

import os
import shutil
import sys
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

sys.path.insert(0, str(Path(__file__).parent.parent))

app = FastAPI(title="DeepScholar API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lazy-loaded components
_components = {}


def get_components():
    """Initialize components on first use."""
    global _components
    if _components:
        return _components

    from app.agents import LLMOrchestrator, ResearchAgent
    from app.memory import MemoryManager
    from app.reporting import ReportGenerator
    from app.retrieval import RAGPipeline
    from app.utils.logger import get_logger, setup_logger
    from app.vectorstore import EmbeddingManager, VectorStore
    from config.settings import get_settings

    setup_logger("deepscholar", log_level="INFO")
    logger = get_logger(__name__)

    settings = get_settings()
    embedding_manager = EmbeddingManager()
    vector_store = VectorStore(embedding_manager=embedding_manager)
    rag_pipeline = RAGPipeline(vector_store=vector_store)
    llm_orchestrator = LLMOrchestrator()
    memory_manager = MemoryManager()
    research_agent = ResearchAgent(
        rag_pipeline=rag_pipeline,
        llm_orchestrator=llm_orchestrator,
        memory_manager=memory_manager,
    )
    report_generator = ReportGenerator()
    memory_manager.start_session()

    _components = {
        "embedding_manager": embedding_manager,
        "vector_store": vector_store,
        "rag_pipeline": rag_pipeline,
        "llm_orchestrator": llm_orchestrator,
        "memory_manager": memory_manager,
        "research_agent": research_agent,
        "report_generator": report_generator,
    }
    logger.info("DeepScholar components initialized.")
    return _components


class ChatRequest(BaseModel):
    query: str
    use_documents: bool = True
    use_web_search: bool = False


@app.get("/api/health")
async def health():
    return {"status": "ok", "message": "DeepScholar API is running"}


@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        components = get_components()
        result = components["research_agent"].answer(
            request.query,
            use_web_search=request.use_web_search,
            use_documents=request.use_documents,
            stream=False,
        )
        return {"answer": result["answer"], "sources": result.get("sources", [])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/documents")
async def upload_documents(files: List[UploadFile] = File(...)):
    try:
        from app.document_processing import DocumentProcessor
        components = get_components()
        processor = DocumentProcessor(chunk_size=1000, chunk_overlap=200)
        results = []
        os.makedirs("temp_uploads", exist_ok=True)

        for file in files:
            temp_path = f"temp_uploads/{file.filename}"
            with open(temp_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            result = processor.process_document(temp_path)
            components["rag_pipeline"].add_documents(
                documents=result["chunks"],
                metadata=[{"filename": result["metadata"]["filename"]} for _ in result["chunks"]],
            )
            results.append({"filename": file.filename, "status": "processed"})
            os.remove(temp_path)

        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/search")
async def search(q: str, top_k: int = 5):
    try:
        components = get_components()
        results = components["rag_pipeline"].retrieve(q, top_k=top_k)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class ReportRequest(BaseModel):
    topic: str
    report_type: str


@app.post("/api/reports")
async def generate_report(request: ReportRequest):
    try:
        components = get_components()
        report = components["report_generator"].generate_report(
            topic=request.topic,
            report_type=request.report_type,
        )
        return {"content": report["content"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats")
async def get_stats():
    try:
        components = get_components()
        stats = components["vector_store"].get_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
