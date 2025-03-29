from fastapi import APIRouter
from ..models.pod import PodRef, PodRefs
from ..services.pod import PodService

router = APIRouter()

@router.post("/")
async def create_pod() -> PodRef:
    """Creates a managed pod."""
    service = PodService()
    return await service.create_pod()

@router.get("/{pod_name}")
async def get_pod(pod_name: str) -> PodRef:
    """Fetches the status of a specific managed pod."""
    service = PodService()
    return await service.get_pod(pod_name)

@router.delete("/{pod_name}", status_code=204)
async def delete_pod(pod_name: str):
    """Deletes a managed pod."""
    service = PodService()
    await service.delete_pod(pod_name)

@router.get("/")
async def list_pods() -> PodRefs:
    """Lists all managed pods in the namespace."""
    service = PodService()
    return await service.list_pods()

@router.delete("/", status_code=204)
async def delete_pods():
    """Deletes all managed pods."""
    service = PodService()
    await service.delete_pods()