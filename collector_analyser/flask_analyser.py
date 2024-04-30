import requests
import urllib.parse
import heapq

from datetime import datetime, timedelta
from flask import Flask, redirect, request, jsonify, session
from flask_cors import CORS, cross_origin
from sqs_util import *
from dynamodb_util import *
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)
app.secret_key = '18ea1408a5c87b8d120e9e5426dc79f56899a637433b88d43211973e1fd5f9c9'
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

CLIENT_ID = 'dd1c295a293049a5970541fbf9a4f615'
CLIENT_SECRET = '703c5ce72af34e95b926b9c6b81d7fec'
REDIRECT_URI = 'http://127.0.0.1:5000/callback'
# REDIRECT_URI = 'https://13.59.32.217/callback'

# CLIENT_ID = '8f72e8cf8eea4ea88025d9ae2782205a'
# CLIENT_SECRET = '72fff3f612d14669b5a04175f1d3983d'
# REDIRECT_URI = 'http://13.59.32.217/callback'
# REDIRECT_URI = 'http://localhost:3001/dashboard'

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'

REQUEST_COUNT = Counter('flask_request_count', 'App Request Count', ['method', 'endpoint', 'http_status'])

@app.route('/')
def index():
    return "Welcome to my Spotify App <a href='/login'>Login with Spotify</a>"

@app.route('/health', methods=['GET', "OPTIONS"])
def health_check():
    print("Health check")
    return jsonify({'status': 'ok'})

@app.route('/login')
def login():
    scope = 'user-read-private user-read-email user-top-read user-read-recently-played playlist-modify-public playlist-modify-private'

    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': REDIRECT_URI,
        'show_dialog': True
    }

    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    return redirect(auth_url)

@app.route('/callback')
def callback():
    if 'error' in request.args:
        return jsonify({"error": requests.args['error']})
    
    if 'code' in request.args:
        req_body = {
            'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }

        response = requests.post(TOKEN_URL, data=req_body)
        token_info = response.json()
        token = token_info['access_token']

        user_id = get_user(token)
        queue_msg_body = {
            'user_id': user_id,
            'access_token': token
        }
        send_message(queue_msg_body)
        # return redirect('https://frontend.d3m1pixii726l5.amplifyapp.com/dashboard?user_id='+user_id)
        return redirect('http://localhost:3000/dashboard?user_id='+user_id)
    
def get_user(token):
    headers = {
        'Authorization': f"Bearer {token}"
    }
    response = requests.get(API_BASE_URL+'me', headers=headers)
    user = response.json()
    user_id = user['id']
    return user_id

@app.route('/topSong/<time_range>/<user_id>')
def get_topSong(time_range, user_id):
    topSongResp = []
    if time_range == 'short_term':
        topSongResp = queryByPartKey("top_songs_short_term", user_id)
    elif time_range == 'medium_term':
        topSongResp = queryByPartKey("top_songs_medium_term", user_id)
    else:
        topSongResp = queryByPartKey("top_songs_long_term", user_id)
    output = []
    for currTrack in topSongResp:
        top_song_name = currTrack['track_name']
        top_song_id =   currTrack['track_id']
        top_song_artist = currTrack['track_artist']
        top_song_image = currTrack['track_image']
        top_song_preview = currTrack['track_preview']
        top_song = {
            'name': top_song_name,
            'id': top_song_id,
            'artist': top_song_artist,
            'image': top_song_image,
            'preview': top_song_preview
        }
        output.append(top_song)
    return jsonify(output)

@app.route('/recommendations/<time_range>/<user_id>')
def get_recommendations(time_range, user_id):
    userInfoResp = get_item("user_info", user_id)
    access_token = userInfoResp['Item']['access_token']['S']
    headers = {
        'Authorization': f"Bearer {access_token}"
    }
    topSongResp = []
    if time_range == 'short_term':
        topSongResp = queryByPartKey("top_songs_short_term", user_id)
    elif time_range == 'medium_term':
        topSongResp = queryByPartKey("top_songs_medium_term", user_id)
    else:
        topSongResp = queryByPartKey("top_songs_long_term", user_id)
    track_ids = []
    for song in topSongResp:
        track_ids.append(song['track_id'])
    # print(f"https://api.spotify.com/v1/recommendations?seed_tracks={'%2C'.join(track_ids[:5])}")
    response = requests.get(f"https://api.spotify.com/v1/recommendations?limit=5&seed_tracks={'%2C'.join(track_ids[:5])}", headers=headers)
    response_json = response.json()
    recommended_tracks = response_json['tracks']
    output=[]
    for currTrack in recommended_tracks:
        id = currTrack['id'] 
        response1 = requests.get(f"https://api.spotify.com/v1/tracks/{id}", headers=headers)
        current_Track = response1.json()
        track = {
            'id': current_Track['id'],
            'name': current_Track['name'],
            'artist': current_Track['artists'][0]['name'],
            'image': current_Track['album']['images'][2]['url'],
            'preview': current_Track['preview_url']
        }
        output.append(track)
    return jsonify(output)

@app.route('/addTracks/<user_id>', methods=['POST'])
def add_tracks(user_id):
    userInfoResp = get_item("user_info", user_id)
    access_token = userInfoResp['Item']['access_token']['S']
    playlist_id = userInfoResp['Item']['playlist_id']['S']
    headers = {
        'Authorization': f"Bearer {access_token}"
    }
    data = request.json
    print(data)
    # user_id = get_user()
    # playlist_id = data['playlist_id']
    track_ids = data['tracks'].split(',')
    track_ids1 = []
    for track in track_ids:
        track_ids1.append("spotify:track:"+track)
    print(user_id, playlist_id, track_ids1)
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    print(url)
    req_body = {
        'uris': track_ids1
    }
    response = requests.post(url, headers=headers, json=req_body)
    print(response)
    return response.json()

@app.route('/topArtist/<time_range>/<user_id>')
def get_topArtist(time_range, user_id):
    topArtistResp = []
    if time_range == 'short_term':
        topArtistResp = queryByPartKey("top_artists_short_term", user_id)
    elif time_range == 'medium_term':
        topArtistResp = queryByPartKey("top_artists_medium_term", user_id)
    else:
        topArtistResp = queryByPartKey("top_artists_long_term", user_id)
    output = []
    for currArtist in topArtistResp:
        top_artist_name = currArtist['artist_name']
        top_artist_id = currArtist['artist_id']
        top_artist_image = currArtist['track_image']
        top_artist = {
            'name': top_artist_name,
            'id': top_artist_id,
            'image': top_artist_image
        }
        output.append(top_artist)
    return jsonify(output)

@app.route('/metrics')
def metrics():
   return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@app.after_request
def after_request(response):
   if(request.path == '/metrics'):
       return response
   REQUEST_COUNT.labels(request.method, request.path.split("/")[1], response.status_code).inc()
   return response

if __name__ == '__main__':
    #app.run(debug=True, ssl_context="adhoc")
    app.run(debug=True)