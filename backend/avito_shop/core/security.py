from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_(
    secret: str | bytes, scheme: str = None, category: str = None, **kwargs
) -> str:
    """Прокси для метода ``CriptContext.hash()``.

    Получает параметры, необходимые для выполнения хеширования, и возвращает результат.

    Parameters
    ----------
    secret : str or bytes
        Пароль для хеширования.
    scheme : str or bytes, optional
        Схема, по которой хеширование будет выполнено. Необязательный аргумент.
        Если не передан, используется схема по умолчанию.

        .. deprecated:: 1.7
            Поддержка этого ключевого слова устарела и будет удалена в PassLib 2.0.
    category : str, optional
        Если передано, то любые значения по умолчанию, связанные с категорией
        будут изменены на значения по умолчанию для этой категории.

    Returns
    -------
    hashed : str or bytes
        Хеш пароля в соответствии с установленной схемой и настройками.
    """
    return pwd_context.hash(secret, scheme, category, **kwargs)


def verify(
    secret: str | bytes,
    hashed: str | bytes,
    scheme: str = None,
    category: str = None,
    **kwargs
) -> bool:
    """Прокси для метода ``CriptContext.verify()``.

    Проверяет переданный пароль на соответствие хешу.

    Parameters
    ----------
    secret : str or bytes
        Пароль для проверки.
    hashed : str or bytes
        Хеш пароля.
    scheme : str or bytes, optional
        Схема, по которой хеширование будет выполнено. Необязательный аргумент.
        Если не передан, используется схема по умолчанию.

        .. deprecated:: 1.7
            Поддержка этого ключевого слова устарела и будет удалена в PassLib 2.0.
    category : str, optional
        Если передано, то любые значения по умолчанию, связанные с категорией
        будут изменены на значения по умолчанию для этой категории.

    Returns
    -------
    equality : bool
        ``True``, если хеш пароля соответствует переданному паролю, в ином случае ``False``.
    """
    return pwd_context.verify(secret, hashed, scheme, category, **kwargs)
