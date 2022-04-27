import boto3
from flask import abort
from redis import Redis
import os
from boto3.dynamodb.conditions import Key
from datetime import datetime, timedelta

dynamodb = boto3.resource(
    'dynamodb',
    region_name=os.getenv('REGION_NAME'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

redis = Redis.from_url(
    os.getenv('REDIS_CONNECTION_STRING'), password=os.getenv('PASSWORD_REDIS'), decode_responses=True)


def save_transaction(transaction):

    try:
        table = dynamodb.Table('Transactions')
        table.put_item(Item=transaction)
    except:
        abort(500, description='Its not possible to create transaction')


def search_transaction(artist_name):

    table = dynamodb.Table('Transactions')

    interval = int(datetime.timestamp(datetime.now()-timedelta(7)))

    return table.query(
        KeyConditionExpression=Key('Artist').eq(artist_name) &
        Key('Time').gte(interval),
        Limit=1,
        ScanIndexForward=False)


def create_cache(id, top_songs):

    redis.setex(id, timedelta(7), top_songs)


def get_cache(id):

    return redis.get(id)


def delete_cache(id):

    redis.delete(id)
