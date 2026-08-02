from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.db.base import Base
from backend.app.db.database import get_engine

client = TestClient(app)

# Create tables in test db
Base.metadata.create_all(bind=get_engine())


def test_root_endpoint() -> None:
    response = client.get("/api/")
    assert response.status_code == 200
    assert response.json()["project"] == "Capital OS"


def test_health_endpoint() -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_full_wealth_workflow() -> None:
    # 1. Create User
    user_res = client.post(
        "/api/users/",
        json={"email": "investor@capital-os.ai", "full_name": "Pro Investor"},
    )
    assert user_res.status_code == 201
    user_data = user_res.json()
    user_id = user_data["id"]

    # 2. Create Portfolio
    port_res = client.post(
        "/api/portfolios/",
        json={
            "name": "Main Growth Portfolio",
            "description": "Long-term ETF & Stock wealth engine",
            "owner_id": user_id,
        },
    )
    assert port_res.status_code == 201
    port_data = port_res.json()
    portfolio_id = port_data["id"]

    # 3. Add Asset to Portfolio
    asset_res = client.post(
        "/api/portfolios/assets",
        json={
            "symbol": "VWRA",
            "asset_type": "etf",
            "quantity": 100,
            "cost_basis": 110.0,
            "current_value": 12500.0,
            "notes": "Vanguard FTSE All-World",
            "portfolio_id": portfolio_id,
        },
    )
    assert asset_res.status_code == 201

    # 4. Check updated portfolio total value
    port_updated = client.get(f"/api/portfolios/{portfolio_id}")
    assert port_updated.status_code == 200
    assert float(port_updated.json()["total_value"]) == 12500.0

    # 5. Create Goal
    goal_res = client.post(
        "/api/goals/",
        json={
            "title": "Financial Freedom 2030",
            "target_amount": 500000.0,
            "user_id": user_id,
        },
    )
    assert goal_res.status_code == 201

    # 6. Request AI Wealth Advice
    ai_res = client.post(
        "/api/ai/recommend",
        json={
            "user_id": user_id,
            "portfolio_id": portfolio_id,
            "monthly_investment_budget": 1000.0,
            "risk_tolerance": "moderate",
            "country_code": "UA",
        },
    )
    assert ai_res.status_code == 200
    ai_data = ai_res.json()
    assert "summary" in ai_data
    assert len(ai_data["recommended_actions"]) > 0
