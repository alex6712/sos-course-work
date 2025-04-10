from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from core.config import Settings, get_settings

settings: Settings = get_settings()

test_engine: AsyncEngine = create_async_engine(
    url=settings.TEST_DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)

from .initialize import override_initialize
from .session import override_get_session
