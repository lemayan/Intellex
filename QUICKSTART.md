"""Quick Start Guide for DeepScholar."""

# Quick Start Guide

## 1-Minute Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 3. Run the UI
streamlit run app/frontend/streamlit_app.py
```

## First Use

1. Open http://localhost:8501
2. Go to "Document Management"
3. Upload a PDF or document
4. Go to "Chat"
5. Ask a question about your document!

## Example Questions

- "What are the main topics in this document?"
- "Summarize the key findings"
- "Explain [specific concept] from the document"
- "What does the author conclude?"

## Available Commands

```bash
# UI Mode (Web Interface)
python main.py --ui

# Interactive Mode (Terminal)
python main.py --interactive

# Demo Mode
python main.py --demo

# Run Examples
python examples.py --example 1
python examples.py --example 2
python examples.py --example 7  # Interactive
```

## Folder Structure

```
DeepScholar/
├── app/                  # Main application code
│   ├── agents/          # AI agents
│   ├── retrieval/       # RAG pipeline
│   ├── vectorstore/     # Vector DB
│   ├── memory/          # Conversation memory
│   ├── document_processing/  # PDF/document handling
│   ├── web_search/      # Web search integration
│   ├── reporting/       # Report generation
│   ├── utils/           # Utilities
│   └── frontend/        # Streamlit UI
├── config/              # Configuration
├── data/                # Data storage
├── tests/               # Tests
├── main.py              # Entry point
├── examples.py          # Example code
└── requirements.txt     # Dependencies
```

## Tips

1. **First Run**: Start with the Streamlit UI (easiest)
2. **API Keys**: Make sure you have OPENAI_API_KEY set
3. **Documents**: Upload quality PDFs for best results
4. **Web Search**: Optional but recommended for current info
5. **Memory**: Sessions are automatically saved

## Configuration

Edit `.env` to customize:

```env
# LLM Settings
OPENAI_MODEL=gpt-4-turbo-preview

# Retrieval Settings
RETRIEVAL_TOP_K=5
ENABLE_RERANKING=true

# Memory Settings
MEMORY_MAX_TOKENS=4000
```

## Common Tasks

### Upload Documents
1. Click "Document Management"
2. Select files
3. Click "Process & Store Documents"

### Ask Questions
1. Click "Chat"
2. Type your question
3. Check "Use Documents" or "Web Search"
4. Click "Ask DeepScholar"

### Generate Reports
1. Click "Generate Report"
2. Enter title and research topic
3. Click "Generate Report"
4. Download the result

### View Conversation History
1. Click "Memory & History"
2. View all past messages
3. Export conversation

## Troubleshooting

**Error: "API key not found"**
- Check `.env` file
- Make sure OPENAI_API_KEY is set

**Error: "Module not found"**
- Activate virtual environment
- Run `pip install -r requirements.txt`

**Error: "Port 8501 in use"**
- Run on different port: `streamlit run app/frontend/streamlit_app.py --server.port 8502`

**Slow responses**
- Check internet connection
- Reduce RETRIEVAL_TOP_K in `.env`
- Use fewer documents

## Next Steps

1. Explore the Streamlit UI features
2. Upload some documents
3. Ask research questions
4. Generate reports
5. Check out examples.py for API usage

## Documentation

- README.md - Full documentation
- SETUP.md - Detailed installation
- examples.py - Code examples
- config/settings.py - Configuration options

## Contact & Support

For issues or questions:
- Check logs in `./logs/`
- Review examples.py
- Check README.md
- Look at error messages carefully

---

**Happy Researching! 🔬**
