from typing import Dict, List, Optional

from fastapi import HTTPException, status

from app.api.schemas import CurrencyConversion


def convert_rates(
    from_currency: str,
    rates: Dict[str, float],
    amount: float = 1,
    to_currency: Optional[str] = None
) -> List[CurrencyConversion]:
    """
    Конвертирует сумму `amount` из `from_currency` в одну или все валюты из `rates`.
    Если `to_currency` указан — возвращает только выбранную валюту.
    """
    results = []

    if to_currency:
        if to_currency not in rates:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Валюта {to_currency} не найдена")
        rate = rates[to_currency]["value"] 
        results.append(CurrencyConversion(
            from_currency=from_currency,
            to_currency=to_currency,
            rate=rate,
            amount=amount,
            converted_amount=amount * rate
        ))
    else:

        for code, rate in rates.items():
            rate_value = rate["value"]
            results.append(CurrencyConversion(
                from_currency=from_currency,
                to_currency=code,
                rate=rate_value,
                amount=amount,
                converted_amount=amount * rate_value
            ))

    return results