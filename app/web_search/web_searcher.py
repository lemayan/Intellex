"""Web search functionality for research."""

from typing import List, Dict, Any, Optional
import logging
import requests

from app.utils.logger import get_logger
from config.settings import get_settings

logger = get_logger(__name__)
settings = get_settings()


class WebSearcher:
    """Search the web for research information."""

    def __init__(self, provider: Optional[str] = None):
        """
        Initialize web searcher.

        Args:
            provider: Search provider (tavily, serpapi, google)
        """
        self.provider = provider or settings.web_search_provider
        self._validate_provider()

    def _validate_provider(self):
        """Validate and initialize provider."""
        if self.provider == "tavily":
            self.api_key = settings.tavily_api_key
            if not self.api_key:
                logger.warning("Tavily API key not configured")
        elif self.provider == "serpapi":
            self.api_key = settings.serpapi_api_key
            if not self.api_key:
                logger.warning("SerpAPI key not configured")
        elif self.provider == "google":
            self.api_key = settings.google_search_api_key
            self.engine_id = settings.google_search_engine_id
            if not self.api_key or not self.engine_id:
                logger.warning("Google Search API credentials not configured")
        else:
            raise ValueError(f"Unsupported search provider: {self.provider}")

    def search(
        self, query: str, max_results: int = 5, include_snippets: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Search the web.

        Args:
            query: Search query
            max_results: Maximum number of results
            include_snippets: Whether to include result snippets

        Returns:
            List of search results with source information
        """
        logger.info(f"Searching web with {self.provider}: {query}")

        if self.provider == "tavily":
            return self._search_tavily(query, max_results, include_snippets)
        elif self.provider == "serpapi":
            return self._search_serpapi(query, max_results, include_snippets)
        elif self.provider == "google":
            return self._search_google(query, max_results, include_snippets)
        else:
            return self._mock_search_results(query)

    def _search_tavily(
        self, query: str, max_results: int, include_snippets: bool
    ) -> List[Dict[str, Any]]:
        """Search using Tavily API."""
        try:
            url = "https://api.tavily.com/search"
            payload = {
                "api_key": self.api_key,
                "query": query,
                "max_results": max_results,
                "include_answer": include_snippets,
            }

            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()

            data = response.json()
            results = []

            for result in data.get("results", []):
                results.append(
                    {
                        "title": result.get("title", ""),
                        "url": result.get("url", ""),
                        "snippet": result.get("content", ""),
                        "source": "Tavily",
                    }
                )

            logger.info(f"Found {len(results)} results from Tavily")
            return results

        except Exception as e:
            logger.error(f"Error searching Tavily: {str(e)}")
            return self._mock_search_results(query)

    def _search_serpapi(
        self, query: str, max_results: int, include_snippets: bool
    ) -> List[Dict[str, Any]]:
        """Search using SerpAPI."""
        try:
            url = "https://serpapi.com/search"
            params = {"q": query, "api_key": self.api_key, "num": max_results}

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            results = []

            for result in data.get("organic_results", [])[:max_results]:
                results.append(
                    {
                        "title": result.get("title", ""),
                        "url": result.get("link", ""),
                        "snippet": result.get("snippet", ""),
                        "source": "SerpAPI",
                    }
                )

            logger.info(f"Found {len(results)} results from SerpAPI")
            return results

        except Exception as e:
            logger.error(f"Error searching SerpAPI: {str(e)}")
            return self._mock_search_results(query)

    def _search_google(
        self, query: str, max_results: int, include_snippets: bool
    ) -> List[Dict[str, Any]]:
        """Search using Google Custom Search API."""
        try:
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                "q": query,
                "key": self.api_key,
                "cx": self.engine_id,
                "num": max_results,
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            results = []

            for item in data.get("items", []):
                results.append(
                    {
                        "title": item.get("title", ""),
                        "url": item.get("link", ""),
                        "snippet": item.get("snippet", ""),
                        "source": "Google",
                    }
                )

            logger.info(f"Found {len(results)} results from Google")
            return results

        except Exception as e:
            logger.error(f"Error searching Google: {str(e)}")
            return self._mock_search_results(query)

    @staticmethod
    def _mock_search_results(query: str) -> List[Dict[str, Any]]:
        """Return mock search results for demo purposes."""
        logger.warning("Using mock search results (no API configured)")
        return [
            {
                "title": f"Research on {query}",
                "url": "https://example.com/research",
                "snippet": f"Information about {query}...",
                "source": "Demo",
            }
        ]

    def extract_sources(
        self, results: List[Dict[str, Any]]
    ) -> List[Dict[str, str]]:
        """
        Extract citations from search results.

        Args:
            results: Search results

        Returns:
            Formatted citations
        """
        citations = []
        for i, result in enumerate(results, 1):
            citations.append(
                {
                    "number": i,
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "source": result.get("source", ""),
                }
            )
        return citations
