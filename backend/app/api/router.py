from fastapi import APIRouter

from .health import router as health_router
from .users import router as users_router
from .portfolios import router as portfolios_router
from .goals import router as goals_router
from .ai import router as ai_router

router = APIRouter()
router.include_router(health_router)
router.include_router(users_router)
router.include_router(portfolios_router)
router.include_router(goals_router)
router.include_router(ai_router)
