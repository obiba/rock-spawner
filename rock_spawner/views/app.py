from typing import List
from fastapi import APIRouter, status 
from pydantic import BaseModel
from ..config import _config

router = APIRouter()

class HealthCheck(BaseModel):
    """Response model to validate and return when performing a health check."""
    status: str = "OK"

class AppInfo(BaseModel):
    """Response model to validate and return when performing a health check."""
    id: str
    type: str
    cluster: str
    tags: List[str]

@router.get(
    "/healthz",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
)
async def get_health() -> HealthCheck:
    """
    Endpoint to perform a healthcheck on for kubenernetes liveness and
    readiness probes.
    """
    return HealthCheck(status="OK")

@router.get(
    "/_info",
    status_code=status.HTTP_200_OK,
    response_model=AppInfo,
)
async def get_info() -> AppInfo:
    """
    Endpoint to return information about the application.
    """
    return AppInfo(
        id=f"{_config.APP_BASENAME}-spawner",
        type="rock-spawner",
        cluster=_config.ROCK_CLUSTER,
        tags=[],
    )