from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.schemas import UserRequest, UserDatabase
from app.db.db_utils import get_user, add_new_user
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db


router = APIRouter()

@router.post('/register')
async def register(user: UserRequest, db: AsyncSession = Depends(get_db)):
    user_db: Optional[UserDatabase] = await get_user(db, user.username)
    
    if user_db is None:
        await add_new_user(db, user.username, user.password)
        return {"Сообщение": 'Пользователь успешно добавлен'}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Неправильный пароль или никнейм')

@router.post('/login')
async def login(user: UserRequest, db: AsyncSession = Depends(get_db)):
    user_db: Optional[UserDatabase] = await get_user(db, user.username)

    if user_db:
        return {"Сообщение": 'Пользователь успешно авторизирован'}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Неправильный пароль или никнейм')