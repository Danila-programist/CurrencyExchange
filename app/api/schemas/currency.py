from pydantic import BaseModel


class Currency(BaseModel):
    symbol: str
    name: str
    symbol_native: str
    decimal_digits: int
    rounding: int
    code: str
    name_plural: str
    type: str
    countries: list[str]


class CurrencyConversion(BaseModel):
    from_currency: str
    to_currency: str
    rate: float
    amount: float
    converted_amount: float
