from typing import List

from fastapi import HTTPException, status, Request


def permission_checker(allowed_roles: List[str]):

    async def checker(request : Request):
        from app.core.security import get_role_from_token
        from app.utils import logger
        user_role: str = await get_role_from_token(request)

        logger.info("Обращение к PermissionChecker")
        if not user_role:
            logger.warning("Не найден user_role пользователя")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Неавторизован"
            )
        if user_role == "admin":
            logger.info("Найден user_role администратора")
            return user_role
        if user_role not in allowed_roles:
            logger.warning("Не найден user_role пользователя в позволенных")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав"
            )
        return user_role

    return checker
