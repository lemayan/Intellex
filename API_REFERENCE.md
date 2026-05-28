"""API Reference Documentation for DeepScholar."""

# DeepScholar API Reference

## Quick Reference

### ResearchAgent

The main agent for answering questions and generating reports.

```python
from app.agents import ResearchAgent

agent = ResearchAgent(rag_pipeline, llm_orchestrator, memory_manager)

# Answer a question
result = agent.answer(
    query="What is quantum computing?",
    use_web_search=True,
    use_documents=True
)
# Returns: {
#     'query': str,
#     'answer': str,
#     'sources': List[Dict],
#     'web_results': List[Dict],
#     'tokens_used': int,
#     'conversation_context': Dict
# }

# Generate a report
report = agent.generate_report(
    title="AI in Healthcare",
    research_topic="Applications of AI in medical diagnosis"
)
# Returns: {
#     'title': str,
#     'topic': str,
#     'format': str,
#     'content': str,
#     'sections': Dict[str, str],
#     'sources': List[Dict]
# }

# Get follow-up questions
questions = agent.get_follow_up_questions(context, num_questions=3)
# Returns: List[str]
```

### LLMOrchestrator

Manages LLM API interactions.

```python
from app.agents import LLMOrchestrator

llm = LLMOrchestrator(provider="openai", model="gpt-4-turbo-preview")

# Generate text
response = llm.generate(
    prompt="Explain machine learning",
    system_context="You are a helpful AI assistant",
    temperature=0.7,
    max_tokens=2000
)

# Stream generation
for chunk in llm.stream_generate(prompt, system_context):
    print(chunk, end='')

# Count tokens
tokens = llm.count_tokens("Some text to count")
```

### RAGPipeline

Complete RAG (Retrieval-Augmented Generation) pipeline.

```python
from app.retrieval import RAGPipeline

rag = RAGPipeline(vector_store)

# Retrieve context
context, sources = rag.retrieve_context(
    query="Tell me about quantum computing",
    use_reranking=True
)

# Prepare prompt
prompt = rag.prepare_prompt(query, context)

# Add documents
doc_ids = rag.add_documents(
    documents=["doc1", "doc2"],
    ids=["id1", "id2"],
    metadata=[{}, {}]
)

# Get statistics
stats = rag.get_stats()
```

### VectorStore

Vector database operations.

```python
from app.vectorstore import VectorStore

vector_store = VectorStore(db_type="faiss")

# Add documents
ids = vector_store.add_documents(
    documents=["text1", "text2"],
    ids=["id1", "id2"],
    metadata=[{"source": "doc1"}, {"source": "doc2"}]
)

# Search
results = vector_store.search(
    query="search term",
    top_k=5,
    threshold=0.3
)
# Returns: List[(document, score, metadata)]

# Delete
vector_store.delete_document("id1")

# Statistics
stats = vector_store.get_stats()
```

### EmbeddingManager

Handle text embeddings.

```python
from app.vectorstore import EmbeddingManager

embedder = EmbeddingManager(provider="openai")

# Single embedding
emb = embedder.embed_text("Some text")

# Multiple embeddings
embs = embedder.embed_texts(["text1", "text2", "text3"])

# Embedding dimension
dim = embedder.get_embedding_dimension()

# Clear cache
embedder.clear_cache()
```

### DocumentProcessor

Process documents.

```python
from app.document_processing import DocumentProcessor

processor = DocumentProcessor(chunk_size=1000, chunk_overlap=200)

# Process single document
result = processor.process_document("path/to/file.pdf")
# Returns: {
#     'text': str,
#     'chunks': List[str],
#     'metadata': Dict
# }

# Process directory
results = processor.process_multiple_documents("./documents/")
# Returns: List[Dict]
```

### MemoryManager

Manage conversation and session memory.

```python
from app.memory import MemoryManager

memory_mgr = MemoryManager()

# Start session
session_id = memory_mgr.start_session()

# Get conversation
conv = memory_mgr.get_conversation()

# Save session
memory_mgr.save_session()

# Load session
memory_mgr.load_session(session_id)

# List sessions
sessions = memory_mgr.list_sessions()

# Persistent memory
memory_mgr.save_memory("key", {"data": "value"})
data = memory_mgr.load_memory("key")
```

### ConversationMemory

Manage individual conversations.

