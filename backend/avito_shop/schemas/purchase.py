from uuid import UUID

from pydantic import BaseModel, Field, AwareDatetime


class PurchaseSchema(BaseModel):
    """Модель записи покупки из базы данных.

    Attributes
    ----------
    id : UUID
        Идентификатор покупки.
    employee_id : UUID
        UUID сотрудника, совершившего покупку.
    merch_item_id : UUID
        UUID купленного продукта.
    date : AwareDatetime
        Дата покупки.
    """

    id: UUID = Field(examples=["7e4a71df-6f79-4ad7-a102-ec7714f9ddb8"])
    employee_id: UUID = Field(examples=["7e4a71df-6f79-4ad7-a102-ec7714f9ddb8"])
    merch_item_id: UUID = Field(examples=["7e4a71df-6f79-4ad7-a102-ec7714f9ddb8"])
    date: AwareDatetime = Field(examples=["2025-04-03 20:25:41.972274+03"])
