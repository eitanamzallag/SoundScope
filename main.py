import os
from flask import Flask, session, url_for, request, redirect
from dotenv import load_dotenv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler

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

def check_login(mainpage):
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    return redirect(url_for(mainpage))

@app.route('/')
def home():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    return redirect(url_for('top_stats'))

@app.route('/callback')
def callback():
    sp_oauth.get_access_token(request.args['code'])
    return redirect(url_for('top_stats'))

@app.route('/top_stats')
def top_stats():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)

    top_artists = sp.current_user_top_artists(limit=10)
    artists = [artist['name'] for artist in top_artists['items']]
    top_tracks = sp.current_user_top_tracks(limit=10)
    tracks = [track['name'] for track in top_tracks['items']]
    all = artists + tracks
    return all

if __name__ == '__main__':
    app.run(debug=True)
