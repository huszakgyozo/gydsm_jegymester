from __future__ import annotations

from app.extensions import db
from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String


class Role(db.Model):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(primary_key=True)
    rolename: Mapped[str] = mapped_column(String(50), unique=True)

    users: Mapped[List["User"]] = relationship(
        secondary="userroles",
        back_populates="roles"
    )