from typing import Annotated

from fastapi import APIRouter, Depends

from api.dependencies import validate_access_token
from database.tables.entities import Employee

router = APIRouter(
    prefix="/employees",
    tags=["employees"],
)


@router.get(
    "/inventory",
    summary="Предоставляет информацию об инвентаре пользователя.",
)
async def inventory(employee: Annotated[Employee, Depends(validate_access_token)]):
    return {"code": 200, "message": employee.id}


@router.get(
    "/wallet",
    summary="Предоставляет информацию о кошельке пользователя.",
)
async def wallet():
    return {"code": 200, "message": "Всё ок!"}
