from pydantic import BaseModel, EmailStr, Field
from pydantic_extra_types.phone_numbers import PhoneNumber


class SignUpRequest(BaseModel):
    """Схема объекта сотрудника с паролем.

    Используется в качестве представления информации о сотруднике, включая его пароль.

    Attributes
    ----------
    username : str
        Логин сотрудника.
    email : EmailStr
        Адрес электронной почты сотрудника.
    phone : PhoneNumber
        Номер мобильного телефона сотрудника.
    password : str
        Пароль сотрудника.
    """

    username: str = Field(examples=["someone"])
    email: EmailStr = Field(default=None, examples=["someone@post.domen"])
    phone: PhoneNumber = Field(default=None, examples=["+7 900 000-00-00"])
    password: str = Field(examples=["password"])
