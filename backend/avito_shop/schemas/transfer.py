from uuid import UUID

from pydantic import BaseModel, Field, AwareDatetime


class TransferSchema(BaseModel):
    """Модель записи перевода из базы данных.

    Attributes
    ----------
    id : UUID
        Идентификатор перевода.
    sender_id : UUID
        UUID сотрудника-отправителя.
    gainer_id : UUID
        UUID сотрудника-получателя.
    date : AwareDatetime
        Дата перевода.
    """

    id: UUID = Field(examples=["7e4a71df-6f79-4ad7-a102-ec7714f9ddb8"])
    sender_id: UUID = Field(examples=["7e4a71df-6f79-4ad7-a102-ec7714f9ddb8"])
    gainer_id: UUID = Field(examples=["7e4a71df-6f79-4ad7-a102-ec7714f9ddb8"])
    date: AwareDatetime = Field(examples=["2025-04-03 20:25:41.972274+03"])
