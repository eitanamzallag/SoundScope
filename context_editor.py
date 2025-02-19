from helpers import *
from main import sp

def get_context():
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
    return context
