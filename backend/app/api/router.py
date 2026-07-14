from fastapi import APIRouter

from .health import router as health_router

router = APIRouter()
router.include_router(health_router)


@router.get("/")
def root() -> dict[str, str]:
    return {"project": "Capital OS", "status": "running"}
