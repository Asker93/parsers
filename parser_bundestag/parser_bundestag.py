import requests
from bs4 import BeautifulSoup
import json


persons_url_list = []

for i in range(0, 760, 20):
# for i in range(0, 40, 20):
    url = f'https://www.bundestag.de/ajax/filterlist/en/members/863330-863330?limit=20&noFilterSet=true&offset={i}'
    # print(url)

    q = requests.get(url)
    result = q.content

    soup = BeautifulSoup(result, 'lxml')

    persons = soup.find_all(class_='bt-slide-content')

    for person in persons:
        person_url = person.find('a').get('href')

        persons_url_list.append(person_url)


with open('persons_url_list.txt', 'w') as file:
    for line in persons_url_list:
        file.write(f'{line}\n')

# with open('persons_url_list.txt') as file:
#     lines = [line.strip() for line in file.readlines()]
#
#     data_dict = []
#     count = 0
#     for line in lines[0:20]: # убрать количество
#         req = requests.get(line)
#         result = req.content
#
#         soup = BeautifulSoup(result, 'lxml')
#
#         person = soup.find(class_='col-xs-8 col-md-9 bt-biografie-name').find('h3').text.strip()
#         person_name_company = person.split(',')
#
#         person_name = person_name_company[0].strip()
#         person_company = person_name_company[1].strip()
#
#         social_networks = soup.find(class_='bt-linkliste').find_all(class_='bt-link-extern')
#
#         social_networks_urls = []
#         for line in social_networks:
#             social_networks_urls.append(line.get('href').strip())
#
#         data = {
#             'person_name': person_name,
#             'company_name': person_company,
#             'social_networks': social_networks_urls
#         }
#
#         data_dict.append(data)
#         count += 1
#         print(f'Выполнено {count}/{len(lines[0:20])}')
#
#     with open('data.json', 'w') as file:
#         json.dump(data_dict, file, indent=4)





