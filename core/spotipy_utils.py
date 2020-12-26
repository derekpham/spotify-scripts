from spotipy import Spotify
from typing import List


def _list_of_uris_helper(playlist, uris: List[str], spotify_method):
    playlist_id = playlist['id']
    curr = 0
    offset = 100
    while curr < len(uris):
        spotify_method(playlist_id, uris[curr: curr + offset])
        curr += offset


def delete_all_tracks(sp: Spotify, playlist, uris: List[str]):
    _list_of_uris_helper(playlist, uris, sp.playlist_remove_all_occurrences_of_items)


def add_all_tracks(sp: Spotify, playlist, uris: List[str]):
    _list_of_uris_helper(playlist, uris, sp.playlist_add_items)


def retrieve_all_tracks_for_playlist(sp: Spotify, playlist, fields=None):
    if fields is not None:
        fields = f'next,{fields}'

    all_items = []

    results = sp.playlist_items(playlist_id=playlist['id'], limit=50, fields=fields)
    while True:
        all_items.extend(results['items'])

        results = sp.next(results)
        if results is None:
            break
    return all_items


def playlist_size(sp: Spotify, playlist_name: str):
    playlist = search_playlist_in_current_user_library(sp, playlist_name)
    if playlist is None:
        return None
    else:
        return playlist['tracks']['total']


def search_playlist_in_current_user_library(sp: Spotify, playlist_name: str):
    """
    Searches for a playlist within the current user's library with the given name (case insensitive)
    (I don't think Spotify API offers the ability to search for a playlist within a user's library
    yet. See note section here:
    https://developer.spotify.com/documentation/web-api/reference/search/search/)
    """

    batch_results = sp.current_user_playlists(limit=50)
    while True:
        for playlist in batch_results['items']:
            if playlist['name'].lower() == playlist_name.lower():
                return playlist

        batch_results = sp.next(batch_results)

        if batch_results is None:
            break

    return None
