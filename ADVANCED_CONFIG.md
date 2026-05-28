"""Advanced Configuration and Troubleshooting Guide."""

# DeepScholar - Advanced Configuration & Troubleshooting

## Advanced Configuration

### 1. LLM Configuration

#### Using OpenAI GPT-4

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-proj-...
OPENAI_MODEL=gpt-4-turbo-preview
```

#### Using Gemini

```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=AIza...
GEMINI_MODEL=gemini-pro
```

#### Custom Temperature & Tokens

```python
from app.agents import LLMOrchestrator

llm = LLMOrchestrator()
response = llm.generate(
    prompt="Your prompt",
    temperature=0.3,  # 0 = deterministic, 1 = creative
    max_tokens=4000
)
```

### 2. Vector Database Configuration

#### FAISS (Fast, Local)

```env
VECTORDB_TYPE=faiss
VECTORDB_PATH=./data/embeddings/faiss_db
```

Pros: ✅ Fast, ✅ No server needed
Cons: ❌ Local only, ❌ No scaling

#### ChromaDB (Cloud-Ready)

```env
VECTORDB_TYPE=chroma
VECTORDB_PATH=./data/embeddings/chroma_db
```

Pros: ✅ Cloud support, ✅ Managed
Cons: ❌ Slower, ❌ External dependency

### 3. Embedding Configuration

#### OpenAI Embeddings (Recommended)

```env
EMBEDDING_PROVIDER=openai
EMBEDDING_MODEL=text-embedding-3-small  # 1536 dims
# or
EMBEDDING_MODEL=text-embedding-3-large  # 3072 dims
```

#### HuggingFace Embeddings (Free, Local)

```env
EMBEDDING_PROVIDER=huggingface
HUGGINGFACE_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

### 4. Web Search Configuration

#### Tavily (Recommended for AI)

```env
WEB_SEARCH_PROVIDER=tavily
TAVILY_API_KEY=tvly-...
```

#### SerpAPI

```env
WEB_SEARCH_PROVIDER=serpapi
SERPAPI_API_KEY=...
```

#### Google Custom Search

```env
WEB_SEARCH_PROVIDER=google
GOOGLE_SEARCH_API_KEY=...
GOOGLE_SEARCH_ENGINE_ID=...
```

### 5. RAG Pipeline Tuning

```env
# Number of documents to retrieve
RETRIEVAL_TOP_K=5

# Minimum similarity score (0-1)
RETRIEVAL_SIMILARITY_THRESHOLD=0.3

# Maximum context tokens
CONTEXT_WINDOW_TOKENS=2000

# Enable intelligent reranking
ENABLE_RERANKING=true
```

### 6. Memory Configuration

```env
# Memory type: in_memory, redis, hybrid
MEMORY_TYPE=hybrid

# Max tokens to keep in memory
MEMORY_MAX_TOKENS=4000

# Session storage directory
SESSION_MEMORY_DIR=./data/memory/sessions

# Persistent storage directory
PERSISTENT_MEMORY_DIR=./data/memory/persistent
```

### 7. Document Processing

```env
# Size of text chunks
DOCUMENT_CHUNK_SIZE=1000

# Overlap between chunks
DOCUMENT_CHUNK_OVERLAP=200

# Max upload size in MB
MAX_UPLOAD_SIZE_MB=100
```

---

## Troubleshooting Guide

### Problem: "API Key Not Found" Error

**Symptoms:**
```
Error: OPENAI_API_KEY not found
```

**Solutions:**

1. Check `.env` file exists
```bash
ls -la .env
```

2. Verify key is set correctly
```bash
echo $OPENAI_API_KEY
```

3. Ensure no quotes in `.env`
```env
# ❌ Wrong
OPENAI_API_KEY="sk-proj-..."

# ✅ Correct
OPENAI_API_KEY=sk-proj-...
```

4. Restart application after changing `.env`

### Problem: Vector Store Not Found

**Symptoms:**
```
Error: FAISS index not found
```

**Solutions:**

