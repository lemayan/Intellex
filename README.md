# DeepScholar

**An intelligent AI research assistant for document analysis, semantic search, and knowledge discovery.**

DeepScholar combines Retrieval-Augmented Generation (RAG), vector embeddings, and large language models into a production-grade research platform. Upload your documents, ask questions in natural language, and receive accurate, research-backed answers with citations.

---

## Overview

DeepScholar is built for researchers, analysts, and engineers who need to extract insights from large document collections quickly. It features a modern dark-mode web interface, a high-performance Python API, and deep integration with Google Gemini for natural language understanding.

### Core Capabilities

- **Research Chat** — Ask natural language questions and get direct, expert-level answers sourced from your documents or the web
- **Document Management** — Upload PDF, DOCX, and TXT files into a searchable vector knowledge base
- **Semantic Search** — Similarity-based retrieval using FAISS vector indexing
- **Conversation Memory** — Context-aware responses that remember previous turns in a session
- **Report Generation** — Generate structured research reports in Markdown format
- **Web Search** — Optionally augment answers with real-time web results

---

## Architecture

DeepScholar is a decoupled two-tier application:

```
frontend_web/          React + Vite single-page application
app/api.py             FastAPI REST backend
app/agents/            LLM orchestration (Gemini / OpenAI)
app/retrieval/         RAG pipeline and document retrieval
app/vectorstore/       FAISS vector database and embeddings
app/document_processing/  PDF, DOCX, TXT processing
app/memory/            Session-based conversation memory
app/reporting/         Research report generation
config/settings.py     Environment-based configuration
```

**Frontend** communicates with the **Backend API** over HTTP. The backend initializes AI components lazily on first use for a fast startup time.

---

## Tech Stack

| Layer            | Technology                          |
|------------------|-------------------------------------|
| Frontend         | React, Vite, Vanilla CSS            |
| Backend API      | FastAPI, Uvicorn                    |
| LLM Provider     | Google Gemini (gemini-2.5-flash)    |
| Embeddings       | Configurable (simple / HuggingFace / OpenAI) |
| Vector Database  | FAISS                               |
| Document Parsing | PyPDF2, pdfplumber, python-docx     |
| Memory           | In-memory session with token pruning |

---

## Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- A Google Gemini API key — obtain one free at [aistudio.google.com](https://aistudio.google.com)

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/deepscholar.git
cd deepscholar
```

### 2. Set up the Python environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example environment file and fill in your API keys:

```bash
cp .env.example .env
```

Open `.env` and set the following required values:

```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
EMBEDDING_PROVIDER=simple
VECTORDB_TYPE=faiss
```

### 5. Install frontend dependencies

```bash
cd frontend_web
npm install
cd ..
```

---

## Running the Application

DeepScholar requires two processes running simultaneously: the backend API and the frontend development server.

### Terminal 1 — Start the Backend API

```bash
uvicorn app.api:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

You can verify it is running by visiting `http://localhost:8000/api/health` in your browser, which should return:

```json
{ "status": "ok", "message": "DeepScholar API is running" }
```

### Terminal 2 — Start the Frontend

```bash
cd frontend_web
npm run dev
```

The application will be available at `http://localhost:5173`.

---

## Usage

### Research Chat

1. Open `http://localhost:5173` in your browser
2. Navigate to **Research Chat** in the sidebar
3. Toggle **Document Search** if you have uploaded documents
4. Type your question and press Enter or click the send button

### Uploading Documents

1. Navigate to **Documents** in the sidebar
2. Drag and drop PDF, DOCX, or TXT files into the upload zone, or click to browse
3. Click **Upload** — files are processed, chunked, and indexed into the vector database
4. Return to Research Chat and enable **Document Search** to query your documents

---

## API Reference

The backend exposes the following REST endpoints:

| Method | Endpoint          | Description                          |
|--------|-------------------|--------------------------------------|
| GET    | `/api/health`     | Check if the API is running          |
| POST   | `/api/chat`       | Submit a research query              |
| POST   | `/api/documents`  | Upload and index documents           |
| GET    | `/api/search`     | Search the vector knowledge base     |
| POST   | `/api/reports`    | Generate a structured research report|
| GET    | `/api/stats`      | Get vector store statistics          |

