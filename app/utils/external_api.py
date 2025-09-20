import aiohttp

from app.core import settings
from app.utils import logger

async def get_api_all_currencies():
    """
    Получить список всех доступных валют с их названиями на английском языке 
    и дополнительной информацией.

    Эта функция делает асинхронный HTTPS-запрос к CurrencyAPI
    (endpoint /currencies) и возвращает список словарей с ключом - название 
    валюты и в качестве значения - список словарей

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
        logger.info('Подключение aiohttp сессии')
        async with session.get(f"{settings.BASE_URL}/currencies", params={"apikey": settings.CURRENCY_API_KEY}) as response:
            logger.info('Получение get-запроса к внешнему API')
            response.raise_for_status()
            data = await response.json()
            return data['data']
        logger.warning('Не получилось подключиться к внешнему API')
    logger.warning('Не получили подключение к сессии')
        

async def get_api_latest(from_currency: str):
    """
    Получить список всех доступных конвертирующих валют от базовой с их
    значением кодов и относительной стоимостью от базовой, а также время последненего изменения.

    Эта функция делает асинхронный HTTPS-запрос к CurrencyAPI
    (endpoint /currencies) и возвращает следующий результат.

    Пример результата:
    {
    "meta": {
        "last_updated_at": "2023-06-23T10:15:59Z"
    },
    "data": {
        "AED": {
            "code": "AED",
            "value": 3.67306
        },
        "AFN": {
            "code": "AFN",
            "value": 91.80254
        },
        "ALL": {
            "code": "ALL",
            "value": 108.22904
        },
        "AMD": {
            "code": "AMD",
            "value": 480.41659
        },
        "...": "150+ more currencies"
    }
}
    """
    async with aiohttp.ClientSession() as session:
        logger.info('Подключение aiohttp сессии')
        params = {"apikey": settings.CURRENCY_API_KEY, "base": from_currency}
        logger.info('Подключение параметров для aiohttp')
        async with session.get(f"{settings.BASE_URL}/latest", params=params) as response:
            logger.info('Получение get-запроса к внешнему API')
            response.raise_for_status()
            return await response.json()
        logger.warning('Не получилось подключиться к внешнему API')
    logger.warning('Не получили подключение к сессии')