1. Create required directories
```bash
mkdir -p data/embeddings
```

2. Upload documents first
- Go to Document Management
- Upload a PDF
- Check "Process & Store Documents"

3. Check VECTORDB_PATH
```env
VECTORDB_PATH=./data/embeddings/faiss_db
```

### Problem: Out of Memory

**Symptoms:**
```
MemoryError: Unable to allocate...
```

**Solutions:**

1. Reduce RETRIEVAL_TOP_K
```env
RETRIEVAL_TOP_K=3  # Was 5
```

2. Reduce CONTEXT_WINDOW_TOKENS
```env
CONTEXT_WINDOW_TOKENS=1000  # Was 2000
```

3. Reduce MEMORY_MAX_TOKENS
```env
MEMORY_MAX_TOKENS=2000  # Was 4000
```

4. Use smaller embedding model
```env
EMBEDDING_MODEL=text-embedding-3-small
```

### Problem: Slow Response Times

**Symptoms:**
- Queries take 10+ seconds
- Web search very slow

**Solutions:**

1. Disable web search (unless needed)
- Uncheck "Web Search" in Chat

2. Reduce top_k
```env
RETRIEVAL_TOP_K=3
```

3. Use smaller chunks
```env
DOCUMENT_CHUNK_SIZE=500
```

4. Enable streaming
- Check "Stream Response" in UI

### Problem: Port 8501 Already in Use

**Symptoms:**
```
ERROR: Address already in use
```

**Solutions:**

1. Use different port
```bash
streamlit run app/frontend/streamlit_app.py --server.port 8502
```

2. Kill process using port
```bash
# Windows
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# Mac/Linux
lsof -i :8501
kill -9 <PID>
```

### Problem: Documents Not Being Indexed

**Symptoms:**
- Upload documents but get no results
- Search returns no documents

**Solutions:**

1. Check file format
- Supported: PDF, DOCX, TXT
- Check file extensions

2. Verify file size
```env
MAX_UPLOAD_SIZE_MB=100
```

3. Check logs
```bash
tail -f logs/deepscholar.log
```

4. Manual processing
```python
from main import DeepScholar

scholar = DeepScholar()
result = scholar.process_documents(["path/to/file.pdf"])
print(result)
```

### Problem: LLM Timeout

**Symptoms:**
```
timeout: Waited 60s for completion
```

**Solutions:**

1. Check internet connection
```bash
ping api.openai.com
```

2. Reduce max_tokens
```python
llm.generate(prompt, max_tokens=1000)  # Was 2000
```

3. Check API status
- OpenAI: https://status.openai.com
- Gemini: https://status.google.cloud

### Problem: Web Search Not Working

**Symptoms:**
- Web search returns no results
- "API key not configured" warning

**Solutions:**

1. Set WEB_SEARCH_PROVIDER
```env
WEB_SEARCH_PROVIDER=tavily
TAVILY_API_KEY=tvly-...
```

2. Test API key
```python
from app.web_search import WebSearcher

searcher = WebSearcher()
results = searcher.search("test query")
print(results)
```

3. Check network access
```bash
curl https://api.tavily.com
```

---

## Performance Optimization

### 1. Embedding Optimization

```python
# Enable caching to avoid reembedding
embedding_mgr = EmbeddingManager()
# Embeddings are cached automatically

# Clear cache if needed
embedding_mgr.clear_cache()
```

### 2. Batch Processing

```python
# Process multiple documents at once
processor = DocumentProcessor()
results = processor.process_multiple_documents("./documents/")
```

### 3. Query Optimization

```env
# Optimal settings for fast retrieval
RETRIEVAL_TOP_K=3
RETRIEVAL_SIMILARITY_THRESHOLD=0.4
CONTEXT_WINDOW_TOKENS=1500
ENABLE_RERANKING=false  # Disable for speed
```

### 4. Memory Optimization

```python
# Prune old messages
conversation = memory_manager.get_conversation()
conversation._prune_memory()
```

---

## Advanced Features

