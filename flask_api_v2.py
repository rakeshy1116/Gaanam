import requests
import urllib.parse
import heapq

from datetime import datetime, timedelta
from flask import Flask, redirect, request, jsonify, session
from flask_cors import CORS, cross_origin
from sqs_util import *

app = Flask(__name__)
app.secret_key = '18ea1408a5c87b8d120e9e5426dc79f56899a637433b88d43211973e1fd5f9c9'
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
session = {}
CLIENT_ID = 'dd1c295a293049a5970541fbf9a4f615'
CLIENT_SECRET = '703c5ce72af34e95b926b9c6b81d7fec'
REDIRECT_URI = 'http://127.0.0.1:5000/callback'

# CLIENT_ID = '8f72e8cf8eea4ea88025d9ae2782205a'
# CLIENT_SECRET = '72fff3f612d14669b5a04175f1d3983d'
# REDIRECT_URI = 'http://13.59.32.217/callback'
# REDIRECT_URI = 'http://localhost:3001/dashboard'

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'

# token = 'BQDRJLmdJ9eDduDIZWOs0-cIfyy6sbQJqn5ynduvjBU1UzCuDqiy3GH9Cw443UDOyC8bReLXPeDrUJv-S_-G22q4BeyMPrJt4tKWORQVz2fLHAn8LLvEwo_l7vjhIbkftOAf4idj1IG17iFYwYsJQfCxUJCOla_aCUDJ9iJzct8OU3KoLeydwSAZ-42LjxhN92zj5d6ASlWr-qSuwRfYrAXTU9CoaAAGIw'
token = ""
@app.route('/')
def index():
    return "Welcome to my Spotify App <a href='/login'>Login with Spotify</a>"

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
    # redirect(auth_url)
    # callback()
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

        print(token_info['access_token'])
        token = token_info['access_token']
        session['access_token'] = token_info['access_token']
        session['refresh_token'] = token_info['refresh_token']
        session['expires_in'] = datetime.now().timestamp() + token_info['expires_in']
        print(session)

        user_id = get_user()
        queue_msg_body = {
            'user_id': user_id,
            'access_token': token
        }
        send_message(queue_msg_body)
        # return redirect('https://frontend.d3m1pixii726l5.amplifyapp.com/dashboard')
        return redirect('http://localhost:3001/dashboard')


@app.route('/playlists')
def get_playlists():
    if 'access_token' not in session:
        return redirect('/login')

    # if datetime.now().timestamp() > session['expires_at']:
    #     return redirect('/refresh-token')
    print(session['access_token'])
    # token = "BQDvgwYP9l8UuGqUf-OBtw7T9AjOe0OpKpX-3rEhzJihlKi3NEJah22VqHoOQxycGlCl2upx3mXMwGoZgapSt1J70jfj5CW-PH_1YiEOrMBIjAEb0SZJloH80E_6VKu5VfpR4iBo2Lh12Md51d8LdJ3WBv_WTRm48EzQhDV7GbTq232ZvWs5xq5zKRopLfPHqhrKm1fCItcim_6fS80cMYhFUiCV-ch1BA"

    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }
    
    response = requests.get(API_BASE_URL+'me/top/tracks?time_range=short_term', headers=headers)
    print(response)
    playlists = response.json()
    return jsonify(playlists)

@app.route('/topSong/<time_range>')
def get_topSong(time_range):
    # if 'access_token' not in session:
    #     return redirect('/login')
    print("In topSong")
    print(session)
    if 'access_token' not in session:
        return redirect('/login')
    # if datetime.now().timestamp() > session['expires_at']:
    #     return redirect('/refresh-token')
    # print(session['access_token'])
    # token = "BQDvgwYP9l8UuGqUf-OBtw7T9AjOe0OpKpX-3rEhzJihlKi3NEJah22VqHoOQxycGlCl2upx3mXMwGoZgapSt1J70jfj5CW-PH_1YiEOrMBIjAEb0SZJloH80E_6VKu5VfpR4iBo2Lh12Md51d8LdJ3WBv_WTRm48EzQhDV7GbTq232ZvWs5xq5zKRopLfPHqhrKm1fCItcim_6fS80cMYhFUiCV-ch1BA"
    # print(token)
    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }
    
    response = requests.get(API_BASE_URL+'me/top/tracks?time_range='+time_range, headers=headers)
    print(response)
    tracks = response.json()
    print("I am printing this  = ",tracks)
    list_of_tracks = tracks['items']
    output = []
    count = 0
    for currTrack in list_of_tracks:
        top_song_name = currTrack['name']
        top_song_id =   currTrack['id']
        top_song_artist = currTrack['artists'][0]['name']
        top_song_image = currTrack['album']['images'][2]['url']
        top_song_preview = currTrack['preview_url']
        top_song = {
            'name': top_song_name,
            'id': top_song_id,
            'artist': top_song_artist,
            'image': top_song_image,
            'preview': top_song_preview
        }
        output.append(top_song)
        count += 1
        if(count == 5):
            break

    top_tracks = list_of_tracks[0]

    
    return jsonify(output)

