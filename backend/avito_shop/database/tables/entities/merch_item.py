from typing import List, TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import PrimaryKeyConstraint, func
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.types import Float, String, Uuid

from database.tables.base import Base

if TYPE_CHECKING:
    from database.tables.junctions import Purchase


class MerchItem(Base):
    __tablename__ = "merch_item"

    __table_args__ = (
        PrimaryKeyConstraint("id", name="merch_item_pkey"),
        {
            "comment": "Таблица записей о продуктах.",
        },
    )

    id: Mapped[UUID] = mapped_column(Uuid(), default=uuid4)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    price: Mapped[float] = mapped_column(Float(), nullable=False)

    purchases: Mapped[List["Purchase"]] = relationship(
        "Purchase", back_populates="merch_item"
    )

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id!r}, "
            f"name={self.name!r}, "
            f"price={self.price!r}"
            f")>"
        )
