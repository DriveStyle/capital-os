from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.country.engine import CountryEngine
from backend.app.recommendations.rebalancer import PortfolioRebalancer

client = TestClient(app)


def test_country_engine():
    ua_info = CountryEngine.get_country_info("UA")
    assert ua_info["currency"] == "UAH"
    assert ua_info["dividend_tax_rate"] == 0.09

    us_info = CountryEngine.get_country_info("US")
    assert us_info["currency"] == "USD"
    assert "Vanguard" in us_info["recommended_brokers"]

    supported = CountryEngine.get_supported_countries()
    assert "UA" in supported and "US" in supported and "DE" in supported and "UK" in supported


def test_rebalancer_algorithm():
    current_assets = [
        {"symbol": "VWRA", "value": 20000, "type": "ETF"},
        {"symbol": "BTC", "value": 10000, "type": "Crypto"}
    ]
    res = PortfolioRebalancer.calculate_rebalance(
        current_assets=current_assets,
        monthly_budget=1000,
        risk_profile="moderate"
    )
    assert res["monthly_budget"] == 1000
    assert len(res["buy_allocations"]) > 0
    assert "tax_efficient_note" in res


def test_rebalance_api_endpoint():
    response = client.post("/api/portfolios/rebalance", json={
        "monthly_budget": 1000,
        "risk_profile": "moderate"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["monthly_budget"] == 1000
    assert "buy_allocations" in data


def test_voice_assistant_api():
    response = client.post("/api/voice/process", json={
        "transcript": "How should I rebalance my portfolio this month?"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "rebalance_recommendation"
    assert "VWRA" in data["ai_response"] or "allocation" in data["ai_response"]


def test_transactions_api():
    response = client.get("/api/transactions/portfolio/00000000-0000-0000-0000-000000000001")
    assert response.status_code == 200
    txs = response.json()
    assert isinstance(txs, list)
