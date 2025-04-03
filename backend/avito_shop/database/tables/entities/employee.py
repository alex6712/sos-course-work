from typing import List, TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import PrimaryKeyConstraint, UniqueConstraint, func
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.types import String, Uuid, Float

from database.tables.base import Base
from database.tables.junctions import Transfer

if TYPE_CHECKING:  # данных блок необходим для избежания цикличного импорта
    from database.tables.entities import MerchItem
    from database.tables.junctions import Purchase


class Employee(Base):
    __tablename__ = "employee"

    __table_args__ = (
        PrimaryKeyConstraint("id", name="employee_pkey"),
        UniqueConstraint("username", name="employee_username_uk"),
        UniqueConstraint("email", name="employee_email_uk"),
        UniqueConstraint("phone", name="employee_phone_uk"),
        {
            "comment": "Таблица записей о сотрудниках.",
        },
    )

    id: Mapped[UUID] = mapped_column(Uuid(), default=uuid4)
    username: Mapped[str] = mapped_column(String(256))
    password: Mapped[str] = mapped_column(String(256))
    email: Mapped[str] = mapped_column(String(256), nullable=True)
    phone: Mapped[str] = mapped_column(String(256), nullable=True)
    coins_amount: Mapped[float] = mapped_column(Float(), nullable=False)
    refresh_token: Mapped[str] = mapped_column(
        String(256), nullable=True, comment="Токен обновления токена доступа."
    )

    purchases: Mapped[List["Purchase"]] = relationship(
        "Purchase", back_populates="employee"
    )

    bought_items: Mapped[List["MerchItem"]] = relationship(
        "MerchItem",
        secondary="purchase",
        viewonly=True,
    )

    sent_transfers: Mapped[List["Transfer"]] = relationship(
        "Transfer",
        foreign_keys=[Transfer.sender_id],
        back_populates="sender",
        order_by=Transfer.date,
    )

    gained_transfers: Mapped[List["Transfer"]] = relationship(
        "Transfer",
        foreign_keys=[Transfer.gainer_id],
        back_populates="gainer",
        order_by=Transfer.date,
    )

    @property
    def all_transfers(self) -> List["Transfer"]:
        """Объединяет входящие и исходящие транзакции, сортируя их по времени

        Returns
        -------
        transfers : List[Transfer]
            Объединённый список входящих и исходящих транзакций,
            отсортированный по времени совершения транзакции.
        """
        return sorted(
            self.sent_transfers + self.gained_transfers,
            key=lambda transfer: transfer.date,
        )

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id!r}, "
            f"username={self.username!r}, "
            f"password={self.password!r}, "
            f"email={self.email!r}, "
            f"phone={self.phone!r}, "
            f"refresh_token={self.refresh_token!r}"
            f")>"
        )
