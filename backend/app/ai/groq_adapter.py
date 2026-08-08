"""
Groq Adapter implementation of AIProvider for Capital OS.
Integrates Groq cloud inference (e.g. llama-3.3-70b-versatile) into the standardized AIProvider contract.
"""
from __future__ import annotations

import os
import logging
from typing import Any, Optional
import httpx
from dotenv import load_dotenv

from .provider import AIProvider

load_dotenv()
logger = logging.getLogger("groq_adapter")


class GroqAdapter(AIProvider):
    """
    AIProvider adapter implementation using Groq's high-speed inference engine.
    """

    DEFAULT_MODEL = "llama-3.3-70b-versatile"
    API_URL = "https://api.groq.com/openai/v1/chat/completions"

    def __init__(self, default_model: Optional[str] = None) -> None:
        self.default_model = default_model or self.DEFAULT_MODEL
        self.api_key = os.getenv("GROQ_API_KEY", "")

    def generate(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ) -> str:
        model = kwargs.get("model") or self.default_model

        if not self.api_key:
            logger.warning("No GROQ_API_KEY configured. Returning fallback response.")
            return f"[Groq fallback]: Advice generated for: {prompt[:80]}"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        payload: dict[str, Any] = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
        }
        if max_tokens:
            payload["max_tokens"] = max_tokens

        try:
            with httpx.Client(timeout=15.0) as client:
                resp = client.post(self.API_URL, headers=headers, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    choices = data.get("choices", [])
                    if choices:
                        return choices[0].get("message", {}).get("content", "")
                logger.error(f"Groq API returned status {resp.status_code}: {resp.text[:200]}")
                return f"[Groq error {resp.status_code}]: Fallback for: {prompt[:80]}"
        except Exception as e:
            logger.error(f"Groq generation error: {e}")
            return f"[Groq exception]: Fallback for: {prompt[:80]}"
