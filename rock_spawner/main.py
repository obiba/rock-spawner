from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from logging import basicConfig, DEBUG
from .views.app import router as app_router
from .views.pod import router as pod_router
from .views.r import router as r_router

basicConfig(level=DEBUG)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    app_router,
    prefix="",
    tags=["App"],
)

app.include_router(
    pod_router,
    prefix="/pod",
    tags=["Pods"],
)

app.include_router(
    r_router,
    prefix="/rserver",
    tags=["R Server"],
)
