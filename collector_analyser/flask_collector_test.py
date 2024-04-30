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

    @patch('flask_collector.get_item')
    @patch('flask_collector.requests.get')
    @patch('flask_collector.create_song')
    @patch('flask_collector.put_item')
    def test_get_topSong(self, mock_put_item, mock_create_song, mock_requests_get, mock_get_item):
        mock_get_item.return_value = {'Item': {'access_token': {'S': 'test_token'}}}
        mock_requests_get.return_value.json.return_value = {
            'items': [
                {
                    'name': 'test_song',
                    'id': 'test_id',
                    'artists': [{'name': 'test_artist'}],
                    'album': {'images': [{'url': 'test_url'}, {'url': 'test_url'}, {'url': 'test_url'}]},
                    'preview_url': 'test_preview_url'
                }
            ] * 10
        }
        mock_create_song.return_value = 'test_song_item'
        time_range = 'test_time_range'
        user_id = 'test_user_id'

        result = get_topSong(time_range, user_id)


        self.assertEqual(result, "Uploaded songs to dynamoDB")
        mock_get_item.assert_called_once_with("user_info", user_id)
        mock_requests_get.assert_called_once()
        self.assertEqual(mock_create_song.call_count, 10)
        self.assertEqual(mock_put_item.call_count, 10)

    @patch('flask_collector.requests.post')
    def test_create_playlist(self, mock_requests_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {'external_urls': {'spotify': 'https://spotify.com/playlist/test_playlist'}}
        mock_requests_post.return_value = mock_response

        result = create_playlist('test_user_id', 'test_access_token')
        self.assertEqual(result, 'test_playlist')

    @patch('flask_collector.get_item')
    @patch('flask_collector.requests.get')
    @patch('flask_collector.create_artist')
    @patch('flask_collector.put_item')
    def test_get_topArtist(self, mock_put_item, mock_create_artist, mock_requests_get, mock_get_item):
        mock_get_item.return_value = {'Item': {'access_token': {'S': 'test_token'}}}
        mock_requests_get.return_value.json.return_value = {
            'items': [
                {
                    'name': 'test_artist',
                    'id': 'test_id',
                    'images': [{'url': 'test_url'}, {'url': 'test_url'}, {'url': 'test_url'}],
                }
            ] * 10
        }
        mock_create_artist.return_value = 'test_song_item'
        time_range = 'test_time_range'
        user_id = 'test_user_id'

        result = get_topArtist(time_range, user_id)

        self.assertEqual(result, "Artists uploaded to dynamoDB")
        mock_get_item.assert_called_once_with("user_info", user_id)
        mock_requests_get.assert_called_once()
        self.assertEqual(mock_create_artist.call_count, 10)
        self.assertEqual(mock_put_item.call_count, 10)

if __name__ == '__main__':
    unittest.main()