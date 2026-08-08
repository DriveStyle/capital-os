"""
OpenAI Adapter implementation of AIProvider for Capital OS.
Integrates OpenAI models (e.g. gpt-4o-mini, gpt-4o) using the official OpenAI SDK.
"""
from __future__ import annotations

import os
import logging
from typing import Any, Optional
from dotenv import load_dotenv

from .provider import AIProvider

load_dotenv()
logger = logging.getLogger("openai_adapter")


class OpenAIAdapter(AIProvider):
    """
    AIProvider adapter implementation for OpenAI and OpenAI-compatible endpoints.
    """

    DEFAULT_MODEL = "gpt-4o-mini"

    def __init__(
        self,
        default_model: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> None:
        self.default_model = default_model or self.DEFAULT_MODEL
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL")
        self._client = None

    def _get_client(self):
        if self._client is None and self.api_key:
            from openai import OpenAI
            self._client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url,
            )
        return self._client

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
            logger.warning("No OPENAI_API_KEY configured. Returning fallback response.")
            return f"[OpenAI fallback]: Strategy generated for: {prompt[:80]}"

        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        try:
            client = self._get_client()
            if not client:
                return f"[OpenAI client error]: Failed to initialize client for prompt: {prompt[:80]}"

            params: dict[str, Any] = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
            }
            if max_tokens:
                params["max_tokens"] = max_tokens

            response = client.chat.completions.create(**params)
            if response.choices and response.choices[0].message.content:
                return response.choices[0].message.content

            return f"[OpenAI empty response]: No choices returned for: {prompt[:80]}"
        except Exception as e:
            logger.error(f"OpenAI generation error: {e}")
            return f"[OpenAI error]: Fallback for: {prompt[:80]}"
