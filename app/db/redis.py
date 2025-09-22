from fastapi import FastAPI
from contextlib import asynccontextmanager
import redis.asyncio as redis
from fastapi_limiter import FastAPILimiter

from app.core import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.utils import logger

    logger.info("Подключение Redis")
    redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
    logger.info("Инициализация Limiter")
    await FastAPILimiter.init(redis_client)

    yield
    logger.info("Отключение Redis")
    await redis_client.close()
    await redis_client.connection_pool.disconnect()
