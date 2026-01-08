from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from system.app.core.config import settings
from .api.v1.routers.health_router import router as health_router
from .api.v1.routers.email_router import router as email_router

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(email_router)