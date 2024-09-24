from flask import redirect

def get_user_data(sp):
    all = sp.current_user()
    username = sp.current_user()['display_name']
    photo_url = sp.current_user()['images'][1]['url']
    return username, photo_url


def get_top_artists_tracks(sp):
    top_artists = sp.current_user_top_artists(limit=10)
    artists = [artist['name'] for artist in top_artists['items']]
    top_tracks = sp.current_user_top_tracks(limit=10)
    tracks = [track['name'] for track in top_tracks['items']]
    return artists, tracks


def check_token(sp_oauth, cache_handler):
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    return None