@app.route('/health', methods=['GET', "OPTIONS"])
def health_check():
    print("Health check")
    return jsonify({'status': 'ok'})

@app.route('/topArtist/<time_range>')
def get_topArtist(time_range):
    if 'access_token' not in session:
        return redirect('/login')

    # if datetime.now().timestamp() > session['expires_at']:
    #     return redirect('/refresh-token')
    # token = "BQDvgwYP9l8UuGqUf-OBtw7T9AjOe0OpKpX-3rEhzJihlKi3NEJah22VqHoOQxycGlCl2upx3mXMwGoZgapSt1J70jfj5CW-PH_1YiEOrMBIjAEb0SZJloH80E_6VKu5VfpR4iBo2Lh12Md51d8LdJ3WBv_WTRm48EzQhDV7GbTq232ZvWs5xq5zKRopLfPHqhrKm1fCItcim_6fS80cMYhFUiCV-ch1BA"

    print(session['access_token'])
    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }
    
    response = requests.get(API_BASE_URL+'me/top/artists?time_range='+time_range, headers=headers)
    print(response)
    artists = response.json()
    list_of_artists = artists['items']
    output = []
    count = 0
    for curArtist in list_of_artists:
        top_artist_name = curArtist['name']
        top_artist_id =   curArtist['id']
        top_artist_image = curArtist['images'][2]['url']
        top_artist = {
            'name': top_artist_name,
            'id': top_artist_id,
            'image': top_artist_image
        }
        count+=1
        if(count == 4):
            break
        output.append(top_artist)
    print(jsonify(output))
    return jsonify(output)

@app.route('/user')
def get_user():
    if 'access_token' not in session:
        return redirect('/login')
    print(session['access_token'])
    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }
    response = requests.get(API_BASE_URL+'me', headers=headers)
    user = response.json()
    user_id = user['id']
    return user_id

@app.route('/createPlaylist', methods=['POST'])
def create_playlist():
    if 'access_token' not in session:
        return redirect('/login')
    print(session['access_token'])
    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }
    data = request.json
    print(data)
    # user_id = data['user_id']
    # data1 = get_user().json()
    user_id = get_user()
    playlist_name = data['playlist_name']
    playlist_description = data['playlist_description']
    playlist_public = data['playlist_public']
    print(user_id, playlist_name, playlist_description, playlist_public)
    url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    print(url)
    req_body = {
        'name': playlist_name,
        'description': playlist_description,
        'public': playlist_public
    }
    response = requests.post(url, headers=headers, json=req_body)
    print(response)
    return response.json()

@app.route('/addTracks', methods=['POST'])
def add_tracks():
    if 'access_token' not in session:
        return redirect('/login')
    print(session['access_token'])
    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }
    data = request.json
    print(data)
    user_id = get_user()
    playlist_id = data['playlist_id']
    track_ids = data['tracks']
    print(user_id, playlist_id, track_ids)
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    print(url)
    req_body = {
        'uris': track_ids
    }
    response = requests.post(url, headers=headers, json=req_body)
    print(response)
    return response.json()

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
    top_3_keys = heapq.nlargest(3, genreDictionary, key=genreDictionary.get)
    return jsonify(top_3_keys)

@app.route('/totalMinutes')
def get_totalMinutes():
    if 'access_token' not in session:
        return redirect('/login')
    print(session['access_token'])

    # token = "BQDvgwYP9l8UuGqUf-OBtw7T9AjOe0OpKpX-3rEhzJihlKi3NEJah22VqHoOQxycGlCl2upx3mXMwGoZgapSt1J70jfj5CW-PH_1YiEOrMBIjAEb0SZJloH80E_6VKu5VfpR4iBo2Lh12Md51d8LdJ3WBv_WTRm48EzQhDV7GbTq232ZvWs5xq5zKRopLfPHqhrKm1fCItcim_6fS80cMYhFUiCV-ch1BA"

    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }
    curr_time = datetime.now()
    four_weeks_ago = curr_time - timedelta(weeks=4)
    four_weeks_ago_timeStamp = int(four_weeks_ago.timestamp()*1000)
    response = requests.get(API_BASE_URL+'me/player/recently-played?limit=50&after='+str(four_weeks_ago_timeStamp), headers=headers)
    response_json = response.json()
    list_of_tracks = response_json['items']
    totalDuration = 0
    for currTrack in list_of_tracks:
        totalDuration += int(currTrack["track"]["duration_ms"])
    totalSec = totalDuration/1000
    totalHours = totalSec // 3600
    totalMins = (totalSec%3600) // 60
    totalTime = str(totalHours) + " hours " + str(totalMins) +" mins"
    return jsonify(totalTime)


@app.route('/recommendations/<time_range>')
def get_recommendations(time_range):
    if 'access_token' not in session:
        return redirect('/login')
    print(session['access_token'])
    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }
    output = get_topSong(time_range)
    # songs = output.json()
    # print(songs)
    track_ids = []
    for song in output:
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
