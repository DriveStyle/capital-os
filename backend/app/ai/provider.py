from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Optional


class AIProvider(ABC):
    """
    Abstract Base Class for all Capital OS AI providers.

    Standardized contract for Gemini, Groq, OpenAI, Claude, Grok,
    OpenRouter, OmniRouter, Ollama, and OpenAI-compatible providers.
    """

    @abstractmethod
    def generate(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ) -> str:
        """
        Generate a text or structured response for a given prompt.

        :param prompt: User prompt or query text.
        :param system_instruction: Optional system instruction or role context.
        :param temperature: Sampling temperature for deterministic/creative outputs.
        :param max_tokens: Maximum number of tokens to generate.
        :param kwargs: Additional provider-specific parameters.
        :return: Generated response string.
        """
        raise NotImplementedError
