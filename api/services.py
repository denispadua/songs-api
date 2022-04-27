import json
import os
from datetime import datetime, timedelta
from uuid import uuid4

import requests
from boto3.dynamodb.conditions import Key
from flask import abort

from database.db import dynamodb, redis


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


def save_transaction(transaction):

    try:
        table = dynamodb.Table('Transactions')
        table.put_item(Item=transaction)
    except:
        abort(500, description='Its not possible to create transaction')


def create_cache(id, top_songs):

    redis.setex(id, timedelta(7), json.dumps(top_songs))


def create_transaction(artist_name, cache):

    today_timestamp = datetime.timestamp(datetime.now())

    return {'Id': str(uuid4()),
            'Artist': artist_name,
            'Time': int(today_timestamp),
            'Cache': cache}


def search_transaction(artist_name):

    table = dynamodb.Table('Transactions')

    interval = int(datetime.timestamp(datetime.now()-timedelta(7)))

    return table.query(
        KeyConditionExpression=Key('Artist').eq(artist_name) &
        Key('Time').gte(interval),
        Limit=1,
        ScanIndexForward=False)


def get_cache(id):

    return redis.get(id)


def delete_cache(id):

    redis.delete(id)
