from fastapi import APIRouter, status

router = APIRouter(
    prefix="/user_info",
    tags=["user_info"],
)


@router.get(
    "/inventory",
    summary="Предоставляет информацию об инвентаре пользователя.",
)
async def inventory():
    return {"code": 200, "message": "Всё ок!"}


@router.get(
    "/wallet",
    summary="Предоставляет информацию о кошельке пользователя.",
)
async def wallet():
    return {"code": 200, "message": "Всё ок!"}
