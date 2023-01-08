import random
import time
import os

import requests
from bs4 import BeautifulSoup
import json
import csv


HOST = 'https://health-diet.ru'
# req = requests.get('https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie')
#
# with open('index.html', 'w') as file:
#     file.write(req.text)


# with open('index.html') as file:
#     data = file.read()
#
#
# soup = BeautifulSoup(data, 'lxml')
# items = soup.find_all('div', class_='uk-flex mzr-tc-group-item')
#
#
# all_categories_dict = {}
#
# for item in items:
#     tag = item.find('a', class_='mzr-tc-group-item-href')
#     item_text = tag.text
#     item_href = HOST + tag.get('href')
#
#     all_categories_dict[item_text] = item_href
#
#
# with open('all_categories_dict.json', 'w') as file:
#     json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)


with open('all_categories_dict.json') as file:
    all_categories = json.load(file)


iteration_count = int(len(all_categories)) - 1
count = 0
print(f'Всего итераций: {iteration_count}')
for category_name, category_url in all_categories.items():

    rep = [',', ', ', '-', "'", ' ']

    for item in rep:
        if item in category_name:
            category_name = category_name.replace(item, '_')

    req = requests.get(url=category_url)
    src = req.text

    if not os.path.exists(f'{category_name}'):
        os.mkdir(f'data/{category_name}')

    with open(f'data/{category_name}/{count}_{category_name}.html', 'w') as file:
        file.write(src)

    with open(f'data/{category_name}/{count}_{category_name}.html') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    # проверка страницы на наличие таблицы с продуктами

    alert_block = soup.find(class_='uk-alert-danger')
    if alert_block is not None:
        continue

    # собираем заголовки таблицы

    table_head = soup.find(class_='mzr-tc-group-table').find('tr').find_all('th')
    product = table_head[0].text
    calories = table_head[1].text
    proteins = table_head[2].text
    fats = table_head[3].text
    carbohydrates = table_head[4].text

    with open(f'data/{category_name}/{count}_{category_name}.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                product,
                calories,
                proteins,
                fats,
                carbohydrates
            )
        )

    # собираем данные продуктов

    products_data = soup.find(class_='mzr-tc-group-table').find('tbody').find_all('tr')

    product_info = []

    for item in products_data:
        product_tds = item.find_all('td')

        title = product_tds[0].text.strip()
        calories = product_tds[1].text.strip()
        proteins = product_tds[2].text.strip()
        fats = product_tds[3].text.strip()
        carbohydrates = product_tds[4].text.strip()

        product_info.append(
            {
                'title': title,
                'calories': calories,
                'protiens': proteins,
                'fats': fats,
                'carbohydrates': carbohydrates
            }
        )

        with open(f'data/{category_name}/{count}_{category_name}.csv', 'a', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    title,
                    calories,
                    proteins,
                    fats,
                    carbohydrates
                )
            )

    with open(f'data/{category_name}/{count}_{category_name}.json', 'w') as file:
        json.dump(product_info, file, indent=4, ensure_ascii=False)

    count += 1
    print(f'# Итерация {count}. {category_name} записан...')
    iteration_count -= 1

    if iteration_count == 0:
        print('Работа завершена.')
        break

    print(f'Осталось итераций: {iteration_count}')
    # time.sleep(random.randrange(2, 4))









