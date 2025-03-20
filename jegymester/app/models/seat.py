from __future__ import annotations

from app.extensions import db
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String
from sqlalchemy import ForeignKey
from sqlalchemy import Boolean

class Seat(db.Model):
    __tablename__ = "seats"
    id: Mapped[int] = mapped_column(primary_key=True)
    theater_id: Mapped[int] = mapped_column(ForeignKey("theaters.id"), nullable=False)
    seat_number: Mapped[str] = mapped_column(String(10), nullable=False)
    reserved: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    theater: Mapped["Theater"] = relationship(back_populates="seats")
    tickets: Mapped[list["Ticket"]] = relationship("Ticket", back_populates="seat") 