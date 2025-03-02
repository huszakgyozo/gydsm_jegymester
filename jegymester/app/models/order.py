from __future__ import annotations

from app.extensions import db
from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String


class Order(db.Model):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    payment_status: Mapped[str] = mapped_column(String(20), nullable=False, default="Pending")

    tickets: Mapped[List["TicketOrder"]] = relationship(back_populates="order")