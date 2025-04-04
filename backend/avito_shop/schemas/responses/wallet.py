from typing import List

from pydantic import Field

from .standard import StandardResponse
from schemas import TransferSchema


class WalletResponse(StandardResponse):
    """Модель ответа сервера на запрос о кошельке сотрудника.

    Содержит в себе список всех переводов (отправленных и полученных) сотрудника.

    Attributes
    ----------
    coins_amount : float
        Количество монет на аккаунте сотрудника.
    transfers : List[TransferSchema]
        Список всех переводов сотрудника.
    """

    coins_amount: float = Field(examples=[1000.0])
    transfers: List[TransferSchema] = Field()
