import uvicorn
from fastapi import FastAPI

from app.api import api_router
from app.db import lifespan

app = FastAPI(title="Currency Exchange API", lifespan=lifespan)

app.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)