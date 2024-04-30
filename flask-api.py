import requests
import urllib.parse
import heapq

from datetime import datetime, timedelta
from flask import Flask, redirect, request, jsonify, session

app = Flask(__name__)
app.secret_key = '18ea1408a5c87b8d120e9e5426dc79f56899a637433b88d43211973e1fd5f9c9'

# CLIENT_ID = 'dd1c295a293049a5970541fbf9a4f615'
# CLIENT_SECRET = '703c5ce72af34e95b926b9c6b81d7fec'
# REDIRECT_URI = 'http://127.0.0.1:5000/callback'

session = {}

CLIENT_ID = '8f72e8cf8eea4ea88025d9ae2782205a'
CLIENT_SECRET = '72fff3f612d14669b5a04175f1d3983d'
REDIRECT_URI = 'http://127.0.0.1:5000/callback'

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'

@app.route('/')
def index():
    return "Welcome to my Spotify App <a href='/login'>Login with Spotify</a>"

@app.route('/login')
def login():
    scope = 'user-read-private user-read-email user-top-read user-read-recently-played'

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
    print("You are here")
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

        print("Token_info")
        print(token_info['access_token'])

        session['access_token'] = token_info['access_token']
        session['refresh_token'] = token_info['refresh_token']
        session['expires_in'] = datetime.now().timestamp() + token_info['expires_in']

        return redirect('/user')

@app.route('/user')
def get_user():
    if 'access_token' not in session:
        return redirect('/login')

    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }

    response = requests.get(API_BASE_URL+'me', headers=headers)
    user = response.json()

    return jsonify(user)

@app.route('/playlists')
def get_playlists():
    if 'access_token' not in session:
        return redirect('/login')

    # if datetime.now().timestamp() > session['expires_at']:
    #     return redirect('/refresh-token')
    print(session['access_token'])
    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }
    
    response = requests.get(API_BASE_URL+'me/top/artists?time_range=short_term', headers=headers)
    response = requests.get(API_BASE_URL+'me/top/artists?time_range=short_term', headers=headers)
   
    # print(response)
    # playlists = response.json()

    return response

@app.route('/topSong')
def get_topSong():
    if 'access_token' not in session:
        return redirect('/login')

    # if datetime.now().timestamp() > session['expires_at']:
    #     return redirect('/refresh-token')
    print(session['access_token'])
    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }
    
    response = requests.get(API_BASE_URL+'me/top/tracks?time_range=short_term', headers=headers)
    print(response)
    tracks = response.json()
    list_of_tracks = tracks['items']
    output = []
    for currTrack in list_of_tracks:
        track = {
            'name': currTrack['name'],
            'id': currTrack['id'],
            'artist': currTrack['artists'][0]['name'],
            'image': currTrack['album']['images'][2]['url'],
            'preview': currTrack['preview_url']
        }
        output.append(track)
    return output

@app.route('/topArtist')
def get_topArtist():
    if 'access_token' not in session:
        return redirect('/login')

    # if datetime.now().timestamp() > session['expires_at']:
    #     return redirect('/refresh-token')
    print(session['access_token'])
    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }
    
    response = requests.get(API_BASE_URL+'me/top/artists?time_range=short_term', headers=headers)
    print(response)
    artists = response.json()
    list_of_artists = artists['items']
    top_artist = list_of_artists[0]
    top_artist_name = top_artist['name']
    top_artist_id =   top_artist['id']
    top_artist_image = top_artist['images'][0]['url']
    top_artist = {
        'name': top_artist_name,
        'id': top_artist_id,
        'image': top_artist_image
    }
    return jsonify(top_artist)

@app.route('/topGenres')
def get_topGenres():
    if 'access_token' not in session:
        return redirect('/login')
    print(session['access_token'])
    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }

    response = requests.get(API_BASE_URL+'me/top/artists?time_range=short_term', headers=headers)
    tracks = response.json()
    list_of_tracks = tracks['items']
    genreDictionary = {}
    for currTrack in list_of_tracks:
        currGenres = currTrack['genres']
        for genre in currGenres:
            genreDictionary[genre] = genreDictionary.get(genre, 0)+1
    # sorted_genreDict = dict(sorted(genreDictionary.items(), key=lambda item: item[1], reverse=True))
    top_3_keys = heapq.nlargest(5, genreDictionary, key=genreDictionary.get)
    return jsonify(top_3_keys)

@app.route('/totalMin')
def get_totalMin():
    if 'access_token' not in session:
        return redirect('/login')
    print(session['access_token'])
    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }
    return "Total minutes"

@app.route('/totalMinutes')
def get_totalMinutes():
    if 'access_token' not in session:
        return redirect('/login')
    print(session['access_token'])
    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }
    curr_time = datetime.now()
    four_weeks_ago = curr_time - timedelta(weeks=4)
    four_weeks_ago_timeStamp = int(four_weeks_ago.timestamp()*1000)
    response = requests.get(API_BASE_URL+'me/player/recently-played?limit=50&after='+str(four_weeks_ago_timeStamp), headers=headers)
    response_json = response.json()
    # return jsonify(response_json)
    list_of_tracks = response_json['items']
    totalDuration = 0
    for currTrack in list_of_tracks:
        totalDuration += int(currTrack["track"]["duration_ms"])
    totalSec = totalDuration/1000
    totalHours = totalSec // 3600
    totalMins = (totalSec%3600) // 60
    totalTime = str(totalHours) + " hours " + str(totalMins) +" mins"
    return jsonify(totalTime)

@app.route('/recommendations')
def get_recommendations():
    if 'access_token' not in session:
        return redirect('/login')
    print(session['access_token'])
    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }
    songs = get_topSong()
    track_ids = []
    for song in songs:
        track_ids.append(song['id'])
    print(f"https://api.spotify.com/v1/recommendations?seed_tracks={'%2C'.join(track_ids[:2])}")
    response = requests.get(f"https://api.spotify.com/v1/recommendations?seed_tracks={'%2C'.join(track_ids[:2])}", headers=headers)
    response_json = response.json()
    recommended_tracks = response_json['tracks']
    output = []
    for currTrack in recommended_tracks:
        track = {
            'name': currTrack['name'],
            'id': currTrack['id'],
            'artist': currTrack['artists'][0]['name'],
            'image': currTrack['album']['images'][2]['url'],
            'preview': currTrack['preview_url']
        }
        output.append(track)
    return output


if __name__ == '__main__':
    app.run(debug=True)