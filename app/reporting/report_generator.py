"""Report generation and export functionality."""

from typing import Dict, Any, Optional, List
from pathlib import Path
import json
import logging
from datetime import datetime

from app.utils.logger import get_logger

logger = get_logger(__name__)


class ReportGenerator:
    """Generate and export research reports."""

    def __init__(self, output_dir: str = "./reports"):
        """
        Initialize report generator.

        Args:
            output_dir: Directory for saving reports
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_markdown_report(
        self,
        title: str,
        content: Dict[str, str],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Generate Markdown report.

        Args:
            title: Report title
            content: Report sections (dict with section names and content)
            metadata: Optional metadata

        Returns:
            Markdown content
        """
        md = f"# {title}\n\n"

        if metadata:
            md += "_Generated on: " + metadata.get("generated_at", "") + "_\n\n"

        for section_name, section_content in content.items():
            md += f"## {section_name.replace('_', ' ').title()}\n\n"
            md += section_content + "\n\n"

        return md

    def generate_html_report(
        self,
        title: str,
        content: Dict[str, str],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Generate HTML report.

        Args:
            title: Report title
            content: Report sections
            metadata: Optional metadata

        Returns:
            HTML content
        """
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; }}
        .metadata {{ color: #7f8c8d; font-size: 0.9em; font-style: italic; }}
        .source {{ 
            background: #ecf0f1; 
            padding: 10px; 
            margin: 10px 0; 
            border-left: 4px solid #3498db;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
"""

        if metadata:
            html += f'<p class="metadata">Generated on: {metadata.get("generated_at", "")}</p>\n'

        for section_name, section_content in content.items():
            html += f"<h2>{section_name.replace('_', ' ').title()}</h2>\n"
            html += f"<p>{section_content}</p>\n"

        html += """    </div>
</body>
</html>"""

        return html

    def save_report(
        self,
        title: str,
        content: str,
        format: str = "markdown",
    ) -> Path:
        """
        Save report to file.

        Args:
            title: Report title
            content: Report content
            format: File format (markdown, html, json)

        Returns:
            Path to saved file
        """
        # Sanitize filename
        filename = title.lower().replace(" ", "_").replace("/", "_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{filename}_{timestamp}"

        if format == "markdown":
            filepath = self.output_dir / f"{filename}.md"
        elif format == "html":
            filepath = self.output_dir / f"{filename}.html"
        elif format == "json":
            filepath = self.output_dir / f"{filename}.json"
        else:
            filepath = self.output_dir / f"{filename}.md"

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info(f"Saved report: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Error saving report: {str(e)}")
            return None

    def format_citation(
        self, title: str, url: str, authors: Optional[List[str]] = None
    ) -> str:
        """
        Format a citation.

        Args:
            title: Source title
            url: Source URL
            authors: Optional list of authors

        Returns:
            Formatted citation
        """
        if authors:
            authors_str = ", ".join(authors)
            return f"{authors_str}. \"{title}\" Retrieved from {url}"
        else:
            return f"\"{title}\" Retrieved from {url}"

    def generate_bibliography(
        self, sources: List[Dict[str, Any]]
    ) -> str:
        """
        Generate bibliography from sources.

        Args:
            sources: List of source dictionaries

        Returns:
            Formatted bibliography
        """
        bib = "## Bibliography\n\n"

        for i, source in enumerate(sources, 1):
            title = source.get("title", source.get("content", "")[:50])
            url = source.get("url", source.get("metadata", {}).get("url", ""))

            if url:
                bib += f"{i}. [{title}]({url})\n"
            else:
                bib += f"{i}. {title}\n"

        return bib
