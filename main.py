from dotenv import load_dotenv
import requests
import json
import os
import argparse
import sys


def get_bitlink(token, long_url):
    headers = {'Authorization': token}
    params = {'long_url': long_url}
    URL = 'https://api-ssl.bitly.com/v4/bitlinks'
    response = requests.post(URL, headers=headers, json=params)
    response.raise_for_status()
    bitlink = response.json()['id']
    return bitlink


def count_clicks(token, short_url):
    headers = {'Authorization': token}
    params = {'units': -1}
    URL = \
        'https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary'.format(short_url)
    response = requests.get(URL, headers=headers, params=params)
    response.raise_for_status()
    bitlink_json = response.json()
    return bitlink_json['total_clicks']


if __name__ == '__main__':
    load_dotenv()
    parser = argparse.ArgumentParser(description='Программа сокращает ссылки и считает клики в bit.ly')
    parser.add_argument('input_url',help='Вставьте ссылку')
    args = parser.parse_args()
    input_url = sys.argv[1]
    token = os.getenv('BITLY_TOKEN')
    if input_url.lower().startswith('bit.ly'):
        try:
            clicks_count = count_clicks(token, input_url)
            print ('Всего кликов: ', clicks_count)
        except requests.exceptions.HTTPError:
            print('Невалидная ссылка')
    else:
        try:
            bitlink = get_bitlink(token, input_url)
            print (input_url, '- ', bitlink)
        except requests.exceptions.HTTPError:
            print('Невалидная ссылка')
