import os
from urllib.parse import urlparse
import argparse
import requests
from dotenv import load_dotenv


def shorten_link(bitly_token, parser):
    bitly_url = "https://api-ssl.bitly.com/v4/shorten"
    headers = {
        "Authorization": f"Bearer {bitly_token}",
    }
    payload = {
        "long_url": parser,
    }
    response = requests.post(bitly_url, headers=headers, json=payload)
    response.raise_for_status()
    bitlink = response.json()["link"]
    return bitlink


def is_bitlink(bitly_token, url):
    bitly_url = f"https://api-ssl.bitly.com/v4/bitlinks/{url}"
    headers = {
        "Authorization": f"{bitly_token}",
    }
    response = requests.get(bitly_url, headers=headers)
    return response.ok


def count_clicks(bitly_token, bitlink):
    bitly_url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
    headers = {
        "Authorization": f'Bearer {bitly_token}',
    }
    response = requests.get(bitly_url, headers=headers)
    response.raise_for_status()
    return response.json()['total_clicks']


if __name__ == "__main__":
    load_dotenv()
    bitly_token = os.environ["BITLY_TOKEN"]
    parser = argparse.ArgumentParser(description="Ссылка")
    parser.add_argument("--url", help="Введите ссылку:")
    arguments = parser.parse_args()
    parsed_url = urlparse(arguments.url)
    parsed_bitlink = f'{parsed_url.netloc}{parsed_url.path}'
    try:
        if is_bitlink(bitly_token, parsed_bitlink):
           clicks_count = count_clicks(bitly_token, parsed_bitlink)
           print(clicks_count) 
        else:
            bitlink = shorten_link(bitly_token, arguments.url)
            print('Битлинк', bitlink)
    except requests.exceptions.HTTPError:
        print("Неверная ссылка или токен")
    