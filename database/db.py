import boto3
from redis import Redis
import os
from dotenv import load_dotenv

load_dotenv()

dynamodb = boto3.resource(
    'dynamodb',
    region_name=os.getenv('REGION_NAME'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

redis = Redis.from_url(
    os.getenv('REDIS_CONNECTION_STRING'), password=os.getenv('PASSWORD_REDIS'), decode_responses=True)
