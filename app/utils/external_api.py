import aiohttp

from app.core import settings

async def get_api_all_currencies():
    """
    Получить список всех доступных валют с их названиями на английском языке 
    и дополнительной информацией.

    Эта функция делает асинхронный HTTPS-запрос к CurrencyAPI
    (endpoint /currencies) и возвращает список словарей с ключом - название 
    валюты и в качестве ключа - 

    Пример результата:
    {
        "AED": {
            "symbol": "AED",
            "name": "United Arab Emirates Dirham",
            "symbol_native": "د.إ",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "AED",
            "name_plural": "UAE dirhams",
            "type": "fiat",
            "countries": [
                "AE"
            ]
        },
        ...
    }
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{settings.BASE_URL}/currencies", params={"apikey": settings.CURRENCY_API_KEY}) as response:
            response.raise_for_status()
            data = await response.json()
            return data['data']