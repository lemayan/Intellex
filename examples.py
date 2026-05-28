"""Example usage of DeepScholar API."""

import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import DeepScholar
from app.utils.logger import setup_logger

# Setup logging
setup_logger("example")


def example_1_basic_qa():
    """Example 1: Basic Q&A."""
    print("\n" + "=" * 60)
    print("Example 1: Basic Q&A")
    print("=" * 60)

    scholar = DeepScholar()

    questions = [
        "What is machine learning?",
        "How does deep learning work?",
        "What are neural networks?",
    ]

    for question in questions:
        print(f"\n❓ Question: {question}")
        try:
            result = scholar.answer_question(question)
            print(f"✅ Answer: {result['answer'][:300]}...")
            print(f"📚 Sources found: {len(result['sources'])}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")


def example_2_web_search():
    """Example 2: Q&A with web search."""
    print("\n" + "=" * 60)
    print("Example 2: Q&A with Web Search")
    print("=" * 60)

    scholar = DeepScholar()

    question = "What are the latest AI trends in 2024?"

    print(f"\n❓ Question: {question}")
    print("(Searching web for latest information...)")

    try:
        result = scholar.answer_question(question, use_web_search=True)
        print(f"✅ Answer: {result['answer'][:400]}...")
        print(f"📚 Total sources: {len(result['sources'])}")
        print(f"🌐 Web results: {len(result['web_results'])}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def example_3_document_processing():
    """Example 3: Process and search documents."""
    print("\n" + "=" * 60)
    print("Example 3: Document Processing")
    print("=" * 60)

    scholar = DeepScholar()

    # Example document paths (you would replace with real files)
    documents = [
        # "path/to/research_paper.pdf",
        # "path/to/document.docx",
    ]

    if documents:
        print("\n📄 Processing documents...")
        result = scholar.process_documents(documents)

        for item in result["processed"]:
            if item["status"] == "success":
                print(f"✅ {item['file']}: {item['chunks']} chunks created")
            else:
                print(f"❌ {item['file']}: {item['error']}")

        # Now ask questions about the documents
        print("\n❓ Asking about uploaded documents...")
        qa_result = scholar.answer_question(
            "Summarize the key findings from the documents"
        )
        print(f"✅ Answer: {qa_result['answer'][:300]}...")


def example_4_report_generation():
    """Example 4: Generate a research report."""
    print("\n" + "=" * 60)
    print("Example 4: Report Generation")
    print("=" * 60)

    scholar = DeepScholar()

    title = "Artificial Intelligence in Modern Healthcare"
    topic = "Applications of AI and machine learning in healthcare diagnostics, treatment planning, and patient outcomes"

    print(f"\n📊 Generating report: {title}")
    print(f"📍 Topic: {topic}")

    try:
        report = scholar.generate_report(title, topic)
        print(f"\n✅ Report generated!")
        print(f"📑 Format: {report['format']}")
        print(f"📚 Sources cited: {len(report['sources'])}")
        print(f"\n{report['content'][:500]}...")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def example_5_memory_management():
    """Example 5: Conversation memory management."""
    print("\n" + "=" * 60)
    print("Example 5: Memory Management")
    print("=" * 60)

    scholar = DeepScholar()

    # Start a new session
    session_id = scholar.memory_manager.start_session()
    print(f"📋 Started new session: {session_id}")

    # Have a conversation
    questions = [
        "What is quantum computing?",
        "How does it differ from classical computing?",
        "What are its applications?",
    ]

    for question in questions:
        print(f"\n❓ Question: {question}")
        result = scholar.answer_question(question)
        print(f"✅ Answered (using conversation context)")

    # Get stats
    stats = scholar.memory_manager.get_conversation().get_stats()
    print(f"\n📊 Session Statistics:")
    print(f"  - Total messages: {stats['total_messages']}")
    print(f"  - Total tokens: {stats['total_tokens']}")
    print(f"  - User messages: {stats['user_messages']}")

    # Save session
    scholar.memory_manager.save_session()
    print(f"💾 Session saved!")


def example_6_advanced_search():
    """Example 6: Advanced search capabilities."""
    print("\n" + "=" * 60)
    print("Example 6: Advanced Search")
    print("=" * 60)

    scholar = DeepScholar()

    # Test vector store
    context, sources = scholar.rag_pipeline.retrieve_context(
        "latest developments in AI"
    )

    print(f"🔍 Retrieved {len(sources)} relevant documents")
    print(f"📝 Context length: {len(context)} characters")

    # Get system stats
    stats = scholar.get_stats()
    print(f"\n📊 System Statistics:")
    import json

    print(json.dumps(stats, indent=2))


def example_7_interactive_mode():
    """Example 7: Interactive chat mode."""
    print("\n" + "=" * 60)
    print("Example 7: Interactive Chat")
    print("=" * 60)
    print("\nStarting interactive mode. Type 'quit' to exit.\n")

    scholar = DeepScholar()

    while True:
        query = input("🤖 Ask a question: ").strip()

        if query.lower() == "quit":
            print("👋 Goodbye!")
            break

        if not query:
            continue

        print("\n⏳ Thinking...")

        try:
            result = scholar.answer_question(query)
            print(f"\n📝 Answer:\n{result['answer']}\n")
            print(f"📚 Sources: {len(result['sources'])} found\n")
        except Exception as e:
            print(f"❌ Error: {str(e)}\n")


def main():
    """Run examples."""
    import argparse

    parser = argparse.ArgumentParser(description="DeepScholar Examples")
    parser.add_argument(
        "--example",
        type=int,
        choices=[1, 2, 3, 4, 5, 6, 7],
        help="Run specific example",
    )

    args = parser.parse_args()

    if args.example == 1:
        example_1_basic_qa()
    elif args.example == 2:
        example_2_web_search()
    elif args.example == 3:
        example_3_document_processing()
    elif args.example == 4:
        example_4_report_generation()
    elif args.example == 5:
        example_5_memory_management()
    elif args.example == 6:
        example_6_advanced_search()
    elif args.example == 7:
        example_7_interactive_mode()
    else:
        print("DeepScholar - Usage Examples\n")
        print("Run specific examples:")
        print("  python examples.py --example 1  # Basic Q&A")
        print("  python examples.py --example 2  # Q&A with web search")
        print("  python examples.py --example 3  # Document processing")
        print("  python examples.py --example 4  # Report generation")
        print("  python examples.py --example 5  # Memory management")
        print("  python examples.py --example 6  # Advanced search")
        print("  python examples.py --example 7  # Interactive mode")


if __name__ == "__main__":
    main()
