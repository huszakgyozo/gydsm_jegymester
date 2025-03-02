from __future__ import annotations

from app.extensions import db
from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String


class Theater(db.Model):
    __tablename__ = "theaters"
    id: Mapped[int] = mapped_column(primary_key=True)
    theatname: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    seats: Mapped[List["Seat"]] = relationship(back_populates="theater")
    screenings: Mapped[List["Screening"]] = relationship(back_populates="theater")