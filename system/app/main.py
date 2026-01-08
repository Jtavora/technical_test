# system/app/main.py
from fastapi import FastAPI

# IMPORTS CORRIGIDOS (relativos ao pacote app)
from .api.v1.routers.health_router import router as health_router
from .api.v1.routers.email_router import router as email_router

app = FastAPI(
    title="Email Classification API",
    version="0.1.0",
)

app.include_router(health_router)
app.include_router(email_router)