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


def get_top_artists_tracks(sp, range):
    top_artists = sp.current_user_top_artists(limit=14, time_range = range)
    artists_photos = {}
    for i in top_artists['items']:
        artist = i['name']
        photo = i['images'][0]['url']
        artists_photos[artist] = photo
    top_tracks = sp.current_user_top_tracks(limit=14, time_range = range)
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

    popularity_descriptions = {
    0: "Your music taste is truly unique—you're discovering hidden gems before anyone else!",
    1: "You’re on the fringe of mainstream—your taste is rare but appreciated by a select few.",
    2: "You're still off the beaten path, enjoying underrated tracks with a growing audience.",
    3: "A mix of niche and known—your taste balances individuality with some mainstream appeal.",
    4: "Right in the middle! Your playlist has both underground hits and popular favorites.",
    5: "You enjoy the best of both worlds—mainstream hits with a touch of personal flair.",
    6: "Your music taste is widely appreciated, featuring popular tracks with some unique picks.",
    7: "You’re in tune with trending music—your taste aligns closely with what’s popular now.",
    8: "Your playlists are filled with crowd-pleasers—your music taste is a hit with the masses!",
    9: "You have peak mainstream taste! Your favorite songs dominate the charts and playlists."
    }


    return int((sum/lim)), popularity_descriptions[int((sum/lim)/10)]

def get_current_track(sp):
    track = sp.currently_playing()
    if track is None:
        return {"track_name": "No track playing", "playback": False, "track_photo": "https://static.thenounproject.com/png/173320-200.png"}
    track_name = track['item']['name']
    playback = track['is_playing']
    track_photo = track['item']['album']['images'][0]['url']
    return {"track_name": track_name, "playback": playback, "track_photo": track_photo}

