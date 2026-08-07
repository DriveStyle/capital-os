from fastapi import FastAPI

from .api.router import router
from .config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="AI-powered Personal Wealth Operating System",
)

from .api.webapp import WEBAPP_HTML
from fastapi.responses import HTMLResponse

app.include_router(router, prefix=settings.api_prefix)


@app.get("/", response_class=HTMLResponse)
@app.get("/webapp", response_class=HTMLResponse)
@app.get("/app", response_class=HTMLResponse)
def serve_webapp_root():
    return HTMLResponse(content=WEBAPP_HTML)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name}

