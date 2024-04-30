import unittest
from unittest.mock import patch, MagicMock
import dynamodb_util as dynamodb_util

class TestDynamoDBUtil(unittest.TestCase):
    @patch('dynamodb_util.dynamodb.put_item')
    def test_put_item(self, mock_put_item):
        mock_put_item.return_value = 'put_response'
        TableName = 'user_table'
        Item = 'user_item'

        result = dynamodb_util.put_item(TableName, Item)

        self.assertEqual(result, 'put_response')
        mock_put_item.assert_called_once_with(TableName=TableName, Item=Item)

    @patch('dynamodb_util.dynamodb.get_item')
    def test_get_item(self, mock_get_item):
        mock_get_item.return_value = 'get_response'
        TableName = 'user_table'
        key = 'user_id'

        result = dynamodb_util.get_item(TableName, key)

        self.assertEqual(result, 'get_response')
        mock_get_item.assert_called_once_with(TableName=TableName, Key={'user_id': {'S': key}})

    # @patch('dynamodb_util.resource')
    # def test_queryByPartKey(self, mock_resource):
    #     mock_table = MagicMock()
    #     mock_resource.return_value.Table.return_value = mock_table
    #     mock_table.query.return_value = 'query_response'
    #     TableName = 'user_table'
    #     key = 'user_key'

    #     result = dynamodb_util.queryByPartKey(TableName, key)

    #     self.assertEqual(result, 'query_response')
    #     mock_table.query.assert_called_once()

if __name__ == '__main__':
    unittest.main()