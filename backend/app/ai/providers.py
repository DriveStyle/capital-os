"""
Built-in AI Providers registration for Capital OS.
Registers default AIProvider adapter classes into an AIProviderRegistry.
"""
from __future__ import annotations

from .registry import AIProviderRegistry
from .gemini_adapter import GeminiAdapter
from .groq_adapter import GroqAdapter
from .openai_adapter import OpenAIAdapter
from .claude_adapter import ClaudeAdapter
from .openai_compatible_adapter import OpenAICompatibleAdapter


def register_builtin_providers(registry: AIProviderRegistry) -> AIProviderRegistry:
    """
    Register all built-in AI adapter classes into the provided AIProviderRegistry.
    Classes are registered without eager instantiation.
    """
    registry.register("gemini", GeminiAdapter)
    registry.register("groq", GroqAdapter)
    registry.register("openai", OpenAIAdapter)
    registry.register("claude", ClaudeAdapter)
    registry.register("openai_compatible", OpenAICompatibleAdapter)
    return registry
