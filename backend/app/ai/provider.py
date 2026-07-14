from abc import ABC, abstractmethod
from typing import Any


class AIProvider(ABC):
    """Abstract interface for AI providers.""

    @abstractmethod
    def generate(self, prompt: str, **kwargs: Any) -> str:
        raise NotImplementedError


class OpenAIProvider(AIProvider):
    def generate(self, prompt: str, **kwargs: Any) -> str:
        return f"OpenAI response for: {prompt}"


class AnthropicProvider(AIProvider):
    def generate(self, prompt: str, **kwargs: Any) -> str:
        return f"Anthropic response for: {prompt}"


class GeminiProvider(AIProvider):
    def generate(self, prompt: str, **kwargs: Any) -> str:
        return f"Gemini response for: {prompt}"


class GrokProvider(AIProvider):
    def generate(self, prompt: str, **kwargs: Any) -> str:
        return f"Grok response for: {prompt}"


def get_provider(name: str) -> AIProvider:
    providers = {
        "openai": OpenAIProvider(),
        "anthropic": AnthropicProvider(),
        "gemini": GeminiProvider(),
        "grok": GrokProvider(),
    }
    return providers.get(name.lower(), OpenAIProvider())
