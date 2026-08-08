"""
Unit tests for AIServiceFactory in Capital OS.
"""
from backend.app.ai.factory import AIServiceFactory
from backend.app.ai.openai_adapter import OpenAIAdapter
from backend.app.ai.gemini_adapter import GeminiAdapter
from backend.app.ai.groq_adapter import GroqAdapter
from backend.app.ai.claude_adapter import ClaudeAdapter
from backend.app.ai.openai_compatible_adapter import OpenAICompatibleAdapter


def test_factory_import_and_empty_env():
    """Verify that factory creates manager from empty environment without crashing."""
    manager = AIServiceFactory.create_manager_from_env(env={})
    assert manager.list_connections() == []
    status = AIServiceFactory.get_safe_status(manager)
    assert status["total_connections"] == 0
    assert status["configured_providers"] == []
    assert status["connections"] == {}


def test_factory_with_all_test_env_vars():
    """Verify that all 6 providers are properly configured from environment variables."""
    fake_env = {
        "OPENAI_API_KEY": "sk-test-secret-key-1234567890",
        "OPENAI_MODEL": "gpt-4o-mini",
        "GEMINI_API_KEY": "AIza-test-secret-key-12345678",
        "GEMINI_MODEL": "gemini-2.5-flash",
        "GROQ_API_KEY": "gsk-test-secret-key-1234567890",
        "GROQ_MODEL": "llama-3.3-70b-versatile",
        "ANTHROPIC_API_KEY": "sk-ant-test-secret-key-123456",
        "ANTHROPIC_MODEL": "claude-3-5-sonnet",
        "OMNIROUTER_API_KEY": "omni-test-secret-key-123456",
        "OMNIROUTER_BASE_URL": "https://api.omnirouter.ai/v1",
        "OMNIROUTER_MODEL": "omni-smart-v1",
        "OLLAMA_BASE_URL": "http://localhost:11434/v1",
        "OLLAMA_MODEL": "llama3:latest",
    }

    manager = AIServiceFactory.create_manager_from_env(env=fake_env)
    assert len(manager.list_connections()) == 6

    # 1. OpenAI
    assert manager.has_connection("openai")
    p_openai = manager.get_provider("openai")
    assert isinstance(p_openai, OpenAIAdapter)

    # 2. Gemini
    assert manager.has_connection("gemini")
    p_gemini = manager.get_provider("gemini")
    assert isinstance(p_gemini, GeminiAdapter)

    # 3. Groq
    assert manager.has_connection("groq")
    p_groq = manager.get_provider("groq")
    assert isinstance(p_groq, GroqAdapter)

    # 4. Claude
    assert manager.has_connection("claude")
    p_claude = manager.get_provider("claude")
    assert isinstance(p_claude, ClaudeAdapter)

    # 5. OmniRouter (must use openai_compatible)
    assert manager.has_connection("omnirouter")
    omni_cfg = manager.get_connection("omnirouter")
    assert omni_cfg.provider == "openai_compatible"
    p_omni = manager.get_provider("omnirouter")
    assert isinstance(p_omni, OpenAICompatibleAdapter)

    # 6. Ollama (must not require api_key)
    assert manager.has_connection("ollama")
    ollama_cfg = manager.get_connection("ollama")
    assert ollama_cfg.api_key is None
    assert ollama_cfg.base_url == "http://localhost:11434/v1"
    p_ollama = manager.get_provider("ollama")
    assert isinstance(p_ollama, OpenAICompatibleAdapter)


def test_factory_safe_status_secrets_masking():
    """Verify that credentials are never exposed in safe status output."""
    fake_env = {
        "OPENAI_API_KEY": "sk-secret-key-never-leak-me-12345",
        "ANTHROPIC_API_KEY": "sk-ant-top-secret-token-abcdef",
        "OMNIROUTER_API_KEY": "omni-super-secret-key-99999",
    }

    manager = AIServiceFactory.create_manager_from_env(env=fake_env)
    status = AIServiceFactory.get_safe_status(manager)
    status_str = str(status)

    for secret in fake_env.values():
        assert secret not in status_str

    for conn_data in status["connections"].values():
        assert "api_key" in conn_data
        assert "*" in conn_data["api_key"]
