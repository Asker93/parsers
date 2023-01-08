import os
import json
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import aiofiles
import random


if not os.path.exists('data'):
    os.mkdir('data')


HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15'
}


async def get_html(session: aiohttp.ClientSession, url: str):
    result = await session.get(url, headers=HEADERS, ssl=True)
    return result


# def parser_and_save_data():
#     with open('persons_url_list.txt') as file:
#         lines = [line.strip() for line in file.readlines()]
#
#         data_dict = []
#         count = 0
#         for line in lines[0:20]:  # убрать количество
#             req = requests.get(line)
#             result = req.content
#
#             soup = BeautifulSoup(result, 'lxml')
#
#             person = soup.find(class_='col-xs-8 col-md-9 bt-biografie-name').find('h3').text.strip()
#             person_name_company = person.split(',')
#
#             person_name = person_name_company[0].strip()
#             person_company = person_name_company[1].strip()
#
#             social_networks = soup.find(class_='bt-linkliste').find_all(class_='bt-link-extern')
#
#             social_networks_urls = []
#             for line in social_networks:
#                 social_networks_urls.append(line.get('href').strip())
#
#             data = {
#                 'person_name': person_name,
#                 'company_name': person_company,
#                 'social_networks': social_networks_urls
#             }
#
#             data_dict.append(data)
#             count += 1
#             print(f'Выполнено {count}/{len(lines[0:20])}')
#
#         with open('data.json', 'w') as file:
#             json.dump(data_dict, file, indent=4)


async def save_html(result, count):
    async with aiofiles.open(f'data/{count}.html', 'w') as file:
        await file.write(await result.text())


async def main():
    with open('persons_url_list.txt') as file:
        hosts = [line.strip() for line in file.readlines()]

    urls = []
    for url in hosts:
        a = url.split('/')[-1:][0]
        url = 'https://www.bundestag.de/abgeordnete/biografien/' + a[0].upper() + '/' + a
        urls.append(url)

    print(urls)

    # async with aiohttp.ClientSession() as session:
    #     tasks = [get_html(session, url) for url in urls]
    #
    #     count = 1
    #     for task in asyncio.as_completed(tasks):
    #         result: aiohttp.ClientResponse = await task
    #
    #         await save_html(result, count)
    #         count += 1


if __name__ == '__main__':
    asyncio.run(main())
