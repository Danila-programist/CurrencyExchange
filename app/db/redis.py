from fastapi import FastAPI
from contextlib import asynccontextmanager
import redis.asyncio as redis
from fastapi_limiter import FastAPILimiter

from app.core import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
    await FastAPILimiter.init(redis_client)

    yield  

    await redis_client.close()
    await redis_client.connection_pool.disconnect()