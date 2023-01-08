import os
import json
import csv
import time

import requests
from bs4 import BeautifulSoup


if not os.path.exists('data'):
    os.mkdir('data')

headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15'
    }
url = 'https://www.labirint.ru/genres/2308/?available=1&paperbooks=1&display=table'


def get_first_html():
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, 'lxml')

    count_pages = int(soup.find_all('a', class_='pagination-number__text')[-1].text.strip())

    with open('data/1.html', 'w') as file:
        file.write(r.text)

    print(f'Скачано 1 из {count_pages}')

    return count_pages


def get_all_htmls():
    count_pages = get_first_html()

    for count in range(2, count_pages + 1):
        r = requests.get(url=url + f'&page={count}', headers=headers)

        with open(f'data/{count}.html', 'w') as file:
            file.write(r.text)

        print(f'Скачано {count} из {count_pages}')

    print('Загрузка html-страниц завершена!!!')


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


def main():
    get_all_htmls()
    parser_data()


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print(f'Прошло {end - start} сек.')
