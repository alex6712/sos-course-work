from uuid import UUID

from pydantic import BaseModel, Field


class SendCoinsRequest(BaseModel):
    """Схема запроса на перевод монет.

    Используется в качестве схемы тела POST запроса ``api/transactions/send_coins``.

    Attributes
    ----------
    gainer_id : UUID
        UUID сотрудника-получателя.
    coins_amount : float
        Количество монет для перевода.
    """

    gainer_id: UUID = Field(examples=["cb5639aa-3855-4f0b-a92b-6729890b6085"])
    coins_amount: float = Field(examples=[100.0])
