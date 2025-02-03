from flask import redirect
import requests

def check_token(sp_oauth, cache_handler):
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)


def get_user_data(sp):
    all = sp.current_user()
    username = sp.current_user()['display_name']
    photo_url = sp.current_user()['images'][1]['url']
    return username, photo_url


def get_top_artists_tracks(sp):
    top_artists = sp.current_user_top_artists(limit=10)
    artists_photos = {}
    for i in top_artists['items']:
        artist = i['name']
        photo = i['images'][0]['url']
        artists_photos[artist] = photo
    top_tracks = sp.current_user_top_tracks(limit=10)
    tracks_photos = {}
    for i in top_tracks['items']:
        track = i['name']
        photo = i['album']['images'][0]['url']
        tracks_photos[track] = photo
    return artists_photos, tracks_photos

def get_popularity(sp, lim):
    sum = 0
    top_tracks = sp.current_user_top_tracks(limit=lim)
    for track in top_tracks['items']:
        sum += track['popularity']

    return int((sum/lim))