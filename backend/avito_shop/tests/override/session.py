from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from tests.override import test_engine

TestAsyncSessionMaker: async_sessionmaker = async_sessionmaker(
    bind=test_engine, class_=AsyncSession, expire_on_commit=False
)


async def override_get_session() -> AsyncSession:
    """Создает уникальный объект асинхронной сессии запроса.

    Используется для переопределения подобной общей зависимости для изоляции тестов.
    Добавляет сессию базы данных в маршрут запроса, используя систему зависимости FastAPI.

    Returns
    -------
    session : AsyncSession
        Объект асинхронной сессии запроса.
    """
    async with TestAsyncSessionMaker() as test_session:
        yield test_session
