from __future__ import annotations

from app.extensions import db
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String
from sqlalchemy import ForeignKey


class TicketOrder(db.Model):
    __tablename__ = "ticketorders"
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), primary_key=True)
    ticket_id: Mapped[int] = mapped_column(ForeignKey("tickets.id"), primary_key=True)
    ticket_status: Mapped[str] = mapped_column(String(20), nullable=False, default="aktív")

    order: Mapped["Order"] = relationship(back_populates="tickets")
    ticket: Mapped["Ticket"] = relationship()  # Optional, depending on your needs