"""
AI Service Factory for Capital OS.
Initializes AIProviderRegistry, AIRouter, and AIConnectionManager from environment variables.
"""
from __future__ import annotations

import os
from typing import Any, Dict, Optional
from dotenv import load_dotenv

from .config import AIConnectionConfig
from .manager import AIConnectionManager
from .providers import register_builtin_providers
from .registry import AIProviderRegistry
from .router import AIRouter

load_dotenv()


class AIServiceFactory:
    """
    Factory for creating and configuring AI registry, router, and connection manager.
    """

    @classmethod
    def create_manager_from_env(
        cls, env: Optional[Dict[str, str]] = None
    ) -> AIConnectionManager:
        """
        Build and populate an AIConnectionManager from environment variables or a supplied dict.
        """
        registry = AIProviderRegistry()
        register_builtin_providers(registry)
        router = AIRouter(registry)
        manager = AIConnectionManager(router)

        env_source = env if env is not None else os.environ

        # 1. OpenAI
        openai_key = env_source.get("OPENAI_API_KEY")
        openai_model = env_source.get("OPENAI_MODEL") or "gpt-4o-mini"
        openai_base_url = env_source.get("OPENAI_BASE_URL")
        if openai_key:
            manager.add_connection(
                "openai",
                AIConnectionConfig(
                    provider="openai",
                    api_key=openai_key,
                    base_url=openai_base_url,
                    default_model=openai_model,
                    display_name="OpenAI",
                ),
            )

        # 2. Gemini
        gemini_key = env_source.get("GEMINI_API_KEY")
        gemini_model = env_source.get("GEMINI_MODEL") or "gemini-2.5-flash"
        if gemini_key:
            manager.add_connection(
                "gemini",
                AIConnectionConfig(
                    provider="gemini",
                    api_key=gemini_key,
                    default_model=gemini_model,
                    display_name="Google Gemini",
                ),
            )

        # 3. Groq
        groq_key = env_source.get("GROQ_API_KEY")
        groq_model = env_source.get("GROQ_MODEL") or "llama-3.3-70b-versatile"
        if groq_key:
            manager.add_connection(
                "groq",
                AIConnectionConfig(
                    provider="groq",
                    api_key=groq_key,
                    default_model=groq_model,
                    display_name="Groq",
                ),
            )

        # 4. Claude (Anthropic)
        claude_key = env_source.get("ANTHROPIC_API_KEY")
        claude_model = env_source.get("ANTHROPIC_MODEL") or "claude-3-5-sonnet"
        if claude_key:
            manager.add_connection(
                "claude",
                AIConnectionConfig(
                    provider="claude",
                    api_key=claude_key,
                    default_model=claude_model,
                    display_name="Anthropic Claude",
                ),
            )

        # 5. OmniRouter (uses OpenAICompatibleAdapter)
        omni_key = env_source.get("OMNIROUTER_API_KEY")
        omni_base_url = env_source.get("OMNIROUTER_BASE_URL")
        omni_model = env_source.get("OMNIROUTER_MODEL") or "gpt-4o-mini"
        if omni_key or omni_base_url:
            manager.add_connection(
                "omnirouter",
                AIConnectionConfig(
                    provider="openai_compatible",
                    api_key=omni_key,
                    base_url=omni_base_url,
                    default_model=omni_model,
                    display_name="OmniRouter",
                ),
            )

        # 6. Ollama (uses OpenAICompatibleAdapter without requiring API key)
        ollama_base_url = env_source.get("OLLAMA_BASE_URL")
        ollama_model = env_source.get("OLLAMA_MODEL") or "llama3"
        if ollama_base_url:
            manager.add_connection(
                "ollama",
                AIConnectionConfig(
                    provider="openai_compatible",
                    api_key=None,
                    base_url=ollama_base_url,
                    default_model=ollama_model,
                    display_name="Ollama (Local)",
                ),
            )

        return manager

    @classmethod
    def get_safe_status(cls, manager: AIConnectionManager) -> Dict[str, Any]:
        """
        Returns safe telemetry and status of all configured connections without leaking credentials.
        """
        return {
            "total_connections": len(manager.list_connections()),
            "configured_providers": manager.list_connections(),
            "connections": manager.to_safe_dict(),
        }
