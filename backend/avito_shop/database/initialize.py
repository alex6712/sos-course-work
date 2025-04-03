from contextlib import asynccontextmanager
from asyncpg.exceptions import ConnectionDoesNotExistError
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    AsyncSession,
)
from sqlalchemy import select

from core.config import Settings, get_settings
from database.tables.base import Base
from database.tables.entities import MerchItem


PRODUCTS = [
    {"name": "t-shirt", "price": 80},
    {"name": "cup", "price": 20},
    {"name": "book", "price": 50},
    {"name": "pen", "price": 10},
    {"name": "powerbank", "price": 200},
    {"name": "hoody", "price": 300},
    {"name": "umbrella", "price": 200},
    {"name": "socks", "price": 10},
    {"name": "wallet", "price": 50},
    {"name": "pink-hoody", "price": 500},
]


async def initialize():
    """Инициализация базы данных.

    Сбрасывает все таблицы, а затем воссоздает.
    Это удалит всю информацию из существующих таблиц, поэтому
    это очень небезопасная операция.

    Вот почему эта функция требует подтверждения суперпользователя.
    """
    settings: Settings = get_settings()

    database_user: str = input("Please, enter the superuser login: ")
    database_password: str = input("Please, enter the superuser password: ")

    engine: AsyncEngine = create_async_engine(
        url=f"postgresql+asyncpg://{database_user}:{database_password}@{settings.DOMAIN}"
        f":{settings.DATABASE_PORT}/{settings.DATABASE_NAME}",
        echo=False,
        pool_pre_ping=True,
    )

    error = (
        "\n\033[91mWhile initializing database:"
        "\n\tFAIL:  {fail}"
        "\n\tCAUSE: {cause}"
        "\nContinuing without initializing...\033[0m\n"
    )

    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        async with AsyncSession(engine) as session:
            existing_products = await session.execute(select(MerchItem.name))
            existing_products = {row[0] for row in existing_products.all()}

            new_products = [MerchItem(**product) for product in PRODUCTS if
                            product["name"] not in existing_products]

            if new_products:
                session.add_all(new_products)
                await session.commit()
                print("\033[94mProducts added successfully.\033[0m")
            else:
                print("\033[93mNo new products to add.\033[0m")
    except ConnectionDoesNotExistError:
        print(
            error.format(
                fail="Unable to establish a connection.",
                cause="Incorrect password or username.",
            )
        )
    except ProgrammingError:
        print(
            error.format(
                fail="Unable to establish a connection.",
                cause="User is not the superuser.",
            )
        )
    else:
        print("\n\033[92mDatabase initialized and products added successfully.\033[0m\n")
