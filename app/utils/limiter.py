from typing import Dict

from fastapi import Depends, HTTPException, status
from fastapi_limiter.depends import RateLimiter

from app.core.security import get_role_from_token  

def LimitChecker(limits: Dict[str, int], user_role: str = Depends(get_role_from_token)):
    if not user_role:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неавторизован")


    if user_role not in limits:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Лимитер не найден")

    times_per_minute = limits[user_role]

    return RateLimiter(times=times_per_minute, minutes=1)