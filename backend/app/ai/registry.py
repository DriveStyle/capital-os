"""
AI Provider Registry for Capital OS.
Maintains a registry of AIProvider classes and factories without eager instantiation.
"""
from __future__ import annotations

from typing import Dict, Type, Optional, List
from .provider import AIProvider


class AIProviderRegistry:
    """
    Registry for managing AIProvider classes by name.
    """

    def __init__(self) -> None:
        self._providers: Dict[str, Type[AIProvider]] = {}

    def register(self, name: str, provider_cls: Type[AIProvider]) -> None:
        """
        Register an AIProvider class by its string identifier.
        """
        if not issubclass(provider_cls, AIProvider):
            raise TypeError(f"Class {provider_cls} must be a subclass of AIProvider")
        self._providers[name.lower().strip()] = provider_cls

    def unregister(self, name: str) -> None:
        """
        Remove a registered provider class by name.
        """
        self._providers.pop(name.lower().strip(), None)

    def get(self, name: str) -> Optional[Type[AIProvider]]:
        """
        Get the registered AIProvider class by name.
        """
        return self._providers.get(name.lower().strip())

    def has(self, name: str) -> bool:
        """
        Check if an AIProvider class is registered under the given name.
        """
        return name.lower().strip() in self._providers

    def list_providers(self) -> List[str]:
        """
        List all currently registered provider names.
        """
        return list(self._providers.keys())

    def __contains__(self, name: str) -> bool:
        return self.has(name)
