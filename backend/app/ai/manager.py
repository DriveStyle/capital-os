"""
AI Connection Manager for Capital OS.
Stores and manages multiple AIConnectionConfig instances and resolves provider adapters via AIRouter.
"""
from __future__ import annotations

from typing import Dict, List, Optional, Any
from .config import AIConnectionConfig
from .provider import AIProvider
from .router import AIRouter


class AIConnectionManager:
    """
    Manages active AI connections and instantiates AIProvider adapters through AIRouter.
    """

    def __init__(self, router: AIRouter) -> None:
        self.router = router
        self._connections: Dict[str, AIConnectionConfig] = {}

    def add_connection(self, connection_id: str, config: AIConnectionConfig) -> None:
        """
        Add or replace a named AI connection configuration.
        """
        self._connections[connection_id.strip()] = config

    def get_connection(self, connection_id: str) -> Optional[AIConnectionConfig]:
        """
        Retrieve connection configuration by its identifier.
        """
        return self._connections.get(connection_id.strip())

    def remove_connection(self, connection_id: str) -> bool:
        """
        Remove a connection configuration by ID. Returns True if removed, False otherwise.
        """
        key = connection_id.strip()
        if key in self._connections:
            del self._connections[key]
            return True
        return False

    def list_connections(self) -> List[str]:
        """
        List all active connection IDs.
        """
        return list(self._connections.keys())

    def has_connection(self, connection_id: str) -> bool:
        """
        Check if a connection ID exists.
        """
        return connection_id.strip() in self._connections

    def get_provider(self, connection_id: str) -> AIProvider:
        """
        Resolve and instantiate the AIProvider adapter for a given connection_id.

        :param connection_id: Identifier of the configured connection.
        :return: Instantiated AIProvider.
        :raises ValueError: If connection_id is not found in manager.
        """
        config = self.get_connection(connection_id)
        if config is None:
            available = ", ".join(self.list_connections()) or "none"
            raise ValueError(
                f"Connection '{connection_id}' not found. Available connections: [{available}]"
            )

        provider_cls = self.router.registry.get(config.provider)
        if provider_cls is None:
            # Let router handle unknown provider ValueError
            return self.router.get_provider(config.provider)

        import inspect

        sig = inspect.signature(provider_cls.__init__)
        has_varkw = any(p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values())

        kwargs: Dict[str, Any] = {}
        if config.default_model and (has_varkw or "default_model" in sig.parameters):
            kwargs["default_model"] = config.default_model
        if config.api_key and (has_varkw or "api_key" in sig.parameters):
            kwargs["api_key"] = config.api_key
        if config.base_url and (has_varkw or "base_url" in sig.parameters):
            kwargs["base_url"] = config.base_url

        return self.router.get_provider(config.provider, **kwargs)

    def to_safe_dict(self) -> Dict[str, Dict[str, Any]]:
        """
        Export all connection configs as a safe dictionary with masked credentials.
        """
        return {
            cid: cfg.to_safe_dict()
            for cid, cfg in self._connections.items()
        }

    def __contains__(self, connection_id: str) -> bool:
        return self.has_connection(connection_id)
