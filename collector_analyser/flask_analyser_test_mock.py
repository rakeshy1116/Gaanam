import unittest
from unittest.mock import patch, MagicMock
from flask import json
from flask_analyser import app

class TestAddTracks(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('flask_analyser.get_item')
    @patch('flask_analyser.requests.post')
    def test_add_tracks(self, mock_post, mock_get_item):
        mock_get_item.return_value = {
            'Item': {
                'access_token': {'S': 'mock_token'},
                'playlist_id': {'S': 'mock_playlist'}
            }
        }
        mock_post.return_value = MagicMock(status_code=200, json=lambda: {'status': 'success'})

        response = self.app.post('/addTracks/mock_user', data=json.dumps({'tracks': 'track1,track2'}), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'status': 'success'})

        mock_get_item.assert_called_once_with("user_info", "mock_user")
        mock_post.assert_called_once()

    @patch('flask_analyser.queryByPartKey')
    def test_get_topSong(self, mock_query):
        mock_query.return_value = [
            {
                'track_name': 'mock_song',
                'track_id': 'mock_id',
                'track_artist': 'mock_artist',
                'track_image': 'mock_image',
                'track_preview': 'mock_preview'
            }
        ]

        response = self.app.get('/topSong/short_term/mock_user')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [
            {
                'name': 'mock_song',
                'id': 'mock_id',
                'artist': 'mock_artist',
                'image': 'mock_image',
                'preview': 'mock_preview'
            }
        ])

        mock_query.assert_called_once_with("top_songs_short_term", "mock_user")

    @patch('flask_analyser.queryByPartKey')
    def test_get_topArtist(self, mock_query):
        mock_query.return_value = [
            {
                'artist_name': 'test_artist',
                'artist_id': 'test_id',
                'track_image': 'test_image'
            }
        ]

        response = self.app.get('/topArtist/short_term/test_user')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [
            {
                'name': 'test_artist',
                'id': 'test_id',
                'image': 'test_image'
            }
        ])

        mock_query.assert_called_once_with("top_artists_short_term", "test_user")

    @patch('flask_analyser.get_item')
    @patch('flask_analyser.queryByPartKey')
    @patch('flask_analyser.requests.get')
    def test_get_recommendations(self, mock_get, mock_query, mock_get_item):
        mock_get_item.return_value = {
            'Item': {
                'access_token': {'S': 'test_token'}
            }
        }
        mock_query.return_value = [
            {
                'track_id': 'test_track'
            }
        ]
        mock_get.side_effect = [
            MagicMock(status_code=200, json=lambda: {'tracks': [{'id': 'test_track'}]}),
            MagicMock(status_code=200, json=lambda: {
                'id': 'test_track',
                'name': 'test_name',
                'artists': [{'name': 'test_artist'}],
                'album': {'images': [{'url': 'test_url'}, {'url': 'test_url'}, {'url': 'test_url'}]},
                'preview_url': 'test_preview'
            })
        ]
        response = self.app.get('/recommendations/short_term/test_user')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [
            {
                'id': 'test_track',
                'name': 'test_name',
                'artist': 'test_artist',
                'image': 'test_url',
                'preview': 'test_preview'
            }
        ])

        mock_get_item.assert_called_once_with("user_info", "test_user")
        mock_query.assert_called_once_with("top_songs_short_term", "test_user")
        self.assertEqual(mock_get.call_count, 2)

if __name__ == '__main__':
    unittest.main()