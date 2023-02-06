import aiohttp
import asyncio
import datetime

from bs4 import BeautifulSoup
from urllib.parse import urlsplit

from api.models import Museum


async def get_url(
    url: str,
    session: aiohttp.ClientSession,
    urls_set: set,
    errors_set: set
) -> None:
    try:
        async with session.get(url, allow_redirects=True, headers={
            'User-Agent':
            (
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                '(KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
            )
        }) as response:
            data = await response.text()
            if 'wp-content' in data:
                splited_url = urlsplit(url)
                db_url = splited_url.scheme + '://' + splited_url.netloc
                if db_url not in urls_set:
                    urls_set.add(db_url)
    except Exception:
        spl_url = urlsplit(url)
        errors_set.add(spl_url.netloc)


async def add_records(
    url: str,
    session: aiohttp.ClientSession,
    errors_set: set
) -> None:
    try:
        async with session.get(url, headers={
            'User-Agent':
            (
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                '(KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
            )
        }) as response:
            posts = await response.json()
            for post in posts:
                title = BeautifulSoup(post['title']['rendered'], 'lxml').text
                content = BeautifulSoup(
                    post['content']['rendered'], 'lxml'
                ).text
                url_spl = urlsplit(url)
                service = url_spl.netloc
                await Museum.objects.acreate(service=service, link=post['link'], title=title, content=content)
    except Exception:
        spl_url = urlsplit(url)
        errors_set.add(spl_url.netloc)


async def fullfill_db() -> None:
    fp = open('museums-urls.csv', 'r')
    urls_file = open('nec-urls.txt', 'w')
    errors_file = open('errors.txt', 'w')
    urls_set = set()
    errors_set = set()
    counter = 0
    tasks_url = []
    sem3 = asyncio.Semaphore(5)
    print('Searching WP sites begin')
    async with sem3:
        async with aiohttp.ClientSession() as session:
            for line in fp.readlines():
                line_spl = line.split(',')
                counter += 1
                if counter == 1:
                    continue
                task_url = asyncio.create_task(get_url(
                    line_spl[-2], session, urls_set, errors_set
                ))
                tasks_url.append(task_url)
            await asyncio.gather(*tasks_url)
    tasks_parse = []
    sem4 = asyncio.Semaphore(5)
    print('Adding data to db')
    async with sem4:
        async with aiohttp.ClientSession() as session:
            for url in urls_set:
                request_url = url + '/wp-json/wp/v2/posts'
                task_parse = asyncio.create_task(add_records(
                    request_url, session, errors_set
                ))
                tasks_parse.append(task_parse)
            await asyncio.gather(*tasks_parse)
    for url in urls_set:
        urls_file.write(url + '\n')
    for error in errors_set:
        errors_file.write(error + '\n')
    urls_file.close()
    errors_file.close()
    fp.close()


time1 = datetime.datetime.utcnow()
asyncio.run(fullfill_db())
time2 = datetime.datetime.utcnow()
print('Время выполнения программы', time2 - time1)