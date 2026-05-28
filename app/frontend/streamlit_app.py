"""DeepScholar - Professional AI Research Assistant Frontend
A minimalist, modern web interface for intelligent document analysis and knowledge discovery.
"""

import streamlit as st
import os
import sys
from pathlib import Path
from datetime import datetime

# Add app to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import get_settings
from app.document_processing import DocumentProcessor
from app.vectorstore import VectorStore, EmbeddingManager
from app.retrieval import RAGPipeline
from app.agents import ResearchAgent, LLMOrchestrator
from app.memory import MemoryManager
from app.web_search import WebSearcher
from app.reporting import ReportGenerator
from app.utils.logger import setup_logger, get_logger

# Setup logging
setup_logger("deepscholar", log_level="INFO")
logger = get_logger(__name__)

# Page configuration
st.set_page_config(
    page_title="DeepScholar",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Professional Minimalist CSS - Force Light Theme
st.markdown(
    """
    <style>
    /* Force Light Theme */
    :root {
        --primary: #1a1a1a;
        --secondary: #2d2d2d;
        --accent: #0066cc;
        --accent-light: #0052a3;
        --border: #e0e0e0;
        --text-main: #1a1a1a;
        --text-secondary: #666666;
        --bg-light: #f5f5f5;
        --bg-white: #ffffff;
    }
    
    * {
        background-color: white !important;
        color: #1a1a1a !important;
    }
    
    html, body {
        background-color: #ffffff !important;
        color: #1a1a1a !important;
    }
    
    [data-testid="stAppViewContainer"] {
        background-color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #f8f8f8 !important;
    }
    
    .stSidebar {
        background-color: #f8f8f8 !important;
    }
    
    /* Typography */
    h1 {
        font-size: 3.5rem;
        font-weight: 300;
        letter-spacing: -0.02em;
        line-height: 1.1;
        margin: 0;
        color: #1a1a1a !important;
    }
    
    h2 {
        font-size: 2rem;
        font-weight: 300;
        letter-spacing: -0.01em;
        margin: 2.5rem 0 1rem 0;
        color: #1a1a1a !important;
    }
    
    h3 {
        font-size: 1.2rem;
        font-weight: 500;
        letter-spacing: -0.005em;
        margin: 1.5rem 0 0.75rem 0;
        color: #1a1a1a !important;
    }
    
    p {
        font-size: 1rem;
        line-height: 1.6;
        color: #666666 !important;
        margin: 0.5rem 0;
    }
    
    /* Override Streamlit Text */
    .stMarkdown, .stMarkdown p {
        color: #1a1a1a !important;
        background-color: transparent !important;
    }
    
    /* Buttons and Controls */
    button {
        background-color: #0066cc !important;
        color: white !important;
        border: none !important;
    }
    
    button:hover {
        background-color: #0052a3 !important;
    }
    
    /* Inputs */
    input, textarea, select {
        background-color: #ffffff !important;
        color: #1a1a1a !important;
        border: 1px solid #e0e0e0 !important;
    }
    
    input:focus, textarea:focus, select:focus {
        background-color: #ffffff !important;
        color: #1a1a1a !important;
        border-color: #0066cc !important;
    }
    
    /* Hero Section */
    .hero {
        padding: 4rem 2rem;
        text-align: center;
        background: linear-gradient(135deg, #f5f5f5 0%, #ffffff 100%);
        border-bottom: 1px solid var(--border);
        margin-bottom: 3rem;
    }
    
    .hero h1 {
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #1a1a1a 0%, #333333 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
        color: var(--text-secondary);
        max-width: 600px;
        margin: 1rem auto 2rem auto;
        font-weight: 300;
    }
    
    /* Cards */
    .card {
        background: var(--bg-white);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 2rem;
        margin: 1.5rem 0;
        transition: all 0.3s ease;
    }
    
    .card:hover {
        border-color: var(--accent);
        box-shadow: 0 8px 24px rgba(0, 102, 204, 0.08);
    }
    
    .card-title {
        font-size: 1.1rem;
        font-weight: 500;
        margin-bottom: 1rem;
        color: var(--text-main);
    }
    
    .card-description {
        font-size: 0.95rem;
        color: var(--text-secondary);
        line-height: 1.6;
    }
    
    /* Input Elements */
    .stTextInput input,
    .stTextArea textarea,
    .stSelectbox select {
        border: 1px solid var(--border) !important;
        border-radius: 4px !important;
        padding: 0.75rem !important;
        font-size: 0.95rem !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }
    
    .stTextInput input:focus,
    .stTextArea textarea:focus,
    .stSelectbox select:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1) !important;
    }
    
    /* Sidebar */
    .sidebar-title {
        font-size: 1.3rem;
        font-weight: 500;
        margin: 1.5rem 0 1rem 0;
        color: var(--text-main);
    }
    
    /* Section Header */
    .section-header {
        padding: 2rem 0 1rem 0;
        border-bottom: 1px solid var(--border);
        margin-bottom: 2rem;
    }
    
    .section-header h2 {
        margin: 0 0 0.5rem 0;
        color: var(--text-main);
    }
    
    .section-description {
        color: var(--text-secondary);
        font-size: 0.95rem;
    }
    
    /* Source Card */
    .source-item {
        border-left: 3px solid var(--accent);
        padding: 1.5rem;
        margin: 1rem 0;
        background: var(--bg-light);
        border-radius: 4px;
    }
    
    .source-title {
        font-weight: 500;
        margin-bottom: 0.5rem;
        color: var(--text-main);
    }
    
    .source-excerpt {
        color: var(--text-secondary);
        font-size: 0.9rem;
        line-height: 1.5;
        margin-bottom: 1rem;
    }
    
    .source-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.85rem;
        color: var(--text-secondary);
    }
    
    /* Response Container */
    .response-box {
        background: var(--bg-light);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 2rem;
        margin: 2rem 0;
        line-height: 1.8;
    }
    
    /* Stats Grid */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .stat-card {
        padding: 1.5rem;
        background: var(--bg-light);
        border-radius: 4px;
        border: 1px solid var(--border);
    }
    
    .stat-value {
        font-size: 1.8rem;
        font-weight: 300;
        color: var(--accent);
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        font-size: 0.85rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Footer */
    .footer {
        margin-top: 4rem;
        padding-top: 2rem;
        border-top: 1px solid var(--border);
        text-align: center;
        color: var(--text-secondary);
        font-size: 0.85rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def initialize_deepscholar():
    """Initialize DeepScholar components."""
    try:
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

        return {
            "embedding_manager": embedding_manager,
            "vector_store": vector_store,
            "rag_pipeline": rag_pipeline,
            "llm_orchestrator": llm_orchestrator,
            "memory_manager": memory_manager,
            "research_agent": research_agent,
            "report_generator": report_generator,
        }
    except Exception as e:
        st.error(f"Failed to initialize: {str(e)}")
        logger.error(f"Initialization error: {str(e)}")
        return None


def show_landing():
    """Landing page."""
    st.markdown(
        """
        <div class="hero">
            <h1>DeepScholar</h1>
            <p class="hero-subtitle">
                An intelligent AI research assistant for document analysis and knowledge discovery.
                Upload your documents, ask questions, and get research-backed answers with citations.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Feature cards
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="card">
                <div class="card-title">Research Chat</div>
                <div class="card-description">
                    Ask natural language questions and receive AI-powered responses backed by your documents.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="card">
                <div class="card-title">Document Management</div>
                <div class="card-description">
                    Upload and organize your documents to build a searchable knowledge base.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="card">
                <div class="card-title">Report Generation</div>
                <div class="card-description">
                    Generate comprehensive research reports based on your documents and analysis.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="footer">
            <p>Powered by Google Generative AI · Built with Streamlit</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_chat(components):
    """Chat page."""
    st.markdown(
        """
        <div class="section-header">
            <h2>Research Chat</h2>
            <p class="section-description">Ask questions and get research-backed answers with citations</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        use_documents = st.checkbox("Use Documents", value=True)
    with col2:
        use_web_search = st.checkbox("Enable Web Search", value=False)
    with col3:
        stream_response = st.checkbox("Stream Response", value=False)

    user_query = st.text_area(
        "Enter your research question",
        placeholder="What are the latest developments in quantum computing?",
        height=80,
    )

    if st.button("Submit", key="chat_submit", use_container_width=False):
        if user_query.strip():
            with st.spinner("Analyzing..."):
                try:
                    result = components["research_agent"].answer(
                        user_query,
                        use_web_search=use_web_search,
                        use_documents=use_documents,
                        stream=stream_response,
                    )

                    st.markdown(
                        '<div class="response-box">',
                        unsafe_allow_html=True,
                    )
                    st.write(result["answer"])
                    st.markdown("</div>", unsafe_allow_html=True)

                    if result.get("sources"):
                        st.markdown("### Sources")
                        for i, source in enumerate(result["sources"][:3], 1):
                            content = source.get('content', '')[:200]
                            score = source.get('score', 0)
                            st.markdown(
                                f"""
                                <div class="source-item">
                                    <div class="source-title">Source {i}</div>
                                    <div class="source-excerpt">{content}...</div>
                                    <div class="source-meta">
                                        <span>Relevance: {score:.0%}</span>
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                except Exception as e:
                    st.error(f"Error: {str(e)}")


def show_documents(components):
    """Document management page."""
    st.markdown(
        """
        <div class="section-header">
            <h2>Document Management</h2>
            <p class="section-description">Upload and organize your knowledge base</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Upload Documents")
        uploaded_files = st.file_uploader(
            "Select files (PDF, DOCX, TXT)",
            type=["pdf", "docx", "txt"],
            accept_multiple_files=True,
        )

        if uploaded_files and st.button("Process", key="doc_process"):
            progress_bar = st.progress(0)

            try:
                processor = DocumentProcessor(chunk_size=1000, chunk_overlap=200)
                total = len(uploaded_files)

                for idx, file in enumerate(uploaded_files):
                    result = processor.process_document(file)

                    components["rag_pipeline"].add_documents(
                        documents=result["chunks"],
                        metadata=[{"filename": result["metadata"]["filename"]}
                                  for _ in result["chunks"]],
                    )

                    st.success(f"Processed: {result['metadata']['filename']}")
                    progress_bar.progress((idx + 1) / total)

                st.balloons()

            except Exception as e:
                st.error(f"Error: {str(e)}")

    with col2:
        st.subheader("Knowledge Base")
        try:
            stats = components["vector_store"].get_stats()
            st.metric("Documents", stats.get('total_documents', 0))
            st.metric("Dimension", stats.get('embedding_dimension', 0))
        except Exception as e:
            st.caption(f"Status: Unavailable")


def show_search(components):
    """Search page."""
    st.markdown(
        """
        <div class="section-header">
            <h2>Document Search</h2>
            <p class="section-description">Search your knowledge base</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    search_query = st.text_input("Enter search query", placeholder="Search documents...")
    top_k = st.slider("Number of results", 1, 20, 5)

    if search_query:
        try:
            results = components["rag_pipeline"].retrieve(search_query, top_k=top_k)

            if results:
                for i, result in enumerate(results, 1):
                    content = result.get('content', '')[:300]
                    score = result.get('score', 0)
                    st.markdown(
                        f"""
                        <div class="source-item">
                            <div class="source-title">Result {i}</div>
                            <div class="source-excerpt">{content}...</div>
                            <div class="source-meta">
                                <span>Score: {score:.0%}</span>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            else:
                st.info("No results found")

        except Exception as e:
            st.error(f"Error: {str(e)}")


def show_reports(components):
    """Reports page."""
    st.markdown(
        """
        <div class="section-header">
            <h2>Generate Report</h2>
            <p class="section-description">Create research reports from your knowledge base</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    report_topic = st.text_input("Report topic", placeholder="e.g., Machine Learning Advances")
    report_type = st.selectbox(
        "Report type",
        ["Executive Summary", "Detailed Analysis", "Literature Review"]
    )

    if st.button("Generate", key="report_gen"):
        if report_topic:
            with st.spinner("Generating report..."):
                try:
                    report = components["report_generator"].generate_report(
                        topic=report_topic,
                        report_type=report_type,
                    )

                    st.markdown(
                        '<div class="response-box">',
                        unsafe_allow_html=True,
                    )
                    st.write(report["content"])
                    st.markdown("</div>", unsafe_allow_html=True)

                    st.download_button(
                        "Download Report",
                        report["content"],
                        f"{report_topic.replace(' ', '_')}_report.md",
                    )

                except Exception as e:
                    st.error(f"Error: {str(e)}")


def main():
    """Main application."""

    # Sidebar
    with st.sidebar:
        st.markdown('<div class="sidebar-title">Navigation</div>', unsafe_allow_html=True)

        page = st.radio(
            "Select",
            ["Home", "Chat", "Documents", "Search", "Reports"],
            key="main_nav",
            label_visibility="collapsed",
        )

        st.markdown("---")

        if page != "Home":
            if "components" not in st.session_state:
                components = initialize_deepscholar()
                if components is None:
                    st.error("Initialization failed")
                    return
                st.session_state.components = components
                st.session_state.components["memory_manager"].start_session()

            components = st.session_state.components

            col1, col2 = st.columns(2)
            with col1:
                if st.button("New Session"):
                    try:
                        components["memory_manager"].start_session()
                        st.success("New session")
                    except:
                        pass

            with col2:
                if st.button("Save"):
                    try:
                        components["memory_manager"].save_session()
                        st.success("Saved")
                    except:
                        pass

    # Pages
    if page == "Home":
        show_landing()
    else:
        if "components" not in st.session_state:
            components = initialize_deepscholar()
            if components is None:
                st.error("Failed to initialize")
                return
            st.session_state.components = components
            st.session_state.components["memory_manager"].start_session()

        components = st.session_state.components

        if page == "Chat":
            show_chat(components)
        elif page == "Documents":
            show_documents(components)
        elif page == "Search":
            show_search(components)
        elif page == "Reports":
            show_reports(components)


if __name__ == "__main__":
    main()
