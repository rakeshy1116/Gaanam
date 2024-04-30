import requests
# import urllib.parse
# import heapq
# from datetime import datetime, timedelta
# from flask import Flask, redirect, request, jsonify, session
# from flask_cors import CORS, cross_origin
import boto3
from datetime import datetime
from sqs_util import *
from dynamodb_util import *

API_BASE_URL = 'https://api.spotify.com/v1/'

def read_sqs_message():
    message = receive_message()
    return message

def get_topSong(time_range,user_id):
    item = get_item("user_info", user_id)
    access_token = item['Item']['access_token']['S']
    headers = {
        'Authorization': f"Bearer {access_token}"
    }
    response = requests.get(API_BASE_URL+'me/top/tracks?time_range='+time_range, headers=headers)
    tracks = response.json()
    list_of_tracks = tracks['items']
    count = 0
    for currTrack in list_of_tracks:
        top_song_name = currTrack['name']
        top_song_id =   currTrack['id']
        top_song_artist = currTrack['artists'][0]['name']
        top_song_image = currTrack['album']['images'][2]['url']
        top_song_preview = currTrack['preview_url']
        song_item = create_song(user_id, count, top_song_name, top_song_id, top_song_artist, top_song_image, top_song_preview, False,time_range,str(int(datetime.now().timestamp()) + 3600))
        # output.append(top_song)
        print('top_songs_'+time_range)
        put_item('top_songs_'+time_range,song_item)
        # print(song_item)
        count += 1
        if(count == 10):
            break
    return "Uploaded songs to dynamoDB"

def create_playlist(user_id,access_token):
    headers = {
        'Authorization': f"Bearer {access_token}"
    }
    url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    req_body = {
        'name': "From Gaanam with Love",
        'description': "Reaching out to you with the best of music!",
        'public': True
    }
    response = requests.post(url, headers=headers, json=req_body)
    data = response.json()
    print(data)
    playlist_id = data['external_urls']['spotify'].split('/')[-1]
    print(playlist_id)
    # return playlist_id
    return playlist_id


def get_topArtist(time_range,user_id):
    item = get_item("user_info", user_id)
    access_token = item['Item']['access_token']['S']
    headers = {
        'Authorization': f"Bearer {access_token}"
    }
    response = requests.get(API_BASE_URL+'me/top/artists?time_range='+time_range, headers=headers)
    artists = response.json()
    list_of_artists = artists['items']
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
        
        artist_item = create_artist(user_id, count, top_artist_name, top_artist_id, top_artist_image, time_range, str(int(datetime.now().timestamp()) + 3600))
        # output.append(top_song)
        print('top_artists_'+time_range)
        put_item('top_artists_'+time_range,artist_item)
        count+=1
        if(count == 10):
            break
       

    return "Artists uploaded to dynamoDB"


if __name__ == '__main__':
    while True:
        message = read_sqs_message()
        # playlist_id = create_playlist("31d4tpb5akuckk3k2i6yazjglnaq","BQBQ4e_WRtN3XXY2rDGJ131xqHSmwskfRMa_QPKNo7ZMC2DIWgmC0wXBQzh7UIGUjqjKbsxSef_sHoCHdQkkS2HhlArb8wErcv-bju8Scz8tNxmxDgdIJKp1TE0DQS8lfzC_-hCPHi7zXz2ZL4ELZ25nI_ZI6fqwJZ83ZnH7JsudfP_BEkgg4rH5QidxBcfJU47TlyRhhxew4dbiPcZ3EZYKkCvsA7YR68-UadHzYDa-e9YOwF34QAC7eveQpZGvWohqK9IzuU0-xjUC81cr5zCPeq-6")
        playlist_id = create_playlist(message['user_id'],message['access_token'])
        put_item('user_info', create_user(message['user_id'], message['access_token'], playlist_id))
        get_topSong("short_term",message['user_id'])
        get_topSong("medium_term",message['user_id'])
        get_topSong("long_term",message['user_id'])
        get_topArtist("short_term",message['user_id'])
        get_topArtist("medium_term",message['user_id'])
        get_topArtist("long_term",message['user_id'])