from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from backend.app.services.ai_service import AIService

router = APIRouter(prefix="/voice", tags=["Voice Assistant"])


class VoiceQueryRequest(BaseModel):
    user_id: Optional[str] = "demo-user"
    transcript: str
    language: Optional[str] = "en"


class VoiceQueryResponse(BaseModel):
    transcript_received: str
    intent: str
    ai_response: str
    suggested_action: Optional[str] = None


@router.post("/process", response_model=VoiceQueryResponse)
def process_voice_input(req: VoiceQueryRequest):
    text = req.transcript.lower()

    if "rebalance" in text or "invest" in text or "buy" in text:
        intent = "rebalance_recommendation"
        response_text = "Based on your monthly budget of $1,000, your tax-efficient allocation is: $700 into VWRA global ETF, and $300 into High-Yield Reserve."
        suggested = "execute_rebalance"
    elif "portfolio" in text or "balance" in text or "worth" in text:
        intent = "portfolio_summary"
        response_text = "Your portfolio total value is currently $50,000. Net growth is +14.2% all-time. You are on track for your 2030 goal."
        suggested = "view_portfolio"
    elif "tax" in text or "country" in text or "ukraine" in text or "us" in text:
        intent = "tax_info"
        response_text = "Under your active country module, foreign dividend income is processed with tax optimization guidelines and local exemptions."
        suggested = "view_tax_rules"
    else:
        intent = "general_ai_advisory"
        response_text = AIService.get_recommendation(
            monthly_budget=1000.0,
            risk_tolerance="moderate",
            country_code="US"
        ).get("summary", "Keep maintaining disciplined monthly investing habits for compound growth.")
        suggested = "consult_ai_coach"

    return VoiceQueryResponse(
        transcript_received=req.transcript,
        intent=intent,
        ai_response=response_text,
        suggested_action=suggested
    )
