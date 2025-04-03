from typing import Annotated

from fastapi import APIRouter, Depends, status

from api.dependencies import validate_access_token
from database.tables.entities import Employee
from schemas.responses import InventoryResponse, WalletResponse

router = APIRouter(
    prefix="/employees",
    tags=["employees"],
)


@router.get(
    "/inventory",
    response_model=InventoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Предоставляет информацию об инвентаре пользователя.",
)
async def inventory(
    employee: Annotated[Employee, Depends(validate_access_token)],
):
    """Метод получения инвентаря пользователя.

    Возвращает список всех совершённых сотрудником покупок.

    Parameters
    ----------
    employee : Employee
        Объект сотрудника.

    Returns
    -------
    response : InventoryResponse
        Список всех покупок, совершённых пользователем.
    """
    return {"purchases": await employee.awaitable_attrs.purchases}


@router.get(
    "/wallet",
    response_model=WalletResponse,
    status_code=status.HTTP_200_OK,
    summary="Предоставляет информацию о кошельке пользователя.",
)
async def wallet(
    employee: Annotated[Employee, Depends(validate_access_token)],
):
    """Метод получения кошелька пользователя.

    Возвращает список всех отправленных и полученных сотрудником переводов.

    Parameters
    ----------
    employee : Employee
        Объект сотрудника.

    Returns
    -------
    response : InventoryResponse
        Список всех переводов сотрудника.
    """
    return {"transfers": await employee.awaitable_attrs.all_transfers}
