import asyncio
import signal
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from logging import basicConfig, DEBUG
from pydantic import BaseModel
from .views.pod import terminate_pods, router as pod_router

basicConfig(level=DEBUG)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic here (if needed)
    yield
    # Shutdown logic here
    await terminate_pods()

# Handle OS signals (SIGTERM, SIGINT)
def handle_exit(*args):
    asyncio.create_task(terminate_pods())

signal.signal(signal.SIGTERM, handle_exit)
signal.signal(signal.SIGINT, handle_exit)

app = FastAPI(lifespan=lifespan)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class HealthCheck(BaseModel):
    """Response model to validate and return when performing a health check."""
    status: str = "OK"

@app.get(
    "/healthz",
    tags=["Healthcheck"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
)
async def get_health(
) -> HealthCheck:
    """
    Endpoint to perform a healthcheck on for kubenernetes liveness and
    readiness probes.
    """
    return HealthCheck(status="OK")

app.include_router(
    pod_router,
    prefix="/pod",
    tags=["Pods"],
)
