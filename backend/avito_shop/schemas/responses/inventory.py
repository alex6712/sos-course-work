from typing import List

from pydantic import Field

from .standard import StandardResponse
from schemas import PurchaseSchema


class InventoryResponse(StandardResponse):
    """Модель ответа сервера на запрос о содержимом инвентаря сотрудника.

    Содержит в себе список всех покупок сотрудника.

    Attributes
    ----------
    purchases : List[PurchaseSchema]
        Список всех покупок, совершённых сотрудником.
    """

    purchases: List[PurchaseSchema] = Field()
