import asyncio
import aiohttp
import aiofiles

from bs4 import BeautifulSoup, SoupStrainer
from urllib import parse
from pathlib import Path

from loguru import logger


URL = "https://www.klenmarket.ru"
# URL = "write URL" #укажите ссылку для начала обхода
NESTING_LEVEL = 2  # Уровень вложенности для обхода
HEADER = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
           "Chrome/108.0.0.0 YaBrowser/23.1.4.776 Yowser/2.5 Safari/537.36"}
FILE_NAME = 'links.txt' # Имя файла для записи ссылок


async def write_link_in_file(link):
    async with aiofiles.open(FILE_NAME, mode='a', encoding='utf-8') as file:
        await file.write(link+'\n')


async def link_search(text_html, level, netlocal):
    soup = BeautifulSoup(markup=text_html, features="lxml", parse_only=SoupStrainer('a'))
    list_tags_a = soup.find_all('a')
    for i_tag in list_tags_a:
        if i_tag.has_attr('href'):
            link = i_tag['href']
            url_parse = parse.urlparse(link)
            if (url_parse.scheme == "http" or url_parse.scheme == "https") and url_parse.netloc != netlocal:
                await write_link_in_file(link)
                if level > 0:
                    await get_content(url=link, level=level-1)


async def get_content(url, level):
    url_sate = parse.urlparse(url).netloc
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(10)) as session:
            async with session.get(url=url) as response:
                if response.status == 200:
                    text_html = await response.text()
                    await link_search(text_html, level, netlocal=url_sate)

    except:
        logger.exception(f"не возможно перейти по ссылке {url}")
        # asyncio.TimeoutError(f"не возможно перейти по ссылке {url}")


def main():
   loop = asyncio.get_event_loop()
   loop.run_until_complete(get_content(URL, NESTING_LEVEL))


if __name__ == '__main__':
    if Path(FILE_NAME).exists():
        Path(FILE_NAME).unlink()
    main()



