import os
from flask import Flask, session, url_for, request, redirect, render_template, jsonify
from dotenv import load_dotenv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler
from helpers import *

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')

client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
redirect_uri = os.getenv('redirect_uri')
scope = os.getenv('scope')

cache_handler = FlaskSessionCacheHandler(session)
sp_oauth = SpotifyOAuth(client_id=client_id,
                        client_secret=client_secret,
                        redirect_uri=redirect_uri,
                        scope=scope,
                        cache_handler=cache_handler,
                        show_dialog=True)

sp = Spotify(auth_manager=sp_oauth)


@app.route('/')
def home():
    token_info = cache_handler.get_cached_token()
    if not token_info or not sp_oauth.validate_token(token_info):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    return redirect(url_for('top_stats'))

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return "Error: Authorization code not provided."
    sp_oauth.get_access_token(code)
    return redirect(url_for('top_stats'))

@app.route("/current_song")
def current_song():
    return jsonify(get_current_track(sp))

@app.route('/top_stats')
def top_stats():
    token_info = cache_handler.get_cached_token()
    if not token_info or not sp_oauth.validate_token(token_info):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)

    username, photo_url = get_user_data(sp)
    popularity = get_popularity(sp, 50)
    artists_photos, tracks_photos = get_top_artists_tracks(sp)
    curr_track_name, playback, curr_track_photo = get_current_track(sp)
    context = {
        'username': username,
        'photo_url': photo_url,
        'artists_photos': artists_photos,
        'tracks_photos': tracks_photos,
        'popularity': popularity,
        'curr_track_name': curr_track_name,
        'playback': playback,
        'curr_track_photo': curr_track_photo
    }
    return render_template('index.html', **context)

if __name__ == '__main__':
    app.run(port=5001, debug=True)