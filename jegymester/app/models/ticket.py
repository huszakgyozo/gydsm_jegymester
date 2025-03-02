﻿from __future__ import annotations

from app.extensions import db
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String
from sqlalchemy import ForeignKey


class Ticket(db.Model):
    __tablename__ = "tickets"
    id: Mapped[int] = mapped_column(primary_key=True)
    screening_id: Mapped[int] = mapped_column(ForeignKey("screenings.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    ticketcategory_id: Mapped[int] = mapped_column(ForeignKey("ticketcategories.id"), nullable=False)

    screening: Mapped["Screening"] = relationship(back_populates="tickets")
    user: Mapped["User"] = relationship(back_populates="tickets")
    ticketcategory: Mapped["TicketCategory"] = relationship(back_populates="tickets")