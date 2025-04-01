from fastapi import APIRouter

from .endpoints import (
    root_router,
    user_info_router,
)


api_router = APIRouter(
    prefix="/api",
)
api_router.include_router(root_router)
api_router.include_router(user_info_router)
