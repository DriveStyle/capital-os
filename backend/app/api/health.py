from fastapi import APIRouter
from ..schemas.health import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/", response_model=dict[str, str])
def root_info() -> dict[str, str]:
    return {"project": "Capital OS", "version": "0.1.0"}


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="Capital OS")
