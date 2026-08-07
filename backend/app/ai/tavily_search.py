"""
Tavily Live Web Search Service for Capital OS.
Enables real-time market research, ETF news, and investment opportunity discovery.
"""

import os
import logging
from typing import List, Dict, Any
import httpx
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger("tavily_search")

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "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")


class TavilySearchService:
    @classmethod
    def search_investment_opportunities(cls, query: str = "best long term index ETF investments 2026", max_results: int = 5) -> List[Dict[str, Any]]:
        if not TAVILY_API_KEY:
            logger.warning("No TAVILY_API_KEY configured.")
            return []

        url = "https://api.tavily.com/search"
        payload = {
            "api_key": TAVILY_API_KEY,
            "query": query,
            "search_depth": "smart",
            "max_results": max_results,
            "include_answer": True,
        }

        try:
            with httpx.Client(timeout=10.0) as client:
                resp = client.post(url, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    results = data.get("results", [])
                    return [
                        {
                            "title": r.get("title"),
                            "url": r.get("url"),
                            "snippet": r.get("content"),
                            "score": r.get("score"),
                        }
                        for r in results
                    ]
                else:
                    logger.error(f"Tavily API returned status {resp.status_code}: {resp.text}")
                    return []
        except Exception as e:
            logger.error(f"Tavily search failed: {e}")
            return []
