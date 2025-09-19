import datetime
from typing import Dict, Optional

import jwt

from app.core import settings

def create_token(data: Optional[Dict[str, str]]) -> str:
    payload: Dict = dict()
    payload.update(data)
    payload['exp'] = datetime.datetime.now() + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(payload=payload, key=settings.SECRET, algorithm=settings.ALGORYTHM)
