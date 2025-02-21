from helpers import *
from spotify_client import sp  # Import from new file, avoiding circular import

def get_context():
    username, photo_url = get_user_data(sp)
    popularity = get_popularity(sp, 50)
    artists_photos_4w, tracks_photos_4w = get_top_artists_tracks(sp, "short_term")
    artists_photos_6m, tracks_photos_6m = get_top_artists_tracks(sp, "medium_term")
    artists_photos_1y, tracks_photos_1y = get_top_artists_tracks(sp, "long_term")
    curr_track_name, playback, curr_track_photo = get_current_track(sp)

    context = {
        'username': username,
        'photo_url': photo_url,
        'artists_photos_4w': artists_photos_4w,
        'tracks_photos_4w': tracks_photos_4w,
        'artists_photos_6m': artists_photos_6m,
        'tracks_photos_6m': tracks_photos_6m,
        'artists_photos_1y': artists_photos_1y,
        'tracks_photos_1y': tracks_photos_1y,
        'popularity': popularity,
        'curr_track_name': curr_track_name,
        'playback': playback,
        'curr_track_photo': curr_track_photo,
    }
    return context
