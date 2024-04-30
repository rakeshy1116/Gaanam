from flask import Flask, request, jsonify
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

artistsDict = {
    "RIHANNA": "5pKCCKE2ajJHZ9KAiaK11H",
    "TAYLOR SWIFT": "06HL4z0CvFAxyc27GXpf02",
    "ARIJIT SINGH": "4YRxDV8wJFPHPTeXepOstw",
    "ED SHEERAN": "6eUKZXaKkcviH0Ku9w2n3V",
    "JUSTIN BIEBER": "1uNFoZAHBGtllmzznpCI3s",
    "SHREYA GHOSHAL": "0oOet2f43PA68X5RxKobEy",
    "BTS": "3Nrfpe0tUJi4K4DXYWgMUX"
}

@app.route('/health', methods=['GET'])
def health_check():
    print("Health check")
    return jsonify({'status': 'ok'})

@app.route('/submit', methods=['POST'])
@cross_origin()
def handle_submit():
    request_data = request.get_json()
    print(request_data)
    artist = request_data["artist"]
    if artist.upper() in artistsDict:
        artist_id = artistsDict[artist.upper()]
        spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
        results = spotify.artist(artist_id)
        artist_url = results["external_urls"]["spotify"]
        artist_name = results["name"]
        artist_popularity = results["popularity"]
        response = {
                    'artist_url': artist_url,
                    'artist_name': artist_name,
                    'artist_popularity': artist_popularity,
                }
        return jsonify(response)
    else:
        return jsonify({'error': 'Artist not found'})

if __name__ == '__main__':
    app.run(debug=True)
