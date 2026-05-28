"""Quick Reference Card for DeepScholar Developers."""

# DeepScholar - Developer Quick Reference

## 🚀 Quick Start (Copy & Paste)

```bash
# 1. Setup
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys

# 2. Run
python main.py --ui
# or
streamlit run app/frontend/streamlit_app.py

# 3. Access
# http://localhost:8501
```

---

## 📚 Common Operations

### Process a Document

```python
from main import DeepScholar

scholar = DeepScholar()
result = scholar.process_documents(["path/to/document.pdf"])
```

### Ask a Question

```python
result = scholar.answer_question("What is machine learning?")
print(result['answer'])
```

### Generate a Report

```python
report = scholar.generate_report(
    title="My Report",
    research_topic="Quantum Computing"
)
```

### Search Documents

```python
context, sources = scholar.rag_pipeline.retrieve_context(
    "search query"
)
```

---

## 🔧 Configuration Quick Links

| Setting | Location | Default |
|---------|----------|---------|
| API Keys | `.env` | N/A |
| LLM Model | `LLM_PROVIDER` | openai |
| Vector DB | `VECTORDB_TYPE` | faiss |
| Top Results | `RETRIEVAL_TOP_K` | 5 |
| Chunk Size | `DOCUMENT_CHUNK_SIZE` | 1000 |
| Memory Type | `MEMORY_TYPE` | hybrid |

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `main.py` | Main entry point |
| `app/agents/research_agent.py` | Core agent logic |
| `app/retrieval/rag_pipeline.py` | RAG pipeline |
| `app/vectorstore/vector_store.py` | Vector database |
| `app/frontend/streamlit_app.py` | Web UI |
| `config/settings.py` | Configuration |

---

## 🐛 Common Errors & Fixes

| Error | Fix |
|-------|-----|
| API Key Not Found | Edit `.env`, add OPENAI_API_KEY |
| Module Not Found | `pip install -r requirements.txt` |
| Port in Use | `streamlit run ... --server.port 8502` |
| Out of Memory | Reduce RETRIEVAL_TOP_K or CONTEXT_WINDOW_TOKENS |
| Vector Store Not Found | Upload documents first |

---

## 🔑 Important Classes

```python
# Main Classes
from main import DeepScholar
from app.agents import ResearchAgent, LLMOrchestrator
from app.retrieval import RAGPipeline
from app.vectorstore import VectorStore, EmbeddingManager
from app.document_processing import DocumentProcessor
from app.memory import MemoryManager, ConversationMemory
from app.web_search import WebSearcher
from app.reporting import ReportGenerator
```

---

## 📊 Architecture Diagram

```
User Input (Streamlit UI)
    ↓
Research Agent (main orchestrator)
    ↓
    ├─→ RAG Pipeline (document retrieval)
    │   ├─→ Vector Store (FAISS/ChromaDB)
    │   └─→ Embedding Manager
    │
    ├─→ LLM Orchestrator (OpenAI/Gemini)
    │
    ├─→ Web Searcher (Tavily/SerpAPI)
    │
    ├─→ Memory Manager (conversation history)
    │
    └─→ Report Generator
         ↓
    Output (Answer + Citations)
```

---

## 🧪 Testing Commands

```bash
# Run tests
pytest tests/

# With coverage
pytest tests/ --cov=app

# Specific test
pytest tests/test_example.py::test_text_chunking

# Examples
python examples.py --example 1
python examples.py --example 7  # Interactive
```

---

## 🐳 Docker Commands

```bash
# Build
docker build -t deepscholar:latest .

# Run
docker run -p 8501:8501 \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  deepscholar:latest

# Docker Compose
docker-compose up -d
docker-compose down
docker-compose logs -f

# Clean up
docker system prune -a
```

---

## 📝 Logging

```python
from app.utils.logger import get_logger

logger = get_logger(__name__)
logger.info("Information")
logger.error("Error")
logger.debug("Debug")
```

View logs:
```bash
tail -f logs/deepscholar.log
```

---

## 🔐 Environment Variables

