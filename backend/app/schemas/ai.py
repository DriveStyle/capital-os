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
