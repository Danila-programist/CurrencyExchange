from fastapi import APIRouter, HTTPException, status

from app.utils import get_api_all_currencies

router = APIRouter()

@router.get('/all')
async def get_all_currencies():
    try:
        all_currencies = await get_api_all_currencies()
        return all_currencies
    except Exception as exp:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ошибка при получении валют: {exp}")