from typing import TYPE_CHECKING
from uuid import UUID, uuid4
from datetime import datetime, timezone

from sqlalchemy import ForeignKeyConstraint, PrimaryKeyConstraint, func
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.types import Uuid, Float, DateTime

from database.tables.base import Base

if TYPE_CHECKING:
    from database.tables.entities import Employee


class Transaction(Base):
    __tablename__ = "transaction"

    __table_args__ = (
        PrimaryKeyConstraint("id", name="transaction_pkey"),
        ForeignKeyConstraint(
            ["sender_id"],
            ["employee.id"],
            name="transaction_sender_id_fk",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["gainer_id"],
            ["employee.id"],
            name="transaction_gainer_id_fk",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        {
            "comment": "Таблица с записями о переводах монет.",
        },
    )

    id: Mapped[UUID] = mapped_column(Uuid(), default=uuid4)
    sender_id: Mapped[UUID] = mapped_column(Uuid())
    gainer_id: Mapped[UUID] = mapped_column(Uuid())
    amount: Mapped[float] = mapped_column(Float(), nullable=False)
    date: Mapped[datetime] = mapped_column(
        DateTime(), default=lambda: datetime.now(timezone.utc)
    )

    sender: Mapped["Employee"] = relationship(
        "Employee",
        foreign_keys=[sender_id],
        back_populates="sent_transactions",
    )

    gainer: Mapped["Employee"] = relationship(
        "Employee",
        foreign_keys=[gainer_id],
        back_populates="gained_transactions",
    )

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id!r}, "
            f"sender_id={self.sender_id!r}, "
            f"gainer_id={self.gainer_id!r}, "
            f"amount={self.amount!r}"
            f")>"
        )
