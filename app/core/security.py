import datetime
from typing import Dict, Optional

import jwt
from fastapi import Request, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import settings
from app.api.schemas import UserDatabase
from app.db.db_utils import get_user, get_role
from app.db import get_db
from app.utils import logger

def create_token(data: Optional[Dict[str, str]]) -> str:
    logger.info('Создание нового токена')
    payload: Dict = dict()
    payload.update(data)
    payload['exp'] = datetime.datetime.now() + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(payload=payload, key=settings.SECRET, algorithm=settings.ALGORYTHM)

async def get_role_from_token(request: Request, db: AsyncSession = Depends(get_db)) -> str:
    logger.info('Получение роли из токена')
    token = request.cookies.get('currency_token')

    if not token:
        logger.info('Токен не найден, поэтому пользователь является гостем')
        return 'guest'
    
    try:
        logger.info('Декодирование токена')
        payload: Dict = jwt.decode(token, key=settings.SECRET, algorithms=settings.ALGORYTHM)
        user: Optional[UserDatabase] = await get_user(db, payload.get('sub'))

        if user is None:
            logger.warning('Пользователь с никнеймом не найден')
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Неверный токен')


        return await get_role(db, user.username)
    except jwt.ExpiredSignatureError:
        logger.warning('Неверная сигнатура токена')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Неверный токен')
    except jwt.InvalidSignatureError:
        logger.warning('Просроченный токен')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Неверный токен')
    
