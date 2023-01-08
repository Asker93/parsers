import os
import csv
import json
import asyncio
import httpx
from bs4 import BeautifulSoup
import time


if not os.path.exists('data/indexes'):
    os.mkdir('data/indexes')


async def get_data(client, url):
    result = await client.get(url, follow_redirects=True)
    return result


def get_and_save_data():
    with open('data/tury.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                'Страна',
                'Город',
                'Название',
                'Адрес'
            )
        )

    list_hotels_for_json = []
    for item in range(1, 101):
        with open(f'data/indexes/{item}.html') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')

        country_item, city_item = soup.find_all('a', class_='bread-crumbs__link')[-2:]

        country = country_item.text.strip()
        city = city_item.text.strip()
        name = soup.find('div', class_='h1').text.strip()
        address = soup.find('a', class_='hotel-contact__link').text.strip()

        list_hotels_for_json.append(
            {
                'country': country,
                'city': city,
                'name': name,
                'address': address
            }
        )

        with open('data/tury.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    country,
                    city,
                    name,
                    address
                )
            )

    with open('data/tury.json', 'w') as file:
        json.dump(list_hotels_for_json, file, ensure_ascii=False, indent=4)


async def main():
    with open('data/hotels_links.txt') as file:
        urls = [line.strip() for line in file.readlines()]

    async with httpx.AsyncClient() as client:
        tasks = [get_data(client, url) for url in urls]

        count = 1
        for i in asyncio.as_completed(tasks, timeout=10):
            result = await i
            with open(f'data/indexes/{count}.html', 'w') as file:
                file.write(result.text)
            count += 1

    get_and_save_data()


if __name__ == '__main__':
    start = time.time()
    asyncio.run(main())
    end = time.time()
    print(f'Прошло {end - start} сек.')
