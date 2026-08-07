"""
Google Gemini AI Integration for Capital OS.
Supports gemini-2.5-flash, gemini-1.5-pro, and fallback reasoning.
"""

import os
import logging
from typing import Dict, Any, Optional
import httpx
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger("gemini_provider")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")



class GeminiProvider:
    DEFAULT_MODEL = "gemini-2.5-flash"

    @classmethod
    def generate_wealth_analysis(cls, prompt: str, model_name: Optional[str] = None) -> Optional[str]:
        if not GEMINI_API_KEY:
            logger.warning("No GEMINI_API_KEY set.")
            return None

        model = model_name or cls.DEFAULT_MODEL
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }

        try:
            with httpx.Client(timeout=15.0) as client:
                resp = client.post(url, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        if parts:
                            return parts[0].get("text")
                logger.error(f"Gemini API returned status {resp.status_code}: {resp.text[:200]}")
                return None
        except Exception as e:
            logger.error(f"Gemini generation error: {e}")
            return None
