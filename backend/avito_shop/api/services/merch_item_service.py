from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.tables.entities import MerchItem


async def get_merch_item_by_id(session: AsyncSession, id_: UUID) -> MerchItem:
    """Возвращает модель продукта для дальнейшей обработки.

    Parameters
    ----------
    session : AsyncSession
        Объект сессии запроса.
    id_ : UUID
        UUID продукта.

    Returns
    -------
    merch_item : MerchItem
        Модель записи продукта из базы данных.
    """
    return await session.scalar(select(MerchItem).where(MerchItem.id == id_))
