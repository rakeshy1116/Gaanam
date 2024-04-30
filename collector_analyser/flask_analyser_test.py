import unittest
from flask_testing import TestCase
from flask import Flask
from flask_analyser import app

class FlaskTestCase(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome to my Spotify App", response.data)

    def test_health_check(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'status': 'ok'})

    def test_login(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 302)  # Expecting a redirect

    def test_topSong(self):
        response = self.client.get('/topSong/short_term/31d4tpb5akuckk3k2i6yazjglnaq')
        self.assertEqual(response.status_code, 200)
   
    def test_add_tracks(self):
        response = self.client.post('/addTracks/31d4tpb5akuckk3k2i6yazjglnaq', json={'tracks': 'track1,track2'})
        self.assertEqual(response.status_code, 200)

    def test_get_topArtist(self):
        response = self.client.get('/topArtist/short_term/31d4tpb5akuckk3k2i6yazjglnaq')
        self.assertEqual(response.status_code, 200)

    def test_metrics(self):
        response = self.client.get('/metrics')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()