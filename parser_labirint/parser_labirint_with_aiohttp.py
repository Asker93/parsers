import asyncio
import os
import json
import csv
import time

from bs4 import BeautifulSoup
import aiohttp


if not os.path.exists('data'):
    os.mkdir('data')

headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15'
    }
url = 'https://www.labirint.ru/genres/2308/?available=1&paperbooks=1&display=table&page='


def parser_data():
    name_head = 'Название'
    author_head = 'Автор'
    publish_head = 'ИЗД-ВО/СЕРИЯ'
    new_price_head = 'Актуальная цена'
    old_price_head = 'Старая цена'
    size_sale_head = 'Размер скидки'
    exist_head = 'Наличие'

    with open('all_books.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                name_head,
                author_head,
                publish_head,
                new_price_head,
                old_price_head,
                size_sale_head,
                exist_head
            )
        )

    all_books = []
    count = 1
    for page in sorted(os.listdir('data')):
        with open(f'data/{page}') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')

        table = soup.find('table', class_='products-table col-xs-12')
        table_body = table.find('tbody', class_='products-table__body').find_all('tr')

        for tr in table_body:
            all_details = tr.find_all('td')
            name = all_details[0].text.strip()
            author = all_details[1].text.strip()
            publish = ' '.join([word.strip() for word in all_details[2].text.strip().split()])
            new_price = all_details[3].find('span', class_='price-val').text.strip()

            try:
                old_price = all_details[3].find('span', class_='price-old').text.strip() + ' ₽'
            except AttributeError:
                old_price = ''

            try:
                size_sale = all_details[3].find('span', class_='price-val').get('title').split(' ')[0]
            except AttributeError:
                size_sale = 'Нет скидки'

            exist = all_details[5].text.strip()

            with open('all_books.csv', 'a') as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        name,
                        author,
                        publish,
                        new_price,
                        old_price,
                        size_sale,
                        exist
                    )
                )

            all_books.append(
                {
                    name_head: name,
                    author_head: author,
                    publish_head: publish,
                    new_price_head: new_price,
                    old_price_head: old_price,
                    size_sale_head: size_sale,
                    exist_head: exist
                }
            )
        print(f'Страница {count} завершена!')
        count += 1

    with open('all_books.json', 'w') as file:
        json.dump(all_books, file, ensure_ascii=False, indent=4)


count = 1
async def get_html(session, url):
    global count
    async with session.get(url, ssl=False) as result:
        response = await result.text()
        print(f'Скачано {count} стр.')
        count += 1
        return response


async def main():
    # get_all_htmls()
    # parser_data()
    async with aiohttp.ClientSession() as session:
        r = await session.get(url=url, headers=headers, ssl=False)
        soup = BeautifulSoup(await r.text(), 'lxml')
        count_pages = int(soup.find_all('a', class_='pagination-number__text')[-1].text.strip())
        tasks = [get_html(session, url + str(page)) for page in range(1, count_pages + 1)]

        count = 1
        for task in asyncio.as_completed(tasks):
            done = await task

            with open(f'data/{count}.html', 'w') as file:
                file.write(done)
            count += 1


if __name__ == '__main__':
    start = time.time()
    asyncio.run(main())
    parser_data()
    end = time.time()
    print(f'Прошло {end - start} сек.')

