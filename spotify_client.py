import os
from flask import session
from dotenv import load_dotenv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler

# Load environment variables
load_dotenv()

# Spotify API credentials
client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
redirect_uri = os.getenv('redirect_uri')
scope = os.getenv('scope')

# Spotify authentication
cache_handler = FlaskSessionCacheHandler(session)
sp_oauth = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    cache_handler=cache_handler,
    show_dialog=True
)
sp = Spotify(auth_manager=sp_oauth)
