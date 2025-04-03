from typing import List

from pydantic import Field

from .standard import StandardResponse
from schemas import TransferSchema


class WalletResponse(StandardResponse):
    """Модель ответа сервера на запрос о кошельке сотрудника.

    Содержит в себе список всех переводов (отправленных и полученных) сотрудника.

    Attributes
    ----------
    transfers : List[TransferSchema]
        Список всех переводов сотрудника.
    """

    transfers: List[TransferSchema] = Field()
