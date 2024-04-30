import boto3
import json

# Create SQS client
sqs = boto3.client('sqs',region_name="us-east-2")
queue_url = 'https://sqs.us-east-2.amazonaws.com/815490976597/gaanam-sqs'

def send_message(msgBody):
    print(msgBody)
    response = sqs.send_message(
    QueueUrl=queue_url,
    # DelaySeconds=10,
    MessageAttributes={
        'User': {
            'DataType': 'String',
            'StringValue': 'User info'
        },
    },
    MessageBody=(
        json.dumps(msgBody)
    )
)

def receive_message(test=False):
    while True:
        response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=[
            'All'
        ],
        MaxNumberOfMessages=10,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=5,
        WaitTimeSeconds=1
    )
        if 'Messages' in response:
            break
        else:
            if test:
                break
            print('Waiting for messages in queue')
            continue

    message = response['Messages'][0]
    body = json.loads(message['Body'])
    # print(body)
    receipt_handle = message['ReceiptHandle']

    # Delete received message from queue
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )
    # print('Received and deleted message: %s' % message)
    return body

