import unittest
import boto3
import json
from moto import mock_aws
from sqs_util import send_message, receive_message

class TestSQSFunctions(unittest.TestCase):
    @mock_aws
    def test_send_message(self):
        sqs = boto3.client('sqs', region_name='us-east-2')
        queue_url = 'https://sqs.us-east-2.amazonaws.com/815490976597/gaanam-sqs'

        # Create a test queue
        sqs.create_queue(QueueName='gaanam-sqs')

        msg_body = {'key': 'value'}
        send_message(msg_body)

        # Receive the message from the queue
        response = sqs.receive_message(QueueUrl=queue_url)
        messages = response.get('Messages', [])
        self.assertEqual(len(messages), 1)
        self.assertEqual(json.loads(messages[0]['Body']), msg_body)

    @mock_aws
    def test_receive_message(self):
        sqs = boto3.client('sqs', region_name='us-east-2')
        queue_url = 'https://sqs.us-east-2.amazonaws.com/815490976597/gaanam-sqs'

        # Create a test queue
        sqs.create_queue(QueueName='gaanam-sqs')

        msg_body = {'key': 'value'}
        sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(msg_body))

        received_message = receive_message()
        self.assertEqual(received_message, msg_body)

if __name__ == '__main__':
    unittest.main()
