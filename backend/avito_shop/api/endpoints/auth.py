import re
from typing import Annotated, AnyStr, Dict

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_session, validate_refresh_token
from api.services import employee_service
from core.jwt import create_jwt_pair
from core.security import hash_, verify
from database.tables.entities import Employee
from schemas.requests import SignUpRequest
from schemas.responses import StandardResponse, TokenResponse

router = APIRouter(
    prefix="/auth",
    tags=["authorization"],
)


@router.post(
    "/sign_in",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Аутентификация.",
)
async def sign_in(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    """Метод аутентификации.

    В теле запроса получает данные аутентификации сотрудника (имя пользователя, пароль),
    выполняет аутентификацию и возвращает JWT.

    Parameters
    -----------
    form_data : OAuth2PasswordRequestForm
        Данные аутентификации сотрудника.
    session : AsyncSession
        Объект сессии запроса.

    Returns
    -------
    response : TokenResponse
        Модель ответа сервера с вложенной парой JWT.
    """
    employee = await employee_service.get_employee_by_username(
        session, form_data.username
    )

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify(form_data.password, employee.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {**await _get_jwt_pair(employee, session), "token_type": "bearer"}


@router.post(
    "/sign_up",
    response_model=StandardResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Регистрация.",
)
async def sign_up(
    employee: Annotated[SignUpRequest, Body()],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    """Метод регистрации.

    Получает модель сотрудника (с паролем) в качестве ввода и добавляет запись в базу данных.

    Parameters
    ----------
    employee : SignUpRequest
        Схема объекта сотрудника.
    session : AsyncSession
        Объект сессии запроса.

    Returns
    -------
    response : StandardResponse
        Положительный ответ о регистрации сотрудника.
    """
    employee.password = hash_(employee.password)

    try:
        await employee_service.add_employee(session, employee)
    except IntegrityError as integrity_error:
        await session.rollback()

        # Необходимо для тестов, т.к. текст ошибки SQLite отличается от PostgreSQL
        if "sqlite3" in str(integrity_error):
            column, *_ = re.search(r"\.(.*)", str(integrity_error.orig)).groups()
            value: str = employee.model_dump()[column]

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f'Employee with {column}="{value}" already exists!',
            )
        elif result := re.search(r'"\((.*)\)=\((.*)\)"', str(integrity_error.orig)):
            column, value = result.groups()

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f'Employee with {column}="{value}" already exists!',
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough data in request.",
        )

    return {
        "code": status.HTTP_201_CREATED,
        "message": "Employee created successfully.",
    }


@router.get(
    "/refresh",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Обновление токена доступа.",
)
async def refresh(
    employee: Annotated[Employee, Depends(validate_refresh_token)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    """Метод повторной аутентификации через токен обновления.

    Получает ``refresh_token`` в заголовке, проверяет на совпадение в базе данных
    используя закодированную информацию, перезаписывает токен обновления в базе данных и
    возвращает новую пару ``access_token`` + ``refresh_token``.

    Parameters
    ----------
    employee : Employee
        Объект сотрудника, полученный из зависимости автоматической аутентификации.
    session : AsyncSession
        Объект сессии запроса.

    Returns
    -------
    response : TokenResponse
        Модель ответа сервера с вложенной парой JWT.
    """
    return {**await _get_jwt_pair(employee, session), "token_type": "bearer"}


async def _get_jwt_pair(
    employee: Employee, session: AsyncSession
) -> Dict[AnyStr, AnyStr]:
    """Функция создания новой пары JWT.

    Создает пару ``access_token`` и ``refresh_token``, перезаписывает токен обновления сотрудника
    в базе данных и возвращает пару JWT.

    Parameters
    ----------
    employee : Employee
        Объект сотрудника.
    session : AsyncSession
        Объект сессии запроса.

    Returns
    -------
    tokens : Dict[AnyStr, AnyStr]
        Пара JWT в форме словаря с двумя ключами: ``access_token`` и ``refresh_token``.

        ``access_token``:
            Токен доступа (``str``).
        ``refresh_token``:
            Токен обновления (``str``).
    """
    tokens = create_jwt_pair({"sub": employee.username})

    try:
        await employee_service.update_refresh_token(
            session, employee, tokens["refresh_token"]
        )
    except IntegrityError:
        await session.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect request.",
        )

    return tokens
