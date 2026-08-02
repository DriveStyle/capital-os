# Capital OS — Project Constitution & System Spec

## Project Overview
Capital OS is an AI-powered Personal Wealth Operating System for long-term investing, portfolio management, AI recommendations, financial planning, and Telegram Mini App interaction.

## Sub-System Architecture
- **Backend API**: FastAPI (Python 3.12) with SQLAlchemy 2.x, Alembic, Pydantic v2.
- **Frontend App**: Next.js 14 / React / TypeScript / Tailwind CSS.
- **AI Intelligence Layer**: Multi-provider abstraction (Gemini, OpenAI, Claude, Grok) for portfolio analysis and wealth advice.
- **Telegram Bot / Mini App**: Interface for instant notifications, portfolio status, and voice/chat commands.

## Key Rules & Invariants
1. Session Safety: Preserving any Telegram `*.session` files.
2. Deployment Invariants: Keep `main.py` entrypoint and `venv` intact.
3. Anti-Hallucination: Validate all DB models and API schemas with empirical tests before declaring done.
