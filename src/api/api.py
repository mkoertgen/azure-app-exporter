from fastapi import APIRouter

from api import sp

api_router = APIRouter()
api_router.include_router(sp.router, prefix="/sp", tags=["sp"])
