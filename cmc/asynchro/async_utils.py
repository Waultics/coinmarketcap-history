from cmc.utils import utils

from functools import partial

# for asynchronous requests to coinmarketcap
import asyncio
import aiohttp
import requests

#------------------------------------------- Asynchronous Functionality -------------------------------------------------------
@asyncio.coroutine
async def fetch_url(session, url):
    async with session.get(url, timeout=60 * 60) as response:
        return await response.read()

async def fetch_all_urls(session, urls, loop):
    results = await asyncio.gather(*[fetch_url(session, url) for url in urls],
    return_exceptions=True)
    return results

def get_htmls(cryptocurrencies, start_date, end_date):
    if len(cryptocurrencies) == 0: return {}

    # create url constructor partial
    url_func = partial(utils.craft_url, start_date = start_date, end_date = end_date)
    urls = [url_func(crypto) for crypto in cryptocurrencies]

    if len(urls) > 0:
        loop = asyncio.get_event_loop()
        connector = aiohttp.TCPConnector(limit=100)
        session = aiohttp.ClientSession(loop=loop, connector=connector)
        htmls = loop.run_until_complete(fetch_all_urls(session, urls, loop))
        connector.close()
        raw_result = dict(zip(cryptocurrencies, htmls))

    return raw_result
