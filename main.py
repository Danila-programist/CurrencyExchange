import uvicorn
from fastapi import FastAPI

from app.api import api_router
from app.db import lifespan
from app.utils import logger

app = FastAPI(title="Currency Exchange API", lifespan=lifespan)

app.include_router(api_router)

if __name__ == '__main__':
    logger.info('Запуск ASGI uvicorn')
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)