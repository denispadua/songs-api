import json

from flask import Blueprint, abort, jsonify, request

import api.services as service

api_bp = Blueprint('api_bp', __name__, url_prefix='/api')


@api_bp.before_request
def cache():

    artist_name = request.args.get('artist_name', type=str)
    cache = request.args.get('cache', 'True', type=str)

    if artist_name is None:
        abort(400, "artist_name is required")

    transaction = service.search_transaction(artist_name)

    if transaction['Items'] != []:
        transaction_data = transaction['Items'][0]

        if transaction_data['Cache'] == 'True':
            songs_cache = service.get_cache(transaction_data['Id'])

            if songs_cache:
                if cache == 'True':
                    songs_cache = json.loads(songs_cache)
                    return jsonify({'cache': songs_cache})
                else:
                    service.delete_cache(transaction_data['Id'])


@api_bp.get('/')
def get_top_songs():

    artist_name = request.args.get('artist_name', type=str)
    cache = request.args.get('cache', 'True', type=str)

    artist_data = service.get_json_data('/search', params={'q': artist_name})
    artist_id = service.get_artist_id(artist_data, artist_name)

    uri_songs = '/artists/{}/songs'.format(artist_id)
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
