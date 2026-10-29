from fastapi import APIRouter
from app.api.routes import (
    map
)

api_router = APIRouter()

api_router.include_router(map.router, tags=["map"], prefix="/map")