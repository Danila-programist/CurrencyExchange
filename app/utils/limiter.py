from typing import Dict

from fastapi import Depends, HTTPException, status, Request, Response
from fastapi_limiter.depends import RateLimiter

from app.core.security import get_role_from_token  

def LimitChecker(limits: Dict[str, int]):
    async def dependency(
        request: Request,
        response: Response,
        user_role: str = Depends(get_role_from_token)
    ):
        if not user_role:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неавторизован")
        if user_role not in limits:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Лимитер не найден")

        limiter = RateLimiter(times=limits[user_role], minutes=1)
        await limiter(request, response)  
        return user_role

    return dependency