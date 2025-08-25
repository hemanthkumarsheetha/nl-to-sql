from fastapi import APIRouter
from models.api_models import HealthCheckResult

router = APIRouter(prefix="/health", tags=["health"])



@router.get("/")
async def health_check():
    return HealthCheckResult(status="ok")