import datetime
from typing import Dict, Optional

import jwt
from fastapi import Request, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import settings
from app.api.schemas import UserDatabase
from app.db.db_utils import get_user, get_role
from app.db import get_db

def create_token(data: Optional[Dict[str, str]]) -> str:
    payload: Dict = dict()
    payload.update(data)
    payload['exp'] = datetime.datetime.now() + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(payload=payload, key=settings.SECRET, algorithm=settings.ALGORYTHM)

async def get_role_from_token(request: Request, db: AsyncSession = Depends(get_db)) -> str:
    token = request.cookies.get('currency_token')

    if not token:
        return 'guest'
    
    try:
        payload: Dict = jwt.decode(token, key=settings.SECRET, algorithms=settings.ALGORYTHM)
        user: Optional[UserDatabase] = await get_user(db, payload.get('sub'))

        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Неверный токен')


        return await get_role(db, user.username)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Неверный токен')
    except jwt.InvalidSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Неверный токен')
    
