"""
Basic AI Router for Capital OS.
Resolves and instantiates registered AIProvider adapters from an AIProviderRegistry.
"""
from __future__ import annotations

from typing import Any
from .provider import AIProvider
from .registry import AIProviderRegistry


class AIRouter:
    """
    Router for instantiating AIProvider adapters on-demand by name.
    """

    def __init__(self, registry: AIProviderRegistry) -> None:
        self.registry = registry

    def get_provider(self, name: str, **kwargs: Any) -> AIProvider:
        """
        Lookup the registered provider class by name and instantiate it with kwargs.

        :param name: Identifier of the registered provider (e.g. 'gemini', 'openai').
        :param kwargs: Keyword arguments to pass to the provider constructor.
        :return: Instantiated AIProvider instance.
        :raises ValueError: If the provider name is not found in the registry.
        """
        provider_cls = self.registry.get(name)
        if provider_cls is None:
            available = ", ".join(self.registry.list_providers()) or "none"
            raise ValueError(
                f"AI provider '{name}' is not registered. Available providers: [{available}]"
            )
        return provider_cls(**kwargs)
