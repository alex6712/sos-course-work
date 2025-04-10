from asyncpg.exceptions import ConnectionDoesNotExistError
from sqlalchemy import select
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.ext.asyncio import AsyncSession

from database.tables.base import Base
from database.tables.entities import MerchItem
from tests.override import test_engine

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


async def override_initialize():
    """Инициализирует тестовую базу данных.

    Инициализирует тестовую in-memory SQLite базу данных для изоляции
    тестов.

    Эта функция не требует подтверждения суперпользователя.
    """
    error = (
        "\n\033[91mWhile initializing database:"
        "\n\tFAIL:  {fail}"
        "\n\tCAUSE: {cause}"
        "\nContinuing without initializing...\033[0m\n"
    )

    try:
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        async with AsyncSession(test_engine) as session:
            existing_products = await session.execute(select(MerchItem.name))
            existing_products = {row[0] for row in existing_products.all()}

            new_products = [
                MerchItem(**product)
                for product in PRODUCTS
                if product["name"] not in existing_products
            ]

            if new_products:
                session.add_all(new_products)
                await session.commit()
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
