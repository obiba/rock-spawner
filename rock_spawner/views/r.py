from typing import Dict
from fastapi import APIRouter
from ..services.r import RService

router = APIRouter()


@router.get("/")
async def get_status() -> Dict:
    """Get R server info."""
    service = RService()
    status = await service.get_status()
    await service.close()
    return status

@router.get("/packages")
async def get_packages() -> Dict:
    """Lists all R packages."""
    service = RService()
    pkgs = await service.get_packages()
    await service.close()
    return pkgs

@router.get("/packages/_datashield")
async def get_datashield_packages() -> Dict:
    """Lists all DataSHIELD R packages."""
    service = RService()
    pkgs = await service.get_datashield_packages()
    await service.close()
    return pkgs