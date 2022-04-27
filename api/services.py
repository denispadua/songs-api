import os
from datetime import datetime
from uuid import uuid4

import requests

from flask import abort


def get_artist_id(artist_data, artist_name):

    artists = artist_data['response']['hits']

    for artist in artists:
        if artist['result']['primary_artist']['name'] == artist_name:
            return artist['result']['primary_artist']['id']

    abort(404, description='Artist not found')


def get_json_data(url, params=None):

    BASE_API = 'http://api.genius.com'
    HEADERS = {
        'Authorization': 'Bearer ' + os.getenv('GENIUS_TOKEN')
    }

    try:
        return requests.get(url=BASE_API + url, params=params, headers=HEADERS).json()
    except:
        abort(500, description='Error to connect in Genius API')


def create_transaction(artist_name, cache):

    today_timestamp = datetime.timestamp(datetime.now())

    return {'Id': str(uuid4()),
            'Artist': artist_name,
            'Time': int(today_timestamp),
            'Cache': cache}
