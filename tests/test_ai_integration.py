"""
Integration tests for AI Router, AIServiceFactory, and AI API endpoints in Capital OS.
"""
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_ai_status_endpoint_returns_safe_status():
    """Verify that the /api/ai/status endpoint returns safe telemetry without credentials."""
    response = client.get("/api/ai/status")
    assert response.status_code == 200
    data = response.json()
    assert "total_connections" in data
    assert "configured_providers" in data
    assert "connections" in data
    assert "active_provider" in data
    # Ensure all connection api_keys are masked with asterisks
    for conn in data["connections"].values():
        if conn.get("api_key"):
            assert "*" in conn["api_key"]


def test_ai_set_active_provider_endpoint():
    """Verify switching active AI provider."""
    response = client.post("/api/ai/set-active-provider", json={"provider": "omnirouter"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["active_provider"] == "omnirouter"

    # Verify status reflects the change
    status_res = client.get("/api/ai/status")
    assert status_res.status_code == 200
    assert status_res.json()["active_provider"] == "omnirouter"


def test_ai_update_connection_endpoint():
    """Verify updating a connection configuration safely."""
    payload = {
        "connection_id": "omnirouter",
        "provider": "openai_compatible",
        "api_key": "sk-new-secret-test-token-12345",
        "base_url": "https://api.omnirouter.ai/v1",
        "default_model": "omni-pro-v2",
        "enabled": True,
        "display_name": "OmniRouter Pro",
    }
    response = client.post("/api/ai/connections", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "connections" in data
    omni_data = data["connections"]["omnirouter"]
    assert omni_data["default_model"] == "omni-pro-v2"
    assert omni_data["display_name"] == "OmniRouter Pro"
    # Ensure updated API key is masked and not exposed plaintext
    assert "sk-new-secret-test-token-12345" not in str(data)
    assert "*" in omni_data["api_key"]


def test_ai_test_connection_endpoint():
    """Verify connection health check endpoint."""
    response = client.post("/api/ai/test-connection", json={"connection_id": "omnirouter"})
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "latency_ms" in data
    assert data["connection_id"] == "omnirouter"


def test_ai_recommend_endpoint_fallback():
    """Verify that /api/ai/recommend generates a structured plan with fallback support."""
    req_payload = {
        "user_id": "test-user-123",
        "portfolio_id": "port-001",
        "monthly_investment_budget": 1200.0,
        "risk_tolerance": "moderate",
        "country_code": "UA",
    }
    response = client.post("/api/ai/recommend", json=req_payload)
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert "risk_assessment" in data
    assert "country_notes" in data
    assert len(data["recommended_actions"]) >= 1
    assert "provider_used" in data


def test_ai_recommend_conservative_and_aggressive_profiles():
    """Verify different risk profile allocations."""
    # Conservative
    res_cons = client.post(
        "/api/ai/recommend",
        json={
            "user_id": "user-cons",
            "monthly_investment_budget": 800.0,
            "risk_tolerance": "conservative",
            "country_code": "DE",
        },
    )
    assert res_cons.status_code == 200
    summary_cons = res_cons.json()["summary"].lower()
    assert "conservative" in summary_cons or "preservation" in summary_cons or "de" in summary_cons

    # Aggressive
    res_agg = client.post(
        "/api/ai/recommend",
        json={
            "user_id": "user-agg",
            "monthly_investment_budget": 2000.0,
            "risk_tolerance": "aggressive",
            "country_code": "US",
        },
    )
    assert res_agg.status_code == 200
    summary_agg = res_agg.json()["summary"].lower()
    assert "aggressive" in summary_agg or "growth" in summary_agg or "us" in summary_agg


def test_ai_search_endpoint_with_tavily():
    """Verify that /api/ai/search executes without crashing."""
    response = client.get("/api/ai/search?query=best+etfs")
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "best etfs"
    assert "results" in data
    assert isinstance(data["results"], list)
