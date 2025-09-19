from typing import Dict

from fastapi import APIRouter, HTTPException, status

from app.utils import get_api_all_currencies
from app.api.schemas import Currency


router = APIRouter()

@router.get("/all", response_model=Dict[str, Currency], summary="Получить список всех валют с дополнительной информацией")
async def all_currencies():
    try:
        return await get_api_all_currencies()
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))