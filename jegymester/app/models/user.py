﻿from __future__ import annotations

from app.extensions import db
from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String


class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(256))  # For hashed passwords

    roles: Mapped[List["Role"]] = relationship(
        secondary="userroles",
        back_populates="users"
    )
    tickets: Mapped[List["Ticket"]] = relationship(back_populates="user")

    def set_password(self, password: str) -> None:
        # Placeholder for password hashing (implement with a library like Werkzeug)
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)

