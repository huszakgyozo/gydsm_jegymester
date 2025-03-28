﻿from __future__ import annotations

from app.extensions import db
from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String, Integer


class Movie(db.Model):
    __tablename__ = "movies"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), unique=True)
    duration: Mapped[int] = mapped_column(Integer)
    genre: Mapped[str] = mapped_column(String(50))
    age_limit: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(String(500))
    deleted : Mapped[bool] = mapped_column(default = False)

    screenings: Mapped[List["Screening"]] = relationship(back_populates="movie")