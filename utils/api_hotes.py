import requests
from config_data.config import RAPID_API_KEY
from typing import Literal

def get_cites(city: str) -> dict | None:

    querystring = {'q': city, 'locale':'ru_RU'}
    response = request_to_api(querystring=querystring, mode='loc')
    if not response:
        return None
    #TODO Тут добавить проверку и обработку ошибок парсинга

    cites = dict()
    for region in response['sr']:
        if region['type'] == 'CITY':
            cites[region['regionNames'].get('fullName')] = region['gaiaId']
    return cites
    ...

def request_to_api(querystring, mode):
    #TODO Парсинг для теста. Настроить несколько попыток при неудаче, добавить обработку ошибок
    if mode == 'loc':
        url = 'https://hotels4.p.rapidapi.com/locations/v3/search'
        headers = {
            "X-RapidAPI-Key": RAPID_API_KEY,
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
        }
    else:
        return None
    try:
        response = requests.request('GET', url, headers=headers, params=querystring, timeout=50)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            response = response.json()
            return response
        else:
            return response.status_code #Так для отладки
    except requests.exceptions.RequestException as er:
        return er #TODO: Настроить обработку ошибок
    return None
