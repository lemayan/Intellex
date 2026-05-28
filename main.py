"""DeepScholar - AI Research Assistant Main Entry Point."""

import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import get_settings
from app.document_processing import DocumentProcessor
from app.vectorstore import VectorStore, EmbeddingManager
from app.retrieval import RAGPipeline
from app.agents import ResearchAgent, LLMOrchestrator
from app.memory import MemoryManager
from app.utils.logger import setup_logger, get_logger

logger = setup_logger("deepscholar")


class DeepScholar:
    """Main DeepScholar application class."""

    def __init__(self):
        """Initialize DeepScholar."""
        self.settings = get_settings()
        logger.info("Initializing DeepScholar...")

        # Initialize components
        self.embedding_manager = EmbeddingManager()
        self.vector_store = VectorStore(embedding_manager=self.embedding_manager)
        self.rag_pipeline = RAGPipeline(vector_store=self.vector_store)
        self.llm_orchestrator = LLMOrchestrator()
        self.memory_manager = MemoryManager()
        self.research_agent = ResearchAgent(
            rag_pipeline=self.rag_pipeline,
            llm_orchestrator=self.llm_orchestrator,
            memory_manager=self.memory_manager,
        )
        self.document_processor = DocumentProcessor()

        logger.info("DeepScholar initialized successfully")

    def process_documents(self, file_paths: list) -> dict:
        """
        Process documents.

        Args:
            file_paths: List of document file paths

        Returns:
            Processing results
        """
        results = []

        for file_path in file_paths:
            try:
                result = self.document_processor.process_document(file_path)
                doc_ids = self.rag_pipeline.add_documents(
                    documents=result["chunks"],
                    metadata=[
                        {"filename": result["metadata"]["filename"], "chunk_index": i}
                        for i in range(len(result["chunks"]))
                    ],
                )
                results.append(
                    {
                        "file": file_path,
                        "chunks": len(result["chunks"]),
                        "doc_ids": doc_ids,
                        "status": "success",
                    }
                )
            except Exception as e:
                logger.error(f"Error processing {file_path}: {str(e)}")
                results.append(
                    {"file": file_path, "status": "error", "error": str(e)}
                )

        return {"processed": results}

    def answer_question(self, query: str, use_web_search: bool = False) -> dict:
        """
        Answer a research question.

        Args:
            query: Research question
            use_web_search: Whether to search the web

        Returns:
            Answer with sources
        """
        return self.research_agent.answer(query, use_web_search=use_web_search)

    def generate_report(self, title: str, topic: str) -> dict:
        """
        Generate a research report.

        Args:
            title: Report title
            topic: Research topic

        Returns:
            Report content
        """
        return self.research_agent.generate_report(title, topic)

    def get_stats(self) -> dict:
        """Get system statistics."""
        return {
            "vector_store": self.vector_store.get_stats(),
            "rag_pipeline": self.rag_pipeline.get_stats(),
            "memory": self.memory_manager.get_conversation().get_stats(),
        }


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="DeepScholar - AI Research Assistant")
    parser.add_argument("--ui", action="store_true", help="Launch Streamlit UI")
    parser.add_argument("--interactive", action="store_true", help="Interactive mode")
    parser.add_argument("--demo", action="store_true", help="Run demo")

    args = parser.parse_args()

    if args.ui:
        # Launch Streamlit
        import subprocess
        import sys

        subprocess.run(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                "app/frontend/streamlit_app.py",
                "--logger.level=info",
            ]
        )

    elif args.interactive:
        # Interactive mode
        print("🔬 DeepScholar - Interactive Mode")
        print("-" * 50)

        deepscholar = DeepScholar()

        while True:
            query = input("\n🤖 Ask a question (or 'quit' to exit): ").strip()

            if query.lower() == "quit":
                break

            if query:
                result = deepscholar.answer_question(query)
                print(f"\n📝 Answer:\n{result['answer']}")

                if result["sources"]:
                    print(f"\n📚 Sources ({len(result['sources'])} found):")
                    for i, source in enumerate(result["sources"][:3], 1):
                        print(f"{i}. {source['content'][:100]}...")

    elif args.demo:
        # Run demo
        print("🔬 DeepScholar - Demo Mode")
        print("-" * 50)

        deepscholar = DeepScholar()

        # Example questions
        demo_questions = [
            "What is machine learning?",
            "Explain quantum computing",
            "How does AI work?",
        ]

        for question in demo_questions:
            print(f"\n❓ Question: {question}")
            try:
                result = deepscholar.answer_question(question)
                print(f"✅ Answer: {result['answer'][:200]}...")
            except Exception as e:
                print(f"❌ Error: {str(e)}")

    else:
        # Show help
        parser.print_help()


if __name__ == "__main__":
    main()