```python
from app.memory import ConversationMemory

conv = ConversationMemory(max_messages=20, max_tokens=4000)

# Add messages
conv.add_message(
    role="user",
    content="Hello",
    tokens=10,
    sources=[]
)

# Get context
context = conv.get_conversation_context(num_messages=5)

# Get system context
sys_context = conv.get_system_context()

# Statistics
stats = conv.get_stats()

# Export
export = conv.export_conversation()

# Clear
conv.clear()
```

### WebSearcher

Web search functionality.

```python
from app.web_search import WebSearcher

searcher = WebSearcher(provider="tavily")

# Search
results = searcher.search(
    query="latest AI research",
    max_results=5,
    include_snippets=True
)
# Returns: List[{
#     'title': str,
#     'url': str,
#     'snippet': str,
#     'source': str
# }]

# Extract sources
citations = searcher.extract_sources(results)
```

### ReportGenerator

Generate and export reports.

```python
from app.reporting import ReportGenerator

gen = ReportGenerator(output_dir="./reports/")

# Generate Markdown
md = gen.generate_markdown_report(
    title="My Report",
    content={
        "introduction": "...",
        "findings": "...",
        "conclusion": "..."
    }
)

# Generate HTML
html = gen.generate_html_report(title, content)

# Save report
path = gen.save_report(title, content, format="markdown")

# Generate bibliography
bib = gen.generate_bibliography(sources)
```

## Configuration

All settings are in `config/settings.py` and can be overridden via `.env`:

```env
# LLM
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4-turbo-preview

# Embeddings
EMBEDDING_PROVIDER=openai
EMBEDDING_MODEL=text-embedding-3-small

# Vector DB
VECTORDB_TYPE=faiss
VECTORDB_PATH=./data/embeddings/faiss_db

# Web Search
WEB_SEARCH_PROVIDER=tavily
TAVILY_API_KEY=...

# Memory
MEMORY_TYPE=hybrid
MEMORY_MAX_TOKENS=4000

# RAG
RETRIEVAL_TOP_K=5
ENABLE_RERANKING=true

# Application
ENVIRONMENT=production
LOG_LEVEL=INFO
```

## Error Handling

All modules include proper error handling:

```python
from app.utils.logger import get_logger

logger = get_logger(__name__)

try:
    result = agent.answer(query)
except Exception as e:
    logger.error(f"Error: {str(e)}")
```

## Logging

Configure logging:

```python
from app.utils.logger import setup_logger

logger = setup_logger("my_app", log_level="INFO")
logger.info("Message")
logger.error("Error")
```

## Utilities

Useful utility functions:

```python
from app.utils.text_utils import (
    truncate_text,
    clean_text,
    split_text_into_sentences,
    extract_keywords
)

from app.utils.validators import (
    validate_file,
    validate_url,
    validate_api_keys,
    validate_document_size
)
```

## Examples

See `examples.py` for complete usage examples:

```bash
python examples.py --example 1  # Basic Q&A
python examples.py --example 2  # Web search
python examples.py --example 3  # Document processing
python examples.py --example 4  # Report generation
python examples.py --example 5  # Memory management
python examples.py --example 6  # Advanced search
python examples.py --example 7  # Interactive mode
```

## Complete Integration Example

```python
from main import DeepScholar

# Initialize
scholar = DeepScholar()

# Process documents
scholar.process_documents(["doc1.pdf", "doc2.pdf"])

# Ask question
result = scholar.answer_question(
    "What are the key findings?",
    use_web_search=True
)

print(result['answer'])
print(f"Sources: {len(result['sources'])}")

# Generate report
report = scholar.generate_report(
    "Research Summary",
    "Summary of key findings from documents"
)

# Get statistics
stats = scholar.get_stats()
print(stats)
```

## Performance Tips

1. **Cache Embeddings** - Reuse embeddings for same text
2. **Batch Processing** - Process documents in batches
3. **Reduce Top-K** - Use smaller retrieval_top_k for faster results
4. **Token Limits** - Set reasonable context_window_tokens
5. **Index Optimization** - Use FAISS for large-scale retrieval

## Troubleshooting

Common issues and solutions:

| Issue | Solution |
|-------|----------|
| API Key Error | Check .env, validate key format |
| Memory Error | Reduce batch size, lower max_messages |
| Slow Search | Increase retrieval_top_k, optimize index |
| Generation Timeout | Reduce max_tokens, check network |

---

**Need help?** Check README.md or examples.py
