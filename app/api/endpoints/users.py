from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas import UserRequest, UserDatabase
from app.db.db_utils import get_user, add_new_user
from app.db import get_db
from app.utils import is_verify_password
from app.core import create_token


router = APIRouter()

@router.post('/register', summary="Регистрация нового пользователя")
async def register(user: UserRequest, db: AsyncSession = Depends(get_db)):
    user_db: Optional[UserDatabase] = await get_user(db, user.username)
    
    if user_db is None:
        await add_new_user(db, user.username, user.password)
        return {"Сообщение": 'Пользователь успешно добавлен'}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Неправильный пароль или никнейм')

@router.post('/login', summary="Авторизация пользователя")
async def login(user: UserRequest, response: Response, db: AsyncSession = Depends(get_db)):
    user_db: Optional[UserDatabase] = await get_user(db, user.username)

    if user_db and is_verify_password(user.password, user_db.hashed_password):
        token = create_token(data={'sub': user.username})
        response.set_cookie(key='currency_token', value=token, httponly=True)
        return {"Сообщение": 'Пользователь успешно авторизирован'}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Неправильный пароль или никнейм')