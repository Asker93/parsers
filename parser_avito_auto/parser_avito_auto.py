import time
import os
import json
import csv
import requests
from bs4 import BeautifulSoup
from selenium import webdriver


URL = 'https://www.avito.ru/moskva_i_mo/avtomobili?cd=1&s=104'

HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'host': 'www.avito.ru',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15',
    'accept-language': 'ru',
    'referer': 'https://www.avito.ru/',
    'connection': 'keep-alive'
}


def get_html():
    with requests.Session() as session:
        session.headers = HEADERS

        params = {
            'cd': 1,
            's': 104
        }

        r = session.get(url=URL, params=params)

    # r = requests.get(url=URL, headers=HEADERS, cookies={'cookie': 'tmr_detect=0%7C1672947014437; cto_bundle=lYRDg184ZGlmc002YmJONVRib2t6aUxRczA1MGprNjE5a251ODZwbE1OZjV6MDFiM0F4SGwlMkJTTmolMkZTc0lDNG9DUHVoUWxYQVZ2JTJCN25OTDVpYSUyQjNuSmt2aEZUTXFnZGY2YWdwQ210d211MyUyRlRtVUhEREh4dHRUZEkwY3NHUFBzVVM1cUg; _ga=GA1.1.1139955084.1672946748; _ga_M29JC28873=GS1.1.1672946748.1.1.1672947012.16.0.0; tmr_lvid=fedcc8ff71d00234674f3fe005da6956; tmr_lvidTS=1672946748393; buyer_location_id=107620; sx=H4sIAAAAAAAC%2F1TMza2DMAwA4F185kCeHSdmm8QxAT1UKD9VEWL3nnroAt8FjmLszYQLoYkzyhwdq6AmtYQJugte0AFlf1S3Y6plWf7Fb%2BesNJ99wvBHhNCAQec4YIuIgncDzMxaAvfC4plYLGRDKcG3qqHIVx6Gx6FTcdvunlytrpnKONU4r4zb%2BP6VOdz3JwAA%2F%2F9AWjrPtQAAAA%3D%3D; v=1672946670; abp=0; buyer_laas_location=107620; adrcid=Ao1XOM80SFJPrAiKgOtCMyg; adrdel=1; _gcl_au=1.1.621531206.1672946747; dfp_group=32; luri=moskva_i_mo; u=2tkw0duw.p6bx5.1w271uhwgf600',})

        with open('index.html', 'w') as file:
            file.write(r.text)


