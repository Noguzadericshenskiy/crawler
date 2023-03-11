import asyncio
import aiohttp
import aiofiles

from loguru import logger

from bs4 import BeautifulSoup


URL = "https://www.klenmarket.ru"
DEPTH = 2


async def get_link(client: aiohttp.ClientSession, url: str, depth: int = DEPTH) -> None:
    async with client.get(url) as response:
        try:
            result = await response.text()
            soup = BeautifulSoup(result, 'html.parser')

            for link in soup.find_all('a'):
                link_str = link.get('href')
                logger.info(f'depth-{depth}, link-{link_str}')
                if link_str is not None and link_str.startswith("http"):
                    await write_link_in_file(link_str)
                    if depth > 0:
                        await get_link(client, link_str, depth - 1)
        except TimeoutError as err:
            logger.exception(f"не возможно перейти по ссылке {url}")


async def write_link_in_file(content: str):
    async with aiofiles.open('links_db.txt', mode='a') as file:
        await file.write(content + '\n')


# async def get_html(*url):
#     async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(10)) as session:
#         htmls = [get_link(session, i_url) for i_url in url]
#         return await asyncio.gather(*htmls)


async def get_html(url):
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(10)) as session:
        htmls = get_link(session, url)
        return await asyncio.gather(htmls)


if __name__ == '__main__':
    asyncio.run(get_html(URL))




