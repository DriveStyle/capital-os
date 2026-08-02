# Capital OS

Capital OS is an AI-powered Personal Wealth Operating System designed to help individuals build long-term wealth through disciplined investing, portfolio management, AI recommendations, and financial planning.

## Overview

The platform combines:
- personal finance planning
- portfolio tracking
- country-specific investment strategies
- explainable AI recommendations
- Telegram-based interaction
- voice-first assistance

## Technology Stack

### Backend
- Python 3.12
- FastAPI
- SQLAlchemy
- Alembic
- Pydantic
- Uvicorn

### Frontend
- Next.js
- React
- TypeScript
- TailwindCSS

### Data & Infrastructure
- PostgreSQL
- Docker
- python-dotenv

### AI
- Provider abstraction layer for OpenAI, Anthropic Claude, Google Gemini, and Grok

## Architecture

Capital OS follows clean architecture principles with:
- modular domain packages
- repository pattern
- dependency injection-friendly services
- API-first backend design
- scalable multi-provider AI layer

## Roadmap

- MVP onboarding and profile setup
- portfolio engine and recommendation service
- country-specific financial modules
- Telegram Mini App integration
- voice assistant support
- advanced reporting and analytics

## Running Locally

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Environment
Copy `.env.example` to `.env` and adjust credentials as needed.