def get_html_with_selenium(pagination=1):
    options = webdriver.ChromeOptions()

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15')
    options.add_argument('cookie=tmr_detect=0%7C1672947014437; cto_bundle=lYRDg184ZGlmc002YmJONVRib2t6aUxRczA1MGprNjE5a251ODZwbE1OZjV6MDFiM0F4SGwlMkJTTmolMkZTc0lDNG9DUHVoUWxYQVZ2JTJCN25OTDVpYSUyQjNuSmt2aEZUTXFnZGY2YWdwQ210d211MyUyRlRtVUhEREh4dHRUZEkwY3NHUFBzVVM1cUg; _ga=GA1.1.1139955084.1672946748; _ga_M29JC28873=GS1.1.1672946748.1.1.1672947012.16.0.0; tmr_lvid=fedcc8ff71d00234674f3fe005da6956; tmr_lvidTS=1672946748393; buyer_location_id=107620; sx=H4sIAAAAAAAC%2F1TMza2DMAwA4F185kCeHSdmm8QxAT1UKD9VEWL3nnroAt8FjmLszYQLoYkzyhwdq6AmtYQJugte0AFlf1S3Y6plWf7Fb%2BesNJ99wvBHhNCAQec4YIuIgncDzMxaAvfC4plYLGRDKcG3qqHIVx6Gx6FTcdvunlytrpnKONU4r4zb%2BP6VOdz3JwAA%2F%2F9AWjrPtQAAAA%3D%3D; v=1672946670; abp=0; buyer_laas_location=107620; adrcid=Ao1XOM80SFJPrAiKgOtCMyg; adrdel=1; _gcl_au=1.1.621531206.1672946747; dfp_group=32; luri=moskva_i_mo; u=2tkw0duw.p6bx5.1w271uhwgf600')
    options.add_argument('accept=text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    options.add_argument('accept-encoding=gzip, deflate, br')
    options.add_argument('host=www.avito.ru')
    options.add_argument('accept-language=ru')
    options.add_argument('referer=https://www.avito.ru/')
    options.add_argument('connection=keep-alive')


    for i in range(1, pagination + 1):
        try:
            driver = webdriver.Chrome(
                executable_path='/Users/askerkhan/PycharmProjects/pythonProject1/python_today/parsers/parser_tury/chromedriver',
                options=options
            )
            # print(driver.)
            # driver.get(url='https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html')
            driver.get(url=f'https://www.avito.ru/moskva_i_mo/avtomobili?cd=1&p={i}&s=104&user=1')

            time.sleep(2)

            with open(f'indexes/{i}.html', 'w', encoding='utf-8') as file:
                file.write(driver.page_source)

        except Exception as exc:
            print(exc)
        finally:
            driver.close()
            driver.quit()


def get_pagination():
    with open('index_selenium.html') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    count_page = soup.find('div', class_='js-pages pagination-pagination-_FSNE').find_all('span')[-2].text

    return int(count_page)


def parser_data():
    first_parser_dir = 'data/auto_csv.csv'
    first_parser_flag = 'w'

    save_csv(first_parser_dir, first_parser_flag)

    list_indexes = os.listdir('indexes')

    list_auto_for_json = {}

    for index in sorted(list_indexes):

        with open(f'indexes/{index}') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')

        cards = soup.find_all('div', class_='js-catalog-item-enum')

        for card in cards:
            id_card = card.get('data-item-id')
            link = 'https://www.avito.ru' + card.find('a').get('href').strip()
            name, year = card.find('h3').text.strip().split(',')
            price = int(card.find('span', class_='price-text-_YGDY').text.strip().replace(' ', '').replace(' ', '').replace('₽', '').replace('от', ''))

            parameters = card.find('div', class_='iva-item-text-Ge6dR').text.strip().split(',')

            if len(parameters) == 5:
                bit_nebit, probeg, loshad_sil, kuzov, trans, type_auto = ['Не указано'] + parameters
            elif len(parameters) == 6:
                bit_nebit, probeg, loshad_sil, kuzov, trans, type_auto = parameters
            # else:
            #     error = 'DANGER: Длина параметров больше 6, надо переписать код!!!'

            context = '. '.join(word.strip() for word in card.find('div', class_='iva-item-description-FDgK4').text.strip().split('.')).replace('\n', '')

            time_of_buy = card.find('div', class_='iva-item-dateInfoStep-_acjp').text.strip()

            list_auto_for_json[id_card] = {
                        'time_of_buy': time_of_buy,
                        'link': link,
                        'name': name,
                        'year': year,
                        'price': price,
                        'bit_nebit': bit_nebit,
                        'probeg': probeg.replace(' ', ' '),
                        'loshad_sil': loshad_sil.replace(' ', ' '),
                        'kuzov': kuzov,
                        'trans': trans,
                        'type_auto': type_auto,
                        'context': context
                    }

            save_csv(first_parser_dir, 'a', time_of_buy, link, name, year, price, bit_nebit, probeg, loshad_sil, kuzov, trans, type_auto, context)

    save_json('data/auto.json', list_auto_for_json)
    # save_json('data/auto_new.json', list_auto_for_json)


def save_csv(direct, flag, *args):
    with open(direct, flag) as file:
        writer = csv.writer(file)
        if args:
            time_of_buy = args[0]
            link = args[1]
            name = args[2]
            year = args[3]
            price = args[4]
            bit_nebit = args[5]
            probeg = args[6]
            loshad_sil = args[7]
            kuzov = args[8]
            trans = args[9]
            type_auto = args[10]
            context = args[11]
            writer.writerow(
                (
                    time_of_buy,
                    link,
                    name,
                    year,
                    price,
                    bit_nebit,
                    int(probeg.replace(' ', ' ').replace(' ', '').replace('км', '')),
                    loshad_sil.replace(' ', ' '),
                    kuzov,
                    trans,
                    type_auto,
                    context
                )
            )
        else:
            writer.writerow(
                (
                    'Время объявления',
                    'Ссылка',
                    'Название',
                    'Год выпуска',
                    'Цена',
                    'Б/не Б',
                    'Пробег',
                    'Д-Л/С',
                    'Кузов',
                    'Транс',
                    'Заправка',
                    'Описание',
                )
            )


def save_json(direct, data):
    with open(direct, 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def check_new_auto():
    with open('data/auto.json') as file:
        old_json = json.load(file)

    list_keys_old_json = []
    for item_old in old_json:
        for i in item_old:
            list_keys_old_json.append(i)

    with open('data/auto_new.json') as file:
        new_json = json.load(file)

    count = 0
    for item_new in new_json:
        if item_new not in list_keys_old_json:
            count += 1


def main():
    if not os.path.exists('indexes'):
        os.mkdir('indexes')

    if not os.path.exists('data'):
        os.mkdir('data')

    get_html_with_selenium(3)
    parser_data()
    # get_html()
    # check_new_auto()


if __name__ == '__main__':
    main()
