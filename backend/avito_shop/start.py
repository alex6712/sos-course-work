import uvicorn

from core.config import Settings, get_settings

if __name__ == "__main__":
    settings: Settings = get_settings()

    print(f"Swagger UI URL: http://{settings.DOMAIN}:{settings.BACKEND_PORT}/docs")

    uvicorn.run(
        app="main:avito_shop",
        host=settings.DOMAIN,
        port=settings.BACKEND_PORT,
        reload=settings.DEV_MODE,
    )

