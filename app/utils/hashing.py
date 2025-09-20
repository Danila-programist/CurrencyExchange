from passlib.context import CryptContext

from app.core import settings
from app.utils import logger

pwd_context = CryptContext(schemes=[settings.PWD_ALGORYTHM], deprecated="auto")

def hash_password(password: str) -> str:
    logger.info('Хэширование пароля')
    return pwd_context.hash(password)

def is_verify_password(plain_password: str, hashed_password: str) -> bool:
    logger.info('Верификация пароля')
    return pwd_context.verify(plain_password, hashed_password)
