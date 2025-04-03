from pydantic import Field

from .standard import StandardResponse


class TokenResponse(StandardResponse):
    """Модель ответа сервера с вложенной парой JWT.

    Используется в качестве ответа с сервера на запрос на авторизацию.

    Attributes
    ----------
    access_token : str
        JSON Web Token, токен доступа.
    refresh_token : str
        JSON Web Token, токен обновления.
    token_type : str
        Тип возвращаемого токена.
    """

    access_token: str = Field(
        examples=[
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
            ".eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ"  # noqa
            ".SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
        ]
    )  # noqa
    refresh_token: str = Field(
        examples=[
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
            ".eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ"  # noqa
            ".SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
        ]
    )  # noqa
    token_type: str = Field(examples=["bearer"])
