from typing import Dict, Optional, List

from fastapi import APIRouter, HTTPException, status, Query, Depends

from app.utils import get_api_all_currencies, get_api_latest, convert_rates, PermissionChecker
from app.api.schemas import Currency, CurrencyConversion
from app.core import get_role_from_token


router = APIRouter()

@router.get("/all", response_model=Dict[str, Currency], 
            summary="Получить список всех валют с дополнительной информацией",
            dependencies=[Depends(PermissionChecker(["guest", "user", "admin"]))])
async def all_currencies(user_role = Depends(get_role_from_token)):
    try:
        return await get_api_all_currencies()
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))
    
@router.get("/convert", response_model=List[CurrencyConversion], 
            summary="Конвертация валют", 
            dependencies=[Depends(PermissionChecker(["user", "admin"]))] )
async def convert_currency(
    user_role = Depends(get_role_from_token),
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
    