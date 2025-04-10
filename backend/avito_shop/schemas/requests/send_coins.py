from pydantic import BaseModel, Field


class SendCoinsRequest(BaseModel):
    """Схема запроса на перевод монет.

    Используется в качестве схемы тела POST запроса ``api/transactions/send_coins``.

    Attributes
    ----------
    gainer_username : str
        Имя пользователя сотрудника-получателя.
    coins_amount : float
        Количество монет для перевода.
    """

    gainer_username: str = Field(examples=["someone"])
    coins_amount: float = Field(examples=[100.0])