### POST /api/chat

**Request body:**
```json
{
  "query": "What are the key findings in the uploaded papers?",
  "use_documents": true,
  "use_web_search": false
}
```

**Response:**
```json
{
  "answer": "...",
  "sources": [
    {
      "content": "...",
      "score": 0.87,
      "metadata": { "filename": "paper.pdf" }
    }
  ]
}
```

---

## Configuration Reference

All configuration is loaded from the `.env` file.

| Variable                     | Default               | Description                              |
|------------------------------|-----------------------|------------------------------------------|
| `LLM_PROVIDER`               | `gemini`              | LLM provider: `gemini` or `openai`       |
| `GEMINI_API_KEY`             | —                     | Google Gemini API key (required)         |
| `GEMINI_MODEL`               | `gemini-2.5-flash`    | Gemini model name                        |
| `OPENAI_API_KEY`             | —                     | OpenAI API key (if using OpenAI)         |
| `OPENAI_MODEL`               | `gpt-4-turbo-preview` | OpenAI model name                        |
| `EMBEDDING_PROVIDER`         | `simple`              | Embedding backend: `simple`, `openai`, `huggingface` |
| `VECTORDB_TYPE`              | `faiss`               | Vector database: `faiss` or `chroma`     |
| `VECTORDB_PATH`              | `./data/embeddings`   | Path to store the vector index           |
| `WEB_SEARCH_PROVIDER`        | `tavily`              | Web search provider: `tavily`, `serpapi` |
| `TAVILY_API_KEY`             | —                     | Tavily API key for web search            |
| `RETRIEVAL_TOP_K`            | `5`                   | Number of document chunks to retrieve    |
| `DOCUMENT_CHUNK_SIZE`        | `1000`                | Characters per document chunk            |
| `DOCUMENT_CHUNK_OVERLAP`     | `200`                 | Overlap between chunks                   |
| `MEMORY_MAX_TOKENS`          | `4000`                | Max conversation memory tokens           |
| `LOG_LEVEL`                  | `INFO`                | Logging level                            |

---

## Docker Deployment

A Dockerfile and Docker Compose configuration are included for containerized deployment.

```bash
docker-compose up -d
```

This starts the backend API in a container. For the frontend in production, build the static assets:

```bash
cd frontend_web
npm run build
```

---

## Project Structure

```
DeepScholar/
├── app/
│   ├── api.py                    FastAPI application
│   ├── agents/                   LLM orchestration
│   ├── retrieval/                RAG pipeline
│   ├── vectorstore/              Vector database layer
│   ├── document_processing/      File parsing and chunking
│   ├── memory/                   Conversation memory
│   ├── reporting/                Report generation
│   └── utils/                    Logging and utilities
├── frontend_web/
│   ├── src/
│   │   ├── App.jsx               Application layout and routing
│   │   ├── index.css             Global design system
│   │   └── pages/
│   │       ├── Chat.jsx          Research chat interface
│   │       └── Documents.jsx     Document management
│   └── package.json
├── config/
│   └── settings.py               Pydantic configuration
├── data/                         Document and embedding storage
├── .env                          Environment variables
├── .env.example                  Environment template
├── requirements.txt              Python dependencies
├── Dockerfile
└── docker-compose.yml
```

---

## Troubleshooting

**"Could not reach the server"**
Ensure the backend is running: `uvicorn app.api:app --port 8000`

**Quota exceeded (429 error)**
Your Gemini free tier has been exhausted. Either wait for the daily quota to reset or enable billing at [aistudio.google.com](https://aistudio.google.com).

**Model not found (404 error)**
Ensure `GEMINI_MODEL` in your `.env` is set to a supported model such as `gemini-2.5-flash` or `gemini-2.0-flash`.

**Documents not being retrieved in chat**
Make sure you have uploaded documents via the Documents page and that **Document Search** is toggled on in the chat interface.

---

## License

MIT License. See `LICENSE` for details.

---

**Created by Nikita Simiyu**
