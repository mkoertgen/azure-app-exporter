from fastapi import FastAPI
from core.config import settings

from api.api import api_router


def add_api(app: FastAPI):
    app.include_router(api_router, prefix=settings.API_BASE)
