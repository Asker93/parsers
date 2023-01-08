import os
import csv
import json
import requests
from bs4 import BeautifulSoup


def get_html(url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15'
    }

    req = requests.get(url=url, headers=headers)

    with open('index.html', 'w') as file:
        file.write(req.text)


def parser_data():
    if not os.path.exists('data'):
        os.mkdir('data')

    with open('index.html') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    wathes_cards = soup.find_all('div', class_='product-item carousel-item')

    # print(len(wathes_cards))

    with open('data/shop_casio.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                'Тип',
                'Артикул',
                'Ссылка',
                'Цена',
            )
        )

    list_wathes_for_json = []

    for card in wathes_cards:
        articles_and_prices = eval(card.get('data-analitics'))

        article = articles_and_prices['name']
        price = articles_and_prices['price']
        href = 'https://shop.casio.ru/' + card.find('a', class_='product-item__link').get('href')
        type_sex = card.find('p', class_='product-item__type').text.strip()

        list_wathes_for_json.append(
            {
                'type_sex': type_sex,
                'article': article,
                'href': href,
                'price': price
            }
        )

        with open('data/shop_casio.csv', 'a', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    type_sex,
                    article,
                    href,
                    price,
                )
            )

    with open('data/shop_casio.json', 'w', encoding='utf-8') as file:
        json.dump(list_wathes_for_json, file, ensure_ascii=False, indent=4)


def main():
    url = 'https://shop.casio.ru/catalog/g-shock/'
    # get_html(url)
    parser_data()


if __name__ == '__main__':
    main()
