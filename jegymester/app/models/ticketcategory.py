from __future__ import annotations

from app.extensions import db
from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String, Integer


class TicketCategory(db.Model):
    __tablename__ = "ticketcategories"
    id: Mapped[int] = mapped_column(primary_key=True)
    catname: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)

    tickets: Mapped[List["Ticket"]] = relationship(back_populates="ticketcategory")