import os
from flask import Flask, session, url_for, request, redirect, render_template
from dotenv import load_dotenv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler
from helpers import *

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
context = {} # variables to pass to the html file

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
    check_token(sp_oauth, cache_handler)
    return redirect(url_for('top_stats'))

@app.route('/callback')
def callback():
    sp_oauth.get_cached_token()
    return redirect(url_for('top_stats'))


@app.route('/top_stats')
def top_stats():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)

    username, photo_url = get_user_data(sp)

    artists, tracks = get_top_artists_tracks(sp)
    context = {
        'username' : username,
        'photo_url' : photo_url,
        'artists' : artists,
        'tracks' : tracks
    }

    return render_template('index.html', **context)

if __name__ == '__main__':
    app.run(debug=True)
