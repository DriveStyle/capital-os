from fastapi import APIRouter
from ..schemas.ai import (
    AdvisoryRequest,
    AdvisoryResponse,
    ConnectionUpdateRequest,
    ActiveProviderRequest,
    TestConnectionRequest,
    TestConnectionResponse,
)
from ..services.ai_service import AIService

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/recommend", response_model=AdvisoryResponse)
def get_wealth_recommendations(req: AdvisoryRequest):
    return AIService.generate_wealth_advice(req)


@router.get("/status")
def get_ai_status():
    return AIService.get_status()


@router.post("/connections")
def update_ai_connection(req: ConnectionUpdateRequest):
    return AIService.update_connection(req)


@router.post("/set-active-provider")
def set_active_ai_provider(req: ActiveProviderRequest):
    return AIService.set_active_provider(req.provider)


@router.post("/test-connection", response_model=TestConnectionResponse)
def test_ai_connection(req: TestConnectionRequest):
    return AIService.test_connection(req)


@router.get("/search")
def live_web_search(query: str = "best global ETF investments"):
    from ..ai.tavily_search import TavilySearchService
    return {"query": query, "results": TavilySearchService.search_investment_opportunities(query=query)}
