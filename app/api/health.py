from fastapi import APIRouter
from app.schemas.health import HealthCheckResponse
router = APIRouter(
    prefix = "/health"
)

@router.get("", tags = ["Health"])
async def health_check()->HealthCheckResponse:
    return HealthCheckResponse(
        status = "OK"      
    )
