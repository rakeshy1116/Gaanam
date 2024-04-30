import boto3
from boto3.dynamodb.conditions import Attr, Key
from boto3 import resource

# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb',region_name='us-east-2')

def put_item(TableName, Item):
    try:
        response = dynamodb.put_item(
            TableName=TableName,
            Item=Item
        )
        return response
    except Exception as e:
        print("Error:", e) 

def get_item(TableName, key):
    try:
        # Get item from DynamoDB table
        response = dynamodb.get_item(
            TableName=TableName,
            Key = {
            'user_id': { 'S': key } }
        )
        return response
    except Exception as e:
        print("Error:", e)

def queryByPartKey(TableName, key):
    demo_table = resource('dynamodb',region_name='us-east-2').Table(TableName)
    response = {}
    filtering_exp = Key('user_id').eq(key)
    response = demo_table.query(
        KeyConditionExpression=filtering_exp)
    item_list = response["Items"]
    # for item in item_list:
    #     print(f'Item: {item}')
    return item_list

def create_user(user_id, access_token, playlist_id):
    try:
        item = {
            'user_id': {'S': user_id},
            'access_token': {'S': access_token},
            'playlist_id': {'S': playlist_id}
        }
    except Exception as e:
        print("Error:", e)
    return item

def create_song(user_id, position, track_name,track_id,track_artist,track_image,track_preview,track_is_recommended,time_range,ttl):
    try:
        item = {
            'user_id': {'S': user_id},
            'position': {'N': str(position)},
            'track_name': {'S': track_name},
            'track_id': {'S': track_id},
            'track_artist': {'S': track_artist},
            'track_image': {'S': track_image},
            'track_preview': {'S': track_preview},
            'track_is_recommended': {"BOOL": track_is_recommended},
            'time_range': {'S': time_range},
            'ttl': {'N': ttl}
        }
    except Exception as e:
        print("Error:", e)
    return item

def create_artist(user_id,position, artist_name,artist_id,track_image,time_range,ttl):
    try:
        item = {
            'user_id': {'S': user_id},
            'position': {'N': str(position)},
            'artist_name': {'S': artist_name},
            'artist_id': {'S': artist_id},
            'track_image': {'S': track_image},
            'time_range': {'S': time_range},  
            'ttl': {'N': ttl}    
        }
    except Exception as e:
        print("Error:", e)
    return item
