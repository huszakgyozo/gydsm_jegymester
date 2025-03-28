from __future__ import annotations

from app.extensions import db
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String
from sqlalchemy import ForeignKey


class Ticket(db.Model):
    __tablename__ = "tickets"
    id: Mapped[int] = mapped_column(primary_key=True)
    screening_id: Mapped[int] = mapped_column(ForeignKey("screenings.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    ticketcategory_id: Mapped[int] = mapped_column(ForeignKey("ticketcategories.id"))
    seat_id: Mapped[int] = mapped_column(ForeignKey("seats.id"))

    screening: Mapped["Screening"] = relationship(back_populates="tickets")
    user: Mapped["User"] = relationship(back_populates="tickets")
    ticketcategory: Mapped["TicketCategory"] = relationship(back_populates="tickets")
    seat: Mapped["Seat"] = relationship("Seat", back_populates="tickets")
    ticket_orders: Mapped[list["TicketOrder"]] = relationship(back_populates="ticket")