import json
from flask import Blueprint, jsonify, request
import api.services as service
from database.db import redis
api_bp = Blueprint('api_bp', __name__, url_prefix='/api')


@api_bp.before_request
def cache():

    artist_name = request.args.get('artist_name', type=str)
    cache = request.args.get('cache', 'True', type=str)

    transaction = service.search_transaction(artist_name)

    if transaction['Items'] != []:

        transaction_data = transaction['Items'][0]

        if transaction_data['Cache'] == 'True':

            songs_cache = redis.get(transaction_data['Id'])

            if songs_cache:
                if cache == 'True':
                    songs_cache = json.loads(songs_cache)
                    return jsonify({'cache': songs_cache})
                else:
                    redis.delete(artist_name)


@api_bp.get('/')
def get():

    artist_name = request.args.get('artist_name', type=str)
    cache = request.args.get('cache', 'True', type=str)

    artist_data = service.get_json_data('/search', params={'q': artist_name})
    artist_id = service.get_artist_id(artist_data, artist_name)

    uri_songs = f'/artists/{artist_id}/songs'
    top_songs = service.get_json_data(
        uri_songs, params={'sort': 'popularity', 'per_page': 10})

    transaction = service.create_transaction(artist_name, cache)
    service.save_transaction(transaction)

    if cache == 'True':
        service.create_cache(transaction['Id'],
                             top_songs=top_songs['response']['songs'])

    return jsonify({
        'data': top_songs['response']['songs']
    })
