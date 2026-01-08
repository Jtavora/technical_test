# system/app/api/v1/routers/health_router.py
from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/ping")
def ping():
    return {"ping": "pong",
            "status": "ok"}