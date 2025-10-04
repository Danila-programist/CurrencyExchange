from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from .base import Base


class Users(Base):  # pylint: disable=too-few-public-methods
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(16), nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(nullable=False, server_default="user")
