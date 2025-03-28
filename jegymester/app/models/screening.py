﻿from __future__ import annotations

from app.extensions import db
from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import DateTime
from sqlalchemy import ForeignKey
from datetime import datetime


class Screening(db.Model):
    __tablename__ = "screenings"
    id: Mapped[int] = mapped_column(primary_key=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"))
    theater_id: Mapped[int] = mapped_column(ForeignKey("theaters.id"))
    start_time: Mapped[datetime] = mapped_column(DateTime)
    deleted : Mapped[bool] = mapped_column(default = False)

    movie: Mapped["Movie"] = relationship(back_populates="screenings")
    theater: Mapped["Theater"] = relationship(back_populates="screenings")
    tickets: Mapped[List["Ticket"]] = relationship(back_populates="screening")