### Custom Embedding Model

```python
from app.vectorstore import EmbeddingManager

class CustomEmbeddingManager(EmbeddingManager):
    def _embed_openai(self, texts):
        # Custom implementation
        pass

embedder = CustomEmbeddingManager()
```

### Custom LLM Provider

```python
from app.agents import LLMOrchestrator

class CustomLLMOrchestrator(LLMOrchestrator):
    def _generate_custom(self, prompt):
        # Custom implementation
        pass
```

### Extended Retrieval

```python
from app.retrieval import DocumentRetriever

# Multi-query retrieval
queries = [
    "What is quantum computing?",
    "How does QC work?",
    "QC applications"
]

all_results = []
for query in queries:
    results = retriever.retrieve(query)
    all_results.extend(results)

# Deduplicate and rank
unique_results = list({r[2]['id']: r for r in all_results}.values())
```

---

## Monitoring & Logging

### View Logs

```bash
# Real-time logs
tail -f logs/deepscholar.log

# Last 100 lines
tail -100 logs/deepscholar.log

# Search logs
grep "ERROR" logs/deepscholar.log
```

### Custom Logging

```python
from app.utils.logger import setup_logger

logger = setup_logger("my_module", log_level="DEBUG")
logger.info("Information message")
logger.debug("Debug message")
logger.error("Error message")
```

### Log Levels

```env
LOG_LEVEL=DEBUG    # Most verbose
LOG_LEVEL=INFO     # Standard
LOG_LEVEL=WARNING  # Warnings & errors
LOG_LEVEL=ERROR    # Errors only
```

---

## Production Deployment

### Docker Deployment

```bash
# Build image
docker build -t deepscholar:latest .

# Run with environment variables
docker run -p 8501:8501 \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -e ENVIRONMENT=production \
  deepscholar:latest
```

### Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Environment Variables for Production

```env
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
MEMORY_TYPE=hybrid
ENABLE_RERANKING=true
RETRIEVAL_TOP_K=5
```

---

## Security Best Practices

1. **Never commit .env to git**
```bash
# .gitignore
.env
.env.local
secrets/
```

2. **Use environment variables**
```env
OPENAI_API_KEY=xxx  # Not in code
```

3. **Validate user input**
```python
from app.utils.validators import validate_url, validate_file
```

4. **Handle errors securely**
```python
try:
    result = agent.answer(query)
except Exception as e:
    logger.error(f"Error: {str(e)}")  # No API keys in logs
    return "An error occurred"  # Generic message to user
```

---

## Performance Benchmarks

### Typical Performance

| Operation | Time | Notes |
|-----------|------|-------|
| Document Upload (PDF) | 2-5s | Depends on size |
| Text Embedding | 0.5-1s per chunk | Cached |
| Vector Search | 0.1-0.2s | Top-5 results |
| LLM Response | 5-15s | OpenAI API call |
| Web Search | 2-5s | External API |
| Report Generation | 30-60s | Multiple API calls |

### Optimization Tips

- Use smaller embedding models for speed
- Cache embeddings aggressively
- Reduce retrieval_top_k for speed
- Disable reranking unless needed
- Use streaming for better UX

---

## FAQ

**Q: Can I use local LLMs?**
A: Yes, add custom provider to LLMOrchestrator

**Q: What's the cost?**
A: Depends on API usage:
- OpenAI: ~$0.01-0.10 per query
- Embeddings: ~$0.01 per 1M tokens
- Web search: ~$0.005 per query

**Q: Can I modify the UI?**
A: Yes! Edit `app/frontend/streamlit_app.py`

**Q: How do I backup data?**
A: Backup `./data/` directory

**Q: Can I use Redis for memory?**
A: Not yet, but extensible

**Q: How do I scale to 1M documents?**
A: Consider Pinecone or Weaviate

---

For more help, check:
- README.md - Full documentation
- API_REFERENCE.md - Complete API docs
- PROJECT_SUMMARY.md - Project overview
- examples.py - Working examples
