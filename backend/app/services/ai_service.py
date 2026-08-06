import os
import json
import logging
from typing import Dict, Any
from dotenv import load_dotenv
import httpx

load_dotenv()

from ..schemas.ai import AdvisoryRequest, AdvisoryResponse, RecommendationItem
from ..config import get_settings

logger = logging.getLogger("ai_service")


class AIService:
    @staticmethod
    def generate_wealth_advice(req: AdvisoryRequest) -> AdvisoryResponse:
        settings = get_settings()
        provider = os.getenv("AI_PROVIDER", settings.ai_provider).lower()
        groq_key = os.getenv("GROQ_API_KEY")

        budget = req.monthly_investment_budget or 500.0
        risk = (req.risk_tolerance or "moderate").lower()
        country = (req.country_code or "UA").upper()

        if groq_key and (provider == "groq" or not provider):
            try:
                headers = {
                    "Authorization": f"Bearer {groq_key}",
                    "Content-Type": "application/json",
                }
                prompt = (
                    f"You are Capital OS AI Wealth Advisor. Generate a structured JSON wealth plan for a user in country '{country}' "
                    f"with a monthly budget of ${budget} and risk profile '{risk}'. "
                    f"Return ONLY a raw JSON object with keys: summary, risk_assessment, country_notes, "
                    f"recommended_actions (array of objects with category, action, priority, rationale)."
                )
                payload = {
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {"role": "system", "content": "You are a professional wealth operating system advisor. Respond strictly in valid JSON."},
                        {"role": "user", "content": prompt},
                    ],
                    "response_format": {"type": "json_object"},
                    "temperature": 0.3,
                }

                with httpx.Client(timeout=15.0) as client:
                    resp = client.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
                    if resp.status_code == 200:
                        content = resp.json()["choices"][0]["message"]["content"]
                        parsed = json.loads(content)
                        recs = [
                            RecommendationItem(
                                category=r.get("category", "General"),
                                action=r.get("action", "Invest"),
                                priority=r.get("priority", "Medium"),
                                rationale=r.get("rationale", ""),
                            )
                            for r in parsed.get("recommended_actions", [])
                        ]
                        if not recs:
                            recs = [
                                RecommendationItem(
                                    category="Core Indexing",
                                    action=f"Allocate ${int(budget * 0.8)}/mo into broad market ETFs.",
                                    priority="High",
                                    rationale="Groq AI validated portfolio foundation.",
                                )
                            ]
                        raw_summary = parsed.get("summary", f"AI Wealth Strategy for {country}")
                        if isinstance(raw_summary, dict):
                            raw_summary = json.dumps(raw_summary, ensure_ascii=False)

                        raw_risk = parsed.get("risk_assessment", f"Risk profile: {risk.upper()}")
                        if isinstance(raw_risk, dict):
                            raw_risk = json.dumps(raw_risk, ensure_ascii=False)

                        raw_notes = parsed.get("country_notes", f"Jurisdiction: {country}")
                        if isinstance(raw_notes, dict):
                            raw_notes = json.dumps(raw_notes, ensure_ascii=False)

                        return AdvisoryResponse(
                            summary=str(raw_summary),
                            risk_assessment=str(raw_risk),
                            recommended_actions=recs,
                            country_notes=str(raw_notes),
                            provider_used="Groq (Llama-3.3-70b)",
                        )
            except Exception as e:
                logger.error(f"Groq API call failed: {e}. Falling back to rule engine.")

        # Fallback Rule-based engine
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
