from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass


from .users import Users 

__all__ = [
    "Base",
    "Users"
]