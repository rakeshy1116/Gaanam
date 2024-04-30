from boto3 import resource
from boto3.dynamodb.conditions import Attr, Key
from datetime import datetime

demo_table = resource('dynamodb').Table('top_songs_medium_term')

def query_by_partition_key(primKey):
    print(f'demo_select_query')

    response = {}
    filtering_exp = Key('user_id').eq(primKey)
    response = demo_table.query(
        KeyConditionExpression=filtering_exp)
    item_list = response["Items"]
    for item in item_list:
        print(f'Item: {item}')

query_by_partition_key('31pbwwhihwdses2j26ehgxvlz5ui')