```env
# Required
OPENAI_API_KEY=sk-...

# Optional but Recommended
TAVILY_API_KEY=tvly-...

# Optional
GEMINI_API_KEY=AIza...
SERPAPI_API_KEY=...

# Application
ENVIRONMENT=production
LOG_LEVEL=INFO
PORT=8501
```

---

## 📊 Useful Code Snippets

### Initialize All Components

```python
from main import DeepScholar

scholar = DeepScholar()
# Now have access to:
# - scholar.research_agent
# - scholar.rag_pipeline
# - scholar.vector_store
# - scholar.llm_orchestrator
# - scholar.memory_manager
# - scholar.document_processor
```

### Search Documents

```python
results = scholar.rag_pipeline.retriever.retrieve(
    "your search query"
)
for doc, score, meta in results:
    print(f"Score: {score:.2f} - {doc[:100]}...")
```

### Export Conversation

```python
conv = scholar.memory_manager.get_conversation()
data = conv.export_conversation()
import json
with open("conversation.json", "w") as f:
    json.dump(data, f)
```

### Generate Embeddings

```python
embedding = scholar.embedding_manager.embed_text(
    "Text to embed"
)
print(f"Embedding dimension: {len(embedding)}")
```

---

## 🎯 Project Structure Tips

- **Models**: Not stored here, use cloud APIs
- **Data**: Stored in `./data/` directory
- **Logs**: Stored in `./logs/` directory
- **Config**: All settings in `config/settings.py`
- **Utils**: Helper functions in `app/utils/`

---

## 📈 Performance Tips

1. **Cache embeddings** - Automatic in EmbeddingManager
2. **Reduce top_k** - Faster retrieval with `RETRIEVAL_TOP_K=3`
3. **Smaller chunks** - `DOCUMENT_CHUNK_SIZE=500`
4. **Stream responses** - Enable "Stream Response" in UI
5. **Use FAISS** - Faster than ChromaDB for local use

---

## 🔗 External Resources

- **OpenAI Docs**: https://platform.openai.com/docs
- **Tavily API**: https://tavily.com/docs
- **FAISS**: https://github.com/facebookresearch/faiss
- **Streamlit**: https://docs.streamlit.io
- **LangChain**: https://langchain.com/docs

---

## 💡 Extension Ideas

1. Add Claude as LLM provider
2. Add Pinecone for vector DB
3. Add voice interface (whisper + TTS)
4. Add knowledge graph extraction
5. Add collaborative features
6. Add real-time streaming
7. Add PDF annotation/highlighting
8. Add citation style formatting

---

## 🎓 Learning Resources

1. **RAG Papers**: Search for "Retrieval-Augmented Generation"
2. **Vector Databases**: Study FAISS documentation
3. **LLM APIs**: Read OpenAI/Gemini documentation
4. **Python Best Practices**: PEP 8, type hints
5. **Production Code**: Study error handling, logging

---

## 🚀 Deployment Checklist

- [ ] Update `.env` with production API keys
- [ ] Set `ENVIRONMENT=production`
- [ ] Set `DEBUG=false`
- [ ] Create data directories
- [ ] Run `pip install -r requirements.txt`
- [ ] Test locally with `python main.py --ui`
- [ ] Build Docker image
- [ ] Deploy container
- [ ] Monitor logs
- [ ] Set up backups

---

## 📞 Help Resources

1. **README.md** - Full documentation
2. **QUICKSTART.md** - Quick start guide
3. **SETUP.md** - Installation guide
4. **API_REFERENCE.md** - Complete API docs
5. **ADVANCED_CONFIG.md** - Advanced settings
6. **examples.py** - Working code examples
7. **PROJECT_SUMMARY.md** - Project overview

---

## ⚡ Pro Tips

1. Use `--example 7` for interactive mode
2. Check logs when stuck: `tail -f logs/deepscholar.log`
3. Test API keys early: `python examples.py --example 2`
4. Use Docker for production: `docker-compose up`
5. Monitor memory usage: Watch `MEMORY_MAX_TOKENS`

---

**Keep coding! 🚀**

More help? Check PROJECT_SUMMARY.md
