"""Research Agent for DeepScholar."""

from typing import Dict, Any, List, Optional, Tuple
import logging

from app.retrieval import RAGPipeline
from app.memory import ConversationMemory, MemoryManager
from app.web_search import WebSearcher
from .llm_orchestrator import LLMOrchestrator
from app.utils.logger import get_logger
from app.utils.text_utils import extract_keywords

logger = get_logger(__name__)


class ResearchAgent:
    """Intelligent research agent for answering questions."""

    def __init__(
        self,
        rag_pipeline: RAGPipeline,
        llm_orchestrator: LLMOrchestrator,
        memory_manager: MemoryManager,
        enable_web_search: bool = True,
    ):
        """
        Initialize research agent.

        Args:
            rag_pipeline: RAG pipeline for document retrieval
            llm_orchestrator: LLM orchestrator for generation
            memory_manager: Memory manager for conversation history
            enable_web_search: Whether to enable web search
        """
        self.rag_pipeline = rag_pipeline
        self.llm_orchestrator = llm_orchestrator
        self.memory_manager = memory_manager
        self.conversation = memory_manager.get_conversation()
        self.web_searcher = WebSearcher() if enable_web_search else None
        self.enable_web_search = enable_web_search

    def answer(
        self,
        query: str,
        use_web_search: bool = False,
        use_documents: bool = True,
        stream: bool = False,
    ) -> Dict[str, Any]:
        """
        Answer a research question.

        Args:
            query: Research question
            use_web_search: Whether to search the web
            use_documents: Whether to search documents
            stream: Whether to stream the response

        Returns:
            Dict with answer, sources, and metadata
        """
        logger.info(f"Processing query: {query[:100]}...")

        # Retrieve context from documents
        context_str = ""
        sources = []

        if use_documents:
            context_str, doc_sources = self.rag_pipeline.retrieve_context(query)
            sources.extend(doc_sources)

        # Search the web if enabled
        web_results = []
        if use_web_search and self.web_searcher:
            web_results = self.web_searcher.search(query, max_results=3)
            sources.extend(
                [
                    {
                        "content": r.get("snippet", ""),
                        "score": 0.0,
                        "metadata": {"url": r.get("url", ""), "title": r.get("title", "")},
                    }
                    for r in web_results
                ]
            )

        # Prepare prompt
        full_context = f"Retrieved Information:\n{context_str}"
        if web_results:
            web_context = "\n\nWeb Search Results:\n"
            for i, result in enumerate(web_results, 1):
                web_context += f"{i}. {result['title']}\n{result['snippet']}\nSource: {result['url']}\n\n"
            full_context += web_context

        prompt = self.rag_pipeline.prepare_prompt(query, full_context)

        # Get system context
        system_context = self.conversation.get_system_context()

        # Generate response
        if stream:
            response_text = ""
            logger.info("Streaming response...")
            # For now, non-streaming. Streaming can be implemented in UI
            response_text = self.llm_orchestrator.generate(
                prompt, system_context=system_context
            )
        else:
            response_text = self.llm_orchestrator.generate(
                prompt, system_context=system_context
            )

        # Estimate tokens
        tokens_used = self.llm_orchestrator.count_tokens(prompt + response_text)

        # Store in memory
        self.conversation.add_message("user", query, tokens=self.llm_orchestrator.count_tokens(query), sources=sources)
        self.conversation.add_message(
            "assistant",
            response_text,
            tokens=self.llm_orchestrator.count_tokens(response_text),
            sources=sources,
        )

        return {
            "query": query,
            "answer": response_text,
            "sources": sources,
            "web_results": web_results,
            "tokens_used": tokens_used,
            "conversation_context": self.conversation.get_stats(),
        }

    def generate_report(
        self,
        title: str,
        research_topic: str,
        format: str = "markdown",
    ) -> Dict[str, Any]:
        """
        Generate a research report.

        Args:
            title: Report title
            research_topic: Research topic
            format: Output format (markdown, pdf, docx)

        Returns:
            Dict with report content and metadata
        """
        logger.info(f"Generating report: {title}")

        # Retrieve relevant information
        context, sources = self.rag_pipeline.retrieve_context(research_topic)

        # Generate report sections
        report_sections = {}

        # Executive Summary
        summary_prompt = f"Write a brief executive summary (100-150 words) about: {research_topic}\n\nContext: {context[:500]}"
        report_sections["executive_summary"] = self.llm_orchestrator.generate(summary_prompt)

        # Key Findings
        findings_prompt = f"List the key findings about {research_topic} based on this information:\n\n{context}"
        report_sections["key_findings"] = self.llm_orchestrator.generate(findings_prompt)

        # Detailed Analysis
        analysis_prompt = f"Provide a detailed analysis of {research_topic}:\n\n{context}"
        report_sections["detailed_analysis"] = self.llm_orchestrator.generate(analysis_prompt)

        # Conclusions
        conclusion_prompt = f"Write conclusions about {research_topic} based on the provided information."
        report_sections["conclusion"] = self.llm_orchestrator.generate(conclusion_prompt)

        # Format report
        if format == "markdown":
            report_text = self._format_report_markdown(title, report_sections, sources)
        elif format == "html":
            report_text = self._format_report_html(title, report_sections, sources)
        else:
            report_text = self._format_report_markdown(title, report_sections, sources)

        return {
            "title": title,
            "topic": research_topic,
            "format": format,
            "content": report_text,
            "sections": report_sections,
            "sources": sources,
        }

    @staticmethod
    def _format_report_markdown(
        title: str, sections: Dict[str, str], sources: List[Dict]
    ) -> str:
        """Format report as Markdown."""
        report = f"# {title}\n\n"

        report += "## Executive Summary\n\n"
        report += sections.get("executive_summary", "") + "\n\n"

        report += "## Key Findings\n\n"
        report += sections.get("key_findings", "") + "\n\n"

        report += "## Detailed Analysis\n\n"
        report += sections.get("detailed_analysis", "") + "\n\n"

        report += "## Conclusion\n\n"
        report += sections.get("conclusion", "") + "\n\n"

        report += "## Sources\n\n"
        for i, source in enumerate(sources, 1):
            report += f"{i}. {source.get('content', '')[:100]}\n"

        return report

    @staticmethod
    def _format_report_html(
        title: str, sections: Dict[str, str], sources: List[Dict]
    ) -> str:
        """Format report as HTML."""
        html = f"""<html>
<head><title>{title}</title></head>
<body>
<h1>{title}</h1>
<h2>Executive Summary</h2>
<p>{sections.get('executive_summary', '')}</p>
<h2>Key Findings</h2>
<p>{sections.get('key_findings', '')}</p>
<h2>Detailed Analysis</h2>
<p>{sections.get('detailed_analysis', '')}</p>
<h2>Conclusion</h2>
<p>{sections.get('conclusion', '')}</p>
</body>
</html>"""
        return html

    def get_follow_up_questions(self, context: str, num_questions: int = 3) -> List[str]:
        """
        Generate follow-up questions.

        Args:
            context: Conversation context
            num_questions: Number of questions to generate

        Returns:
            List of follow-up questions
        """
        prompt = f"""Based on this research context, generate {num_questions} follow-up research questions:

{context}

Generate questions in a numbered list format."""

        response = self.llm_orchestrator.generate(prompt)
        # Simple parsing
        questions = [q.strip() for q in response.split("\n") if q.strip()]
        return questions[:num_questions]
