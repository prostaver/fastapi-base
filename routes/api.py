from fastapi import APIRouter

# from app.api.api_v1.endpoints import items, login, users, utils
from routes.endpoints import (  # noqa F401
    items,
    users,
)

api_router = APIRouter()

api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
