"""
Country & Tax Rules Engine for Capital OS.
Provides localized tax contexts, broker recommendations, and investment rules.
"""

from typing import Dict, Any, List

COUNTRY_CONFIGS: Dict[str, Dict[str, Any]] = {
    "UA": {
        "country_name": "Ukraine",
        "currency": "UAH",
        "base_fiat_symbol": "₴",
        "capital_gains_tax_rate": 0.18,
        "military_tax_rate": 0.015,
        "total_investment_tax_rate": 0.195,
        "dividend_tax_rate": 0.09,
        "recommended_brokers": ["Interactive Brokers", "Freedom Finance", "Monobank (OVDP)", "Sense Bank"],
        "tax_notes": "Foreign dividend income taxed at 9% + 1.5% military levy. Government bonds (OVDP) are 100% tax-exempt.",
        "preferred_assets": ["OVDP (Government Bonds)", "Global Index ETFs (VWRA/VUAA)", "High-Yield Reserves"],
    },
    "US": {
        "country_name": "United States",
        "currency": "USD",
        "base_fiat_symbol": "$",
        "capital_gains_tax_rate": 0.15,
        "military_tax_rate": 0.0,
        "total_investment_tax_rate": 0.15,
        "dividend_tax_rate": 0.15,
        "recommended_brokers": ["Vanguard", "Fidelity", "Charles Schwab", "Robinhood"],
        "tax_notes": "Utilize tax-advantaged accounts (Roth IRA, 401k) to maximize tax-free growth up to annual contribution limits.",
        "preferred_assets": ["VTI (Total US Stock)", "VOO (S&P 500)", "BND (Total Bond)", "VT (Total World)"],
    },
    "DE": {
        "country_name": "Germany",
        "currency": "EUR",
        "base_fiat_symbol": "€",
        "capital_gains_tax_rate": 0.25,
        "military_tax_rate": 0.055,  # Solidaritätszuschlag portion
        "total_investment_tax_rate": 0.26375,
        "dividend_tax_rate": 0.26375,
        "recommended_brokers": ["Scalable Capital", "Trade Republic", "Interactive Brokers", "Comdirect"],
        "tax_notes": "Abgeltungsteuer rate 25% + Soli. Annual Sparerpauschbetrag tax-free allowance of €1,000 per person.",
        "preferred_assets": ["Accumulating ETFs (iShares Core S&P 500)", "Vanguard FTSE All-World (VWCE)"],
    },
    "UK": {
        "country_name": "United Kingdom",
        "currency": "GBP",
        "base_fiat_symbol": "£",
        "capital_gains_tax_rate": 0.20,
        "military_tax_rate": 0.0,
        "total_investment_tax_rate": 0.20,
        "dividend_tax_rate": 0.0875,
        "recommended_brokers": ["Interactive Investor", "AJ Bell", "Trading 212", "Hargreaves Lansdown"],
        "tax_notes": "Stocks & Shares ISA allows £20,000 tax-free investment annually with zero capital gains tax.",
        "preferred_assets": ["ISA Global Equity ETFs", "FTSE All-World UCITS ETF"],
    },
}


class CountryEngine:
    @staticmethod
    def get_country_info(country_code: str) -> Dict[str, Any]:
        code = country_code.upper()
        return COUNTRY_CONFIGS.get(code, COUNTRY_CONFIGS["US"])

    @staticmethod
    def get_supported_countries() -> List[str]:
        return list(COUNTRY_CONFIGS.keys())
