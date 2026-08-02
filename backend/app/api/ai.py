from fastapi import APIRouter
from ..schemas.ai import AdvisoryRequest, AdvisoryResponse
from ..services.ai_service import AIService

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/recommend", response_model=AdvisoryResponse)
def get_wealth_recommendations(req: AdvisoryRequest):
    return AIService.generate_wealth_advice(req)
