from fastapi import APIRouter

from app.services.subscription_manager import manager

router = APIRouter()


@router.get("/health")
async def health_check():
    stats = await manager.stats
    return {
        "status": "healthy",
        "connections": stats,
    }
