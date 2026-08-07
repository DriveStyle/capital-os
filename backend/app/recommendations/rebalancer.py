"""
Portfolio Rebalancer & Risk Scoring Engine for Capital OS.
Calculates buy-only rebalancing allocations to avoid tax events.
"""

from typing import List, Dict, Any

class PortfolioRebalancer:
    DEFAULT_TARGETS = {
        "conservative": {"ETF": 0.40, "Bond": 0.40, "Yield": 0.15, "Crypto": 0.05},
        "moderate": {"ETF": 0.70, "Bond": 0.10, "Yield": 0.10, "Crypto": 0.10},
        "aggressive": {"ETF": 0.65, "Bond": 0.0, "Yield": 0.05, "Crypto": 0.30},
    }

    @classmethod
    def calculate_rebalance(
        cls,
        current_assets: List[Dict[str, Any]],
        monthly_budget: float,
        risk_profile: str = "moderate"
    ) -> Dict[str, Any]:
        targets = cls.DEFAULT_TARGETS.get(risk_profile.lower(), cls.DEFAULT_TARGETS["moderate"])
        total_current_value = sum(a.get("value", 0.0) for a in current_assets)
        projected_total = total_current_value + monthly_budget

        # Group current value by asset type
        type_values: Dict[str, float] = {}
        for a in current_assets:
            atype = a.get("type", "ETF")
            type_values[atype] = type_values.get(atype, 0.0) + a.get("value", 0.0)

        # Calculate target dollar amounts for projected total
        target_dollars = {atype: projected_total * weight for atype, weight in targets.items()}

        # Shortfall per type (what is underweight)
        shortfalls: Dict[str, float] = {}
        total_shortfall = 0.0
        for atype, target_amt in target_dollars.items():
            current_amt = type_values.get(atype, 0.0)
            diff = max(0.0, target_amt - current_amt)
            shortfalls[atype] = diff
            total_shortfall += diff

        # Allocate monthly budget proportionally to underweight categories
        buy_allocations: List[Dict[str, Any]] = []
        if total_shortfall > 0 and monthly_budget > 0:
            for atype, sf in shortfalls.items():
                if sf > 0:
                    allocated_amount = round((sf / total_shortfall) * monthly_budget, 2)
                    percentage = round((allocated_amount / monthly_budget) * 100, 1)
                    buy_allocations.append({
                        "asset_type": atype,
                        "recommended_buy_amount": allocated_amount,
                        "percentage_of_budget": percentage,
                        "action": f"Buy {atype} assets to bring category closer to target ({int(targets.get(atype, 0)*100)}%)"
                    })
        else:
            # Equal spread if already balanced
            spread_per_type = round(monthly_budget / len(targets), 2)
            for atype in targets.keys():
                buy_allocations.append({
                    "asset_type": atype,
                    "recommended_buy_amount": spread_per_type,
                    "percentage_of_budget": round((1 / len(targets)) * 100, 1),
                    "action": f"Balanced top-up of {atype}"
                })

        # Calculate portfolio risk score (0 - 100)
        risk_score = 30 if risk_profile == "conservative" else (55 if risk_profile == "moderate" else 85)

        return {
            "current_total_value": total_current_value,
            "monthly_budget": monthly_budget,
            "projected_total_value": projected_total,
            "risk_profile": risk_profile,
            "risk_score": risk_score,
            "target_weights": targets,
            "buy_allocations": buy_allocations,
            "tax_efficient_note": "Rebalancing performed strictly via fresh buy orders. No asset sales required, zero capital gains tax triggered."
        }
