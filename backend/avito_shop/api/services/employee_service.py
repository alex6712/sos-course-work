from typing import AnyStr

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.tables.entities import Employee
from schemas import EmployeeWithPasswordSchema


async def get_employee_by_username(session: AsyncSession, username: AnyStr) -> Employee:
    """Возвращает модель сотрудника для дальнейшей работы.

    Parameters
    ----------
    session : AsyncSession
        Объект сессии запроса.
    username : AnyStr
        Логин сотрудника, уникальное имя.

    Returns
    -------
    employee : Employee
        Модель записи сотрудника из базы данных.
    """
    return await session.scalar(select(Employee).where(Employee.username == username))


async def update_refresh_token(
    session: AsyncSession, employee: Employee, refresh_token: AnyStr
):
    """Перезаписывает токен обновления сотрудника.

    Note
    ----
    В этом случае используются функции SQLAlchemy ORM, которые позволяют
    изменить значение атрибута объекта записи сотрудника,
    и при закрытии сессии эти изменения будут сохранены в базе данных.

    Parameters
    ----------
    session : AsyncSession
        Объект сессии запроса.
    employee : Employee
        Объект сотрудника.
    refresh_token : AnyStr
        Новый токен обновления.
    """
    employee.refresh_token = refresh_token
    await session.commit()


async def add_employee(
    session: AsyncSession, employee_info: EmployeeWithPasswordSchema
):
    """Добавляет в базу данных новую запись о сотруднике.

    Parameters
    ----------
    session : AsyncSession
        Объект сессии запроса.
    employee_info : EmployeeWithPasswordSchema
        Схема объекта сотрудника с паролем.
    """
    session.add(Employee(**employee_info.model_dump()))
    await session.commit()
