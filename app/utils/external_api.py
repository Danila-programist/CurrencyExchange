import aiohttp

from app.core import settings

async def get_api_all_currencies():
    """
    Получить список всех доступных валют с их названиями на английском языке.

    Эта функция делает асинхронный HTTPS-запрос к CurrencyAPI
    (endpoint /currencies) и возвращает спикок 

    Пример результата:
    {
        "USD",
        "EUR", 
        "JPY",
        ...
    }
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{settings.BASE_URL}/currencies", params={"apikey": settings.CURRENCY_API_KEY}) as response:
            response.raise_for_status()
            data = await response.json()
            return list(data['data'].keys())