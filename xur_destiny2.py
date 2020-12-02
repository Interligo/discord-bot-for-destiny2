import os
import requests
from bs4 import BeautifulSoup as bs

from load_environment import load_environment


load_environment()

DESTINY_API = os.getenv('DESTINY_API_KEY')
HEADERS = {"X-API-Key": DESTINY_API}


def is_xur_here() -> bool:
    """Function checking Xur and returns True/False."""
    xur_url = 'https://paracausal.science/xur/current.json'

    response = requests.get(xur_url, headers=HEADERS)
    data = response.json()

    search_result = False if data is None else True

    return search_result


def get_xur_location() -> str:
    """Function returns Xur's location from json."""
    xur_url = 'https://paracausal.science/xur/current.json'

    response = requests.get(xur_url, headers=HEADERS)
    data = response.json()

    if data is None:
        return 'Тайные люди Икоры Рей сообщают, что Посланника Девяти нет в Солнечной системе.'
    else:
        planet = data['destinationName']
        location = data['bubbleName']
        return f'Тайные люди Икоры Рей сообщают, что Зур был замечен: {planet}, {location}.'


def get_xur_location_from_url() -> str:
    """Function returns Xur's location from url."""
    xur_url = 'https://whereisxur.com/'

    session = requests.Session()
    response = session.get(xur_url)
    soup = bs(response.content, 'html.parser')
    xur_place = soup.find('h4')

    return xur_place.text
