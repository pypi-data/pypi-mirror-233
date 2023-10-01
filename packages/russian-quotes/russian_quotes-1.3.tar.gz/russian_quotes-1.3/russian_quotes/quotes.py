import aiohttp
from . import exceptions
import asyncio


async def get_quote() -> tuple:
    """
    Get random quote on russian from forismatic API.

    Returns:
        [tuple]: Tuple of quote.
            Contains:
                - quote text
                - quote author

    Raises:
        ServerError:
            Returns when server status isn`t 200.
    """
    async def fetch_quote():
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.forismatic.com/api/1.0/?method=getQuote&format=json&json=?') as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    raise exceptions.ServerError(f'Server isn`t responding. Status code: {response.status}')

    quote_data = loop.run_until_complete(fetch_quote())
    return quote_data['quoteText'], quote_data['quoteAuthor'] or 'Неизвестный автор'
