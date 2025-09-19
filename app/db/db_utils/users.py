from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models import Users
from app.api.schemas import UserDatabase

async def get_user(db: AsyncSession, username: str) -> Optional[UserDatabase]:
    stmt = select(Users).where(Users.username == username)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def add_new_user(db: AsyncSession, username: str, password: str, role: str = "user") -> None:
    new_user: Users = Users(
        username=username,
        hashed_password=password,  
        role=role
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)  