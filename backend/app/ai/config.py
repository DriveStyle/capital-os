"""
AI Connection Configuration Model for Capital OS.
Encapsulates individual AI provider connection settings with security-first credential masking.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class AIConnectionConfig:
    """
    Configuration for an individual AI provider connection.
    Guarantees API keys are never exposed via string representation or safe serialization.
    """

    provider: str
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    default_model: Optional[str] = None
    enabled: bool = True
    display_name: Optional[str] = None

    def masked_api_key(self) -> str:
        """
        Return a safely masked representation of the API key.
        Never reveals the full secret.
        """
        if not self.api_key:
            return ""

        key_len = len(self.api_key)
        if key_len <= 8:
            return "*" * 8

        prefix_len = 4
        suffix_len = 3
        if key_len <= (prefix_len + suffix_len):
            return "*" * key_len

        masked_middle = "*" * (key_len - prefix_len - suffix_len)
        return f"{self.api_key[:prefix_len]}{masked_middle}{self.api_key[-suffix_len:]}"

    def is_configured(self) -> bool:
        """
        Check if the connection has minimum required parameters configured.
        Supports local / self-hosted / Ollama providers without requiring API key.
        """
        if not self.provider or not self.provider.strip():
            return False

        prov_clean = self.provider.strip().lower()
        if prov_clean in ("ollama", "local", "self_hosted") or self.base_url:
            return True

        return bool(self.api_key and self.api_key.strip())

    def to_safe_dict(self) -> Dict[str, Any]:
        """
        Export configuration as a dictionary with masked credentials.
        Safe for logging, debugging, and client-facing status responses.
        """
        return {
            "provider": self.provider,
            "api_key": self.masked_api_key(),
            "base_url": self.base_url,
            "default_model": self.default_model,
            "enabled": self.enabled,
            "display_name": self.display_name or self.provider.capitalize(),
        }

    def __repr__(self) -> str:
        """Safe representation preventing accidental credential exposure in logs."""
        return (
            f"AIConnectionConfig(provider='{self.provider}', "
            f"api_key='{self.masked_api_key()}', base_url={self.base_url!r}, "
            f"default_model={self.default_model!r}, enabled={self.enabled}, "
            f"display_name={self.display_name!r})"
        )
