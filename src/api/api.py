from fastapi import APIRouter

from api import apps

api_router = APIRouter()
api_router.include_router(sp.router, prefix="/apps", tags=["apps"])
