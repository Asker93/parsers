import requests
import os

import pypdftk



def get_data():
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15'
    }

    if not os.path.exists('data'):
        os.mkdir('data')

    for i in range(1, 49):
        req = requests.get(url=f'https://recordpower.co.uk/flip/Winter2020/files/mobile/{i}.jpg', headers=headers)
        response = req.content
        with open(f'data/{i}.jpg', 'wb') as file:
            file.write(response)


def write_to_pdf():
    # print(os.listdir('data'))
    img_list = [f'data/{i}.jpg' for i in range(1, 49)]
    pypdftk.concat(img_list, 'result')


def main():
    # get_data()
    write_to_pdf()


if __name__ == '__main__':
    main()





