from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from database.tables.entities import Employee
from database.tables.junctions import Purchase, Transfer


async def register_purchase(
    session: AsyncSession, employee_id: UUID, merch_item_id: UUID
):
    """Добавляет в базу данных запись о покупке.

    Parameters
    ----------
    session : AsyncSession
        Объект сессии запроса.
    employee_id : UUID
        UUID сотрудника-покупателя.
    merch_item_id : UUID
        UUID покупаемого продукта.
    """
    session.add(Purchase(employee_id=employee_id, merch_item_id=merch_item_id))
    await session.commit()


async def register_transfer(
    session: AsyncSession, sender_id: UUID, gainer_id: UUID, coins_amount: float
):
    """Добавляет в базу данных запись о переводе.

    Parameters
    ----------
    session : AsyncSession
        Объект сессии запроса.
    sender_id : UUID
        UUID сотрудника-отправителя.
    gainer_id : UUID
        UUID сотрудника-получателя.
    coins_amount : float
        Количество переводимых монет.
    """
    session.add(Transfer(sender_id=sender_id, gainer_id=gainer_id, amount=coins_amount))
    await session.commit()


async def spend_coins(session: AsyncSession, employee: Employee, coins_amount: float):
    """Вычитает переданное количество монет с аккаунта сотрудника.

    Parameters
    ----------
    session : AsyncSession
        Объект сессии запроса.
    employee : Employee
        Объект сотрудника-отправителя.
    coins_amount : float
        Количество отправленных монет.
    """
    employee.coins_amount -= coins_amount
    await session.commit()


async def gain_coins(session: AsyncSession, employee: Employee, coins_amount: float):
    """Добавляет полученное количество монет на аккаунта сотрудника.

    Parameters
    ----------
    session : AsyncSession
        Объект сессии запроса.
    employee : Employee
        Объект сотрудника-отправителя.
    coins_amount : float
        Количество полученных монет.
    """
    employee.coins_amount += coins_amount
    await session.commit()
