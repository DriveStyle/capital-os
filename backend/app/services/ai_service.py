from typing import Dict, Any
from ..schemas.ai import AdvisoryRequest, AdvisoryResponse, RecommendationItem
from ..config import get_settings


class AIService:
    @staticmethod
    def generate_wealth_advice(req: AdvisoryRequest) -> AdvisoryResponse:
        settings = get_settings()
        provider = settings.ai_provider

        # Rule-based / Model-driven financial analysis engine
        budget = req.monthly_investment_budget or 500.0
        risk = (req.risk_tolerance or "moderate").lower()
        country = (req.country_code or "UA").upper()

        if risk == "conservative":
            rec_1 = RecommendationItem(
                category="Cash Reserves & Fixed Income",
                action="Allocate 40% of budget to short-term government bonds or high-yield savings.",
                rationale="Protect liquidity and preserve capital against inflation.",
                priority="High",
            )
            rec_2 = RecommendationItem(
                category="Diversified Index Funds",
                action="Allocate 60% to global broad market index ETFs (e.g. VWRA / S&P 500).",
                rationale="Disciplined long-term compounding with low volatility.",
                priority="High",
            )
            summary = f"Conservative wealth strategy tailored for country {country} focused on capital preservation and steady dividend/coupon returns."
        elif risk == "aggressive":
            rec_1 = RecommendationItem(
                category="Growth Stocks & Tech ETFs",
                action="Allocate 70% to broad equity growth ETFs (e.g. QQQ / MSCI World Growth).",
                rationale="Maximize capital gain potential across long-term horizons.",
                priority="High",
            )
            rec_2 = RecommendationItem(
                category="Alternative & Crypto Assets",
                action="Allocate 30% to digital assets (BTC/ETH) and speculative growth.",
                rationale="High upside potential for aggressive wealth accumulation.",
                priority="Medium",
            )
            summary = f"Aggressive capital growth roadmap tailored for {country} targeting high-yield growth assets."
        else:  # moderate
            rec_1 = RecommendationItem(
                category="Broad Market Indexing",
                action="Allocate 80% ($" + str(int(budget * 0.8)) + "/mo) into low-cost global ETFs.",
                rationale="Core wealth foundation providing broad diversification.",
                priority="High",
            )
            rec_2 = RecommendationItem(
                category="Opportunistic / Reserve Allocation",
                action="Keep 20% ($" + str(int(budget * 0.2)) + "/mo) in reserve cash yield.",
                rationale="Liquidity safety buffer for market dips and emergency fund.",
                priority="Medium",
            )
            summary = f"Balanced wealth operating strategy for {country} maintaining strong capital safety and steady indexing."

        country_notes = f"Country module [{country}]: Ensure tax reporting compliance on foreign dividend income and utilize local tax-exempt investment accounts where applicable."

        return AdvisoryResponse(
            summary=summary,
            risk_assessment=f"Risk profile evaluated as [{risk.upper()}]. Recommended investment horizon: 5+ years.",
            recommended_actions=[rec_1, rec_2],
            country_notes=country_notes,
            provider_used=provider,
        )
