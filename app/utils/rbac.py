from functools import wraps
from typing import List, Callable, Optional

from fastapi import HTTPException, status

class PermissionChecker:
    def __init__(self, roles = List[str]):
        self.roles = roles

    def __call__(self, func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user_role: Optional[str] = kwargs.get('user_role')

            if 'admin' in user_role:
                return await func(*args, **kwargs)

            if not user_role in self.roles:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Permission denied')

            return await func(*args, **kwargs)

        return wrapper