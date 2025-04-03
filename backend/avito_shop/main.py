from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import api_router
from core.config import Settings, get_settings

settings: Settings = get_settings()

tags_metadata = [
    {
        "name": "root",
        "description": "Получение информации о **приложении**.",
    },
    {
        "name": "authorization",
        "description": "Операции **регистрации** и **аутентификации**.",
    },
    {
        "name": "employees",
        "description": "Получение информации об **инвентаре** и **кошельке** пользователя.",
    },
    {
        "name": "transactions",
        "description": "Выполнение операций **перевода** и **покупки**.",
    },
]

avito_shop = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    summary=settings.APP_SUMMARY,
    contact={
        "name": settings.ADMIN_NAME,
        "email": settings.ADMIN_EMAIL,
    },
    openapi_tags=tags_metadata,
)

avito_shop.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

avito_shop.include_router(api_router)
