from __future__ import annotations
import enum
from app.extensions import db
from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String


class StatusEnum(enum.Enum):
    Pending = 0
    Successful = 1
    Canceled = 2


class Order(db.Model):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    payment_status: Mapped[StatusEnum] = mapped_column()

    tickets: Mapped[List["TicketOrder"]] = relationship(back_populates="order")