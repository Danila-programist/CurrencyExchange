from typing import List

from fastapi import Depends, HTTPException, status

from app.core.security import get_role_from_token 

def PermissionChecker(allowed_roles: List[str]):
    async def checker(user_role: str = Depends(get_role_from_token)):
        if not user_role:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неавторизован"
            )

        if user_role == "admin":
            return user_role

        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав"
            )

        return user_role

    return checker
