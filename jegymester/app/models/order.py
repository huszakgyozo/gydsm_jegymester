﻿from __future__ import annotations
import enum
from app.extensions import db
from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String


class StatusEnum(enum.Enum):
    Pending = 0
    Successful = 1
    Canceled = 2

    @staticmethod
    def validate(value):
        if isinstance(value, str):
            if value not in StatusEnum.__members__:
                raise ValueError(f"Nem megfelelő payment_status: {value}. Elfogadott: {', '.join([e.name for e in StatusEnum])}")
            return StatusEnum[value]
        raise ValueError(f"Nem megfelelő payment_status: {value}. Elfogadott: {', '.join([e.name for e in StatusEnum])}")

class Order(db.Model):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    payment_status: Mapped[StatusEnum] = mapped_column()
    deleted: Mapped[bool] = mapped_column(default=False)

    tickets: Mapped[List["TicketOrder"]] = relationship(back_populates="order")