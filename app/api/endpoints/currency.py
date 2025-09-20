from typing import Dict, Optional, List

from fastapi import APIRouter, HTTPException, status, Query, Depends

from app.utils import get_api_all_currencies, get_api_latest, convert_rates, PermissionChecker, LimitChecker
from app.api.schemas import Currency, CurrencyConversion
from app.core import get_role_from_token



router = APIRouter()

role_limits = {"admin": 10, "user": 5, "guest": 1}
@router.get(
    "/all",
    response_model=Dict[str, Currency],
    summary="Получить список всех валют с дополнительной информацией",
    dependencies=[
        Depends(PermissionChecker(["guest", "user", "admin"])),
        Depends(LimitChecker(role_limits))
    ]
)
async def all_currencies():
    return await get_api_all_currencies()


@router.get(
    "/convert",
    response_model=List[CurrencyConversion],
    summary="Конвертация валют",
    dependencies=[
        Depends(PermissionChecker(["user", "admin"])),
        Depends(LimitChecker(role_limits))
    ]
)
async def convert_currency(
    from_currency: str = Query("USD", alias="from"),
    to_currency: Optional[str] = Query(None, alias="to"),
    amount: float = 1
):
    data = await get_api_latest(from_currency)
    rates: Dict[str, float] = data.get("data", {})
    if not rates:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка получения курсов валют")
    return convert_rates(from_currency, rates, amount, to_currency)