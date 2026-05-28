"""DeepScholar Installation and Setup Guide.

This guide walks you through setting up DeepScholar from scratch.
"""

# Installation Guide

## 1. Prerequisites

- Python 3.12 or higher
- pip or conda package manager
- 4GB+ RAM recommended
- Internet connection (for web search and API calls)

## 2. Installation Steps

### Step 1: Clone or Download

```bash
# If cloning from git
git clone https://github.com/your-repo/deepscholar.git
cd deepscholar

# Otherwise, extract the downloaded folder
cd DeepScholar
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

### Step 4: Configure Environment

```bash
# Copy example env
cp .env.example .env

# Edit .env with your API keys
# Open .env in your favorite editor and fill in:
# - OPENAI_API_KEY
# - TAVILY_API_KEY (optional, for web search)
```

### Step 5: Create Data Directories

```bash
# Create required directories
mkdir -p data/documents data/embeddings data/memory
mkdir -p logs
```

## 3. API Configuration

### OpenAI Setup

1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Copy it to `.env` as OPENAI_API_KEY

### Tavily API Setup (Optional)

1. Go to https://tavily.com
2. Sign up and get API key
3. Add to `.env` as TAVILY_API_KEY

## 4. Running DeepScholar

### Option 1: Streamlit UI (Recommended)

```bash
python main.py --ui
# or
streamlit run app/frontend/streamlit_app.py
```

Open browser to: http://localhost:8501

### Option 2: Interactive Mode

```bash
python main.py --interactive
```

### Option 3: Demo Mode

```bash
python main.py --demo
```

### Option 4: Docker

```bash
# Build
docker build -t deepscholar:latest .

# Run
docker run -p 8501:8501 -e OPENAI_API_KEY=your_key deepscholar:latest

# Or with docker-compose
docker-compose up -d
```

## 5. First Steps

1. **Open the UI**: http://localhost:8501
2. **Upload Documents**: Use "Document Management" page
3. **Ask Questions**: Use "Chat" page
4. **Generate Reports**: Use "Generate Report" page

## 6. Common Issues

### Issue: API Key Not Found
```
Solution: Check .env file, ensure key is set correctly
```

### Issue: No modules found
```
Solution: Make sure virtual environment is activated
pip install -r requirements.txt
```

### Issue: Port 8501 already in use
```
Solution: streamlit run app/frontend/streamlit_app.py --server.port 8502
```

## 7. Advanced Configuration

See `config/settings.py` for all available options.

Key settings:
- `LLM_PROVIDER`: openai or gemini
- `VECTORDB_TYPE`: faiss or chroma
- `WEB_SEARCH_PROVIDER`: tavily, serpapi, or google
- `RETRIEVAL_TOP_K`: Number of results to retrieve
- `CONTEXT_WINDOW_TOKENS`: Max context size

## 8. Next Steps

- Check README.md for detailed documentation
- Review examples.py for usage patterns
- Explore the Streamlit UI features
- Customize configuration as needed

## 9. Support

For issues:
1. Check the logs in `./logs/`
2. Review error messages
3. Check documentation
4. Try examples.py --example N

Enjoy using DeepScholar!
"""
