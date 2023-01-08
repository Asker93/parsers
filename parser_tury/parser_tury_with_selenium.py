import json
import csv
import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver


if not os.path.exists('data'):
    os.mkdir('data')

headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15'
    }


def get_links():
    req = requests.get(url='https://api.rsrv.me/hc.php?a=hc&most_id=1317&l=ru&sort=most&hotel_link=/hotel/id/%HOTEL_ID%&r=1865103564', headers=headers)

    soup = BeautifulSoup(req.text, 'lxml')

    hotel_cards = soup.find_all('div', class_='hotel_card_dv')

    hrefs = []

    for card in hotel_cards:
        host = 'https://tury.ru'
        href = host + card.find('div', class_='hotel_info_dv').find('a').get('href')
        hrefs.append(href)

    with open('data/hotels_links.txt', 'w') as file:
        for line in hrefs:
            file.write(line + '\n')


def get_links_with_selenium(url):
    options = webdriver.ChromeOptions()
    # options.set_preference('general.useragent.override', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15')

    try:
        driver = webdriver.Chrome(
            executable_path='/Users/askerkhan/PycharmProjects/pythonProject1/python_today/parsers/parser_tury/chromedriver',
            options=options
        )
        driver.get(url=url)
        time.sleep(5)

        with open('index_selenium.html', 'w', encoding='utf-8') as file:
            file.write(driver.page_source)

    except Exception as exc:
        print(exc)
    finally:
        driver.close()
        driver.quit()

    with open('index_selenium.html') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    hotel_cards = soup.find_all('div', class_='hotel_card_dv')

    hrefs = []

    for card in hotel_cards:
        host = 'https://tury.ru'
        href = host + card.find('div', class_='hotel_info_dv').find('a').get('href')
        hrefs.append(href)

    with open('data/hotels_links.txt', 'w') as file:
        for line in hrefs:
            file.write(line + '\n')


def get_and_save_data():
    with open('data/hotels_links.txt') as file:
        urls = [line.strip() for line in file.readlines()]

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
    for url in urls:
        r = requests.get(url=url, headers=headers)

        soup = BeautifulSoup(r.text, 'lxml')

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


def main():
    url = 'https://tury.ru/hotel/most_luxe.php'
    # get_links()
    get_links_with_selenium(url)
    get_and_save_data()


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print(f'Прошло {end - start} сек.')


