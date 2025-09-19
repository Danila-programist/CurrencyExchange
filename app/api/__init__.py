from fastapi import APIRouter
from app.api.endpoints import currency # users

api_router = APIRouter(prefix="/api/v1") 

api_router.include_router(currency.router, prefix="/currency", tags=["currency"])
#api_router.include_router(users.router, prefix="/users", tags=["users"])