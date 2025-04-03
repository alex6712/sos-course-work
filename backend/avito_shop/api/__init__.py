from fastapi import APIRouter

from .endpoints import (
    auth_router,
    employees_router,
    root_router,
    transactions_router,
)


api_router = APIRouter(
    prefix="/api",
)
api_router.include_router(auth_router)
api_router.include_router(employees_router)
api_router.include_router(root_router)
api_router.include_router(transactions_router)
