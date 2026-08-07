from fastapi import APIRouter
from ..schemas.ai import AdvisoryRequest, AdvisoryResponse
from ..services.ai_service import AIService

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/recommend", response_model=AdvisoryResponse)
def get_wealth_recommendations(req: AdvisoryRequest):
    return AIService.generate_wealth_advice(req)


@router.get("/search")
def live_web_search(query: str = "best global ETF investments"):
    from backend.app.ai.tavily_search import TavilySearchService
    return {"query": query, "results": TavilySearchService.search_investment_opportunities(query=query)}

