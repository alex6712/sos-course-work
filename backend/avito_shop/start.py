import asyncio

import uvicorn

from core.config import Settings, get_settings
from database import initialize

if __name__ == "__main__":
    settings: Settings = get_settings()

    if settings.INITIALIZE_DB:
        asyncio.run(initialize())

    print(
        f"Swagger UI URL: \033[97mhttp://{settings.DOMAIN}:{settings.BACKEND_PORT}/docs\033[0m"
    )

    uvicorn.run(
        app="main:avito_shop",
        host=settings.DOMAIN,
        port=settings.BACKEND_PORT,
        reload=settings.DEV_MODE,
    )
