import boto3
from boto3.dynamodb.conditions import Key

# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb',region_name='us-east-2')


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

print(get_item("top_songs_short_term", "31pbwwhihwdses2j26ehgxvlz5ui"))

table = dynamodb.Table('top_songs_medium_term')
result = table.query(
        KeyConditionExpression=Key('user_id').eq('31pbwwhihwdses2j26ehgxvlz5ui')
    )
print(result['Items'])