"""
Claude Adapter implementation of AIProvider for Capital OS.
Integrates Anthropic Claude models (e.g. claude-3-5-sonnet) using the official Anthropic SDK.
"""
from __future__ import annotations

import os
import logging
from typing import Any, Optional
from dotenv import load_dotenv

from .provider import AIProvider

load_dotenv()
logger = logging.getLogger("claude_adapter")


class ClaudeAdapter(AIProvider):
    """
    AIProvider adapter implementation for Anthropic Claude models.
    """

    DEFAULT_MODEL = "claude-3-5-sonnet"

    def __init__(
        self,
        default_model: Optional[str] = None,
        api_key: Optional[str] = None,
    ) -> None:
        self.default_model = default_model or self.DEFAULT_MODEL
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY", "")
        self._client = None

    def _get_client(self):
        if self._client is None and self.api_key:
            from anthropic import Anthropic
            self._client = Anthropic(api_key=self.api_key)
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
            logger.warning("No ANTHROPIC_API_KEY configured. Returning fallback response.")
            return f"[Claude fallback]: Strategy generated for: {prompt[:80]}"

        try:
            client = self._get_client()
            if not client:
                return f"[Claude client error]: Failed to initialize client for prompt: {prompt[:80]}"

            params: dict[str, Any] = {
                "model": model,
                "max_tokens": max_tokens or 1024,
                "temperature": temperature,
                "messages": [{"role": "user", "content": prompt}],
            }
            if system_instruction:
                params["system"] = system_instruction

            response = client.messages.create(**params)
            if response.content:
                text_blocks = [
                    block.text for block in response.content if getattr(block, "type", None) == "text"
                ]
                if text_blocks:
                    return "".join(text_blocks)

            return f"[Claude empty response]: No content returned for: {prompt[:80]}"
        except Exception as e:
            logger.error(f"Claude generation error: {e}")
            return f"[Claude error]: Fallback for: {prompt[:80]}"
