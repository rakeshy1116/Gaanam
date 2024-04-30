import unittest
from unittest.mock import patch, MagicMock
from flask_collector import read_sqs_message, get_topSong, create_playlist, get_topArtist

class TestFunctions(unittest.TestCase):
    @patch('flask_collector.receive_message')
    def test_read_sqs_message(self, mock_receive_message):
        mock_message = {'user_id': 'test_user_id', 'access_token': 'test_access_token'}
        mock_receive_message.return_value = mock_message
        result = read_sqs_message()
        self.assertEqual(result, mock_message)

    # @patch('flask_collector.requests.get')
    # @patch('flask_collector.put_item')
    # def test_get_topSong(self, mock_put_item, mock_requests_get):
    #     mock_response = MagicMock()
    #     mock_response.json.return_value = {'items': []}  # Simulate an empty response
    #     mock_requests_get.return_value = mock_response

    #     result = get_topSong('short_term', 'test_user_id')
    #     self.assertEqual(result, "Uploaded songs to dynamoDB")
    #     self.assertEqual(mock_put_item.call_count, 0)  # No items should be put since the response is empty

    @patch('flask_collector.requests.post')
    def test_create_playlist(self, mock_requests_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {'external_urls': {'spotify': 'https://spotify.com/playlist/test_playlist'}}
        mock_requests_post.return_value = mock_response

        result = create_playlist('test_user_id', 'test_access_token')
        self.assertEqual(result, 'test_playlist')

    # @patch('flask_collector.requests.get')
    # @patch('flask_collector.put_item')
    # def test_get_topArtist(self, mock_put_item, mock_requests_get):
    #     mock_response = MagicMock()
    #     mock_response.json.return_value = {'items': []}  # Simulate an empty response
    #     mock_requests_get.return_value = mock_response

    #     result = get_topArtist('short_term', 'test_user_id')
    #     self.assertEqual(result, "Artists uploaded to dynamoDB")
    #     self.assertEqual(mock_put_item.call_count, 0)  # No items should be put since the response is empty

if __name__ == '__main__':
    unittest.main()
