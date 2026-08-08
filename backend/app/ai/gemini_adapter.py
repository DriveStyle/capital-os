"""
Gemini Adapter implementation of AIProvider for Capital OS.
Wraps existing GeminiProvider to conform to the standardized AIProvider contract.
"""
from __future__ import annotations

from typing import Any, Optional
from .provider import AIProvider
from .gemini_provider import GeminiProvider


class GeminiAdapter(AIProvider):
    """
    AIProvider adapter implementation using Google Gemini models (e.g. gemini-2.5-flash).
    """

    def __init__(self, default_model: Optional[str] = None) -> None:
        self.default_model = default_model or GeminiProvider.DEFAULT_MODEL

    def generate(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ) -> str:
        model = kwargs.get("model") or self.default_model

        full_prompt = prompt
        if system_instruction:
            full_prompt = f"System: {system_instruction}\n\nUser: {prompt}"

        result = GeminiProvider.generate_wealth_analysis(
            prompt=full_prompt,
            model_name=model,
        )

        if result:
            return result

        return f"[Gemini fallback]: Strategy generated for: {prompt[:80]}"
