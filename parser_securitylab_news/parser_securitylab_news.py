import datetime
import time
import json

import requests
from bs4 import BeautifulSoup


HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15'
}


def get_html():
    r = requests.get(url='https://www.securitylab.ru/news/', headers=HEADERS)

    with open('index.html', 'w') as file:
        file.write(r.text)


def parser_html():
    with open('index.html') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    cards = soup.find_all('a', class_='article-card inline-card')

    list_id = [card.get('href').strip().split('/')[-1].split('.')[0] for card in cards]

    news_dict = {}

    for card in cards:
        link = 'https://www.securitylab.ru' + card.get('href').strip()
        article_date_time = card.find('time').get('datetime')
        title = card.find('h2').text.strip()
        context = card.find('p').text.strip()

        date_from_iso = datetime.datetime.fromisoformat(article_date_time)
        date_time = datetime.datetime.strftime(date_from_iso, '%Y-%m-%d %H:%M:%S')
        date_timestamp = time.mktime(datetime.datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S').timetuple())

        id_news = link.split('/')[-1].split('.')[0]

        news_dict[id_news] = {
            'date_timestamp': date_timestamp,
            'title': title,
            'link': link,
            'context': context
        }

    with open('news_dict.json', 'w') as file:
        json.dump(news_dict, file, ensure_ascii=False, indent=4)


def check_news_update():
    get_html()

    with open('index.html') as file:
        src = file.read()

    with open('news_dict.json') as file:
        news_dict = json.load(file)

    soup = BeautifulSoup(src, 'lxml')

    cards = soup.find_all('a', class_='article-card inline-card')

    fresh_news = {}

    for card in cards:
        id_news = card.get('href').strip().split('/')[-1].split('.')[0]
        if id_news in news_dict:
            continue
        link = 'https://www.securitylab.ru' + card.get('href').strip()
        article_date_time = card.find('time').get('datetime')
        title = card.find('h2').text.strip()
        context = card.find('p').text.strip()

        date_from_iso = datetime.datetime.fromisoformat(article_date_time)
        date_time = datetime.datetime.strftime(date_from_iso, '%Y-%m-%d %H:%M:%S')
        date_timestamp = time.mktime(datetime.datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S').timetuple())

        news_dict[id_news] = {
            'date_timestamp': date_timestamp,
            'title': title,
            'link': link,
            'context': context
        }

        fresh_news[id_news] = {
            'date_timestamp': date_timestamp,
            'title': title,
            'link': link,
            'context': context
        }

    with open('news_dict.json', 'w') as file:
        json.dump(news_dict, file, ensure_ascii=False, indent=4)

    return fresh_news


def main():
    get_html()
    parser_html()
    # print(check_news_update())


if __name__ == '__main__':
    main()

