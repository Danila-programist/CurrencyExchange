from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core import settings


engine = create_async_engine(settings.ASYNC_DATABASE_DSN)

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    from app.utils import logger
    async with async_session() as session:
        logger.info('Получение новой транзакции к базе данных')
        try:
            yield session
        finally:
            logger.info('Закрытие транзакции к базе данных')
            await session.close()