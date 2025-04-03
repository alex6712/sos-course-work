from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, HTTPException, status, Path
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_session, validate_access_token
from api.services import (
    employee_service,
    merch_item_service,
    transaction_service,
)
from database.tables.entities import Employee, MerchItem
from schemas.requests import SendCoinsRequest
from schemas.responses import StandardResponse

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
)


@router.post(
    "/send_coins",
    response_model=StandardResponse,
    status_code=status.HTTP_200_OK,
    summary="Отправить монеты другому сотруднику.",
)
async def send_coins(
    request_body: Annotated[SendCoinsRequest, Body()],
    sender: Annotated[Employee, Depends(validate_access_token)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    """Метод перевода монет от сотрудника к сотруднику.

    Проверяет корректность введённых данных и достаточно ли монет для выполнения перевода.
    Выполняет перевод, сохраняет данные о переводе в базу данных.

    Parameters
    ----------
    request_body : SendCoinsRequest
        Тело запроса, в котором содержится информация о получателе
        и количестве монет для перевода.
    sender : Employee
        Объект пользователя-отправителя.
    session : AsyncSession
        Объект сессии запроса.

    Returns
    -------
    response : StandardResponse
        Отчёт о выполнении перевода.
    """
    if request_body.coins_amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Количество монет не может быть отрицательным или равным нулю.",
        )

    if sender.coins_amount < request_body.coins_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Невозможно выполнить перевод, т.к. на счёте недостаточно средств.",
        )

    gainer: Employee = await employee_service.get_employee_by_id(
        session, request_body.gainer_id
    )

    if not gainer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Сотрудник с таким UUID не найден.",
        )

    if sender.id == gainer.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Отправитель и получатель не могут совпадать.",
        )

    try:
        await transaction_service.spend_coins(
            session, sender, request_body.coins_amount
        )

        await transaction_service.gain_coins(session, gainer, request_body.coins_amount)

        await transaction_service.register_transfer(
            session, sender.id, gainer.id, request_body.coins_amount
        )
    except Exception as e:
        await session.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Неизвестная ошибка: {e}.",
        )

    return {"code": 200, "message": "Монеты успешно отправлены."}


@router.get(
    "/buy/{merch_item_id}",
    response_model=StandardResponse,
    status_code=status.HTTP_200_OK,
    summary="Метод покупки предмета за монеты.",
)
async def buy(
    merch_item_id: Annotated[UUID, Path(description="UUID товара к покупке.")],
    employee: Annotated[Employee, Depends(validate_access_token)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    """Метод покупки продукта.

    Находит запись о продукте (в ином случае возвращает Not Found 404), сверяет цену,
    списывает деньги со счёта сотрудника и добавляет запись о покупке продукта.

    Parameters
    ----------
    merch_item_id : UUID
        UUID продукта.
    employee : Employee
        Объект сотрудника-покупателя.
    session : AsyncSession
        Объект сессии запроса.

    Returns
    -------
    response : StandardResponse
        Отчёт о выполнении покупки.
    """
    merch_item: MerchItem = await merch_item_service.get_merch_item_by_id(
        session, merch_item_id
    )

    print(merch_item)

    if not merch_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Продукт с таким UUID не найден.",
        )

    if employee.coins_amount < merch_item.price:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Невозможно купить продукт, т.к. на счёте недостаточно средств.",
        )

    try:
        await transaction_service.spend_coins(session, employee, merch_item.price)

        await transaction_service.register_purchase(session, employee.id, merch_item_id)
    except Exception as e:
        await session.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Неизвестная ошибка: {e}.",
        )

    return {"code": 200, "message": "Покупка совершена успешно."}
