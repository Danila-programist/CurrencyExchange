from typing import Dict, Optional, List

from fastapi import APIRouter, HTTPException, status, Query

from app.utils import get_api_all_currencies, get_api_latest, convert_rates
from app.api.schemas import Currency, CurrencyConversion


router = APIRouter()

@router.get("/all", response_model=Dict[str, Currency], summary="Получить список всех валют с дополнительной информацией")
async def all_currencies():
    try:
        return await get_api_all_currencies()
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))
    
@router.get("/convert", response_model=List[CurrencyConversion] ,summary="Конвертация валют")
async def convert_currency(
    from_currency: str = Query("USD", alias="from"),
    to_currency: Optional[str] = Query(None, alias="to"),
    amount: float = 1
):
    try:
        data = await get_api_latest(from_currency)
        rates: Dict[str, float] = data.get("data", {})

        if not rates:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка получения курсов валют")

        return convert_rates(from_currency, rates, amount, to_currency)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))
    