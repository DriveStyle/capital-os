"""
Universal OpenAI-Compatible Adapter implementation of AIProvider for Capital OS.
Supports any OpenAI Chat Completions-compatible API (e.g. OmniRouter, OpenRouter, Ollama, vLLM, LocalAI).
"""
from __future__ import annotations

import os
import logging
from typing import Any, Optional
from dotenv import load_dotenv

from .provider import AIProvider

load_dotenv()
logger = logging.getLogger("openai_compatible_adapter")


class OpenAICompatibleAdapter(AIProvider):
    """
    Universal AIProvider adapter for OpenAI-compatible endpoints.
    """

    DEFAULT_MODEL = "gpt-4o-mini"

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        default_model: Optional[str] = None,
    ) -> None:
        self.api_key = api_key or os.getenv("OPENAI_COMPATIBLE_API_KEY", "")
        self.base_url = base_url or os.getenv("OPENAI_COMPATIBLE_BASE_URL", "")
        self.default_model = default_model or self.DEFAULT_MODEL
        self._client = None

    def _get_client(self):
        if self._client is None and (self.api_key or self.base_url):
            from openai import OpenAI
            kwargs: dict[str, Any] = {}
            if self.api_key:
                kwargs["api_key"] = self.api_key
            else:
                kwargs["api_key"] = "dummy-key-for-local-endpoint"
            if self.base_url:
                kwargs["base_url"] = self.base_url

            self._client = OpenAI(**kwargs)
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

        if not self.api_key and not self.base_url:
            logger.warning("No OPENAI_COMPATIBLE_API_KEY or OPENAI_COMPATIBLE_BASE_URL configured.")
            return f"[OpenAI-Compatible fallback]: Strategy generated for: {prompt[:80]}"

        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        try:
            client = self._get_client()
            if not client:
                return f"[OpenAI-Compatible client error]: Failed to initialize client for prompt: {prompt[:80]}"

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

            return f"[OpenAI-Compatible empty response]: No choices returned for: {prompt[:80]}"
        except Exception as e:
            logger.error(f"OpenAI-Compatible generation error: {e}")
            return f"[OpenAI-Compatible error]: Fallback for: {prompt[:80]}"
