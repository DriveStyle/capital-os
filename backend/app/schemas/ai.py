from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class AdvisoryRequest(BaseModel):
    user_id: str
    portfolio_id: Optional[str] = None
    query: Optional[str] = "Provide a comprehensive portfolio health check and allocation strategy."
    monthly_investment_budget: Optional[float] = 500.00
    risk_tolerance: Optional[str] = "moderate"  # conservative, moderate, aggressive
    country_code: Optional[str] = "UA"  # UA, US, DE, etc.


class RecommendationItem(BaseModel):
    category: str
    action: str
    rationale: str
    priority: str  # High, Medium, Low


class AdvisoryResponse(BaseModel):
    summary: str
    risk_assessment: str
    recommended_actions: List[RecommendationItem]
    country_notes: str
    provider_used: str


class ConnectionUpdateRequest(BaseModel):
    connection_id: str
    provider: str
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    default_model: Optional[str] = None
    enabled: bool = True
    display_name: Optional[str] = None


class ActiveProviderRequest(BaseModel):
    provider: str


class TestConnectionRequest(BaseModel):
    connection_id: Optional[str] = None
    prompt: Optional[str] = "Respond with status OK."


class TestConnectionResponse(BaseModel):
    status: str
    connection_id: str
    provider: str
    model_used: Optional[str] = None
    latency_ms: float
    message: str
    response_sample: Optional[str] = None
