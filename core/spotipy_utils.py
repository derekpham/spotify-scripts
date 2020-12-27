from spotipy import Spotify, SpotifyOAuth
from typing import List, Optional
import datetime

from core.Track import Track


class SpotipyUtils:
    def __init__(self, client_id, client_secret, redirect_uri, scope):
        self._sp = Spotify(
            auth_manager=SpotifyOAuth(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=redirect_uri,
                scope=scope
            )
        )

    def delete_all_tracks(self, playlist):
        """
        Deletes all tracks in the given playlist
        """

        tracks = self.retrieve_all_tracks_for_playlist(playlist)
        SpotipyUtils._list_of_uris_helper(
            playlist,
            tracks,
            self._sp.playlist_remove_all_occurrences_of_items
        )

    def add_all_tracks(self, playlist, tracks: List[Track]):
        """
        Adds all the tracks to the given playlist
        """

        SpotipyUtils._list_of_uris_helper(playlist, tracks, self._sp.playlist_add_items)

    def retrieve_all_tracks_for_playlist(self, playlist) -> List[Track]:
        """
        Retrieves all tracks for the given playlist
        """

        fields = 'next,' \
                 'items(track(name,album(release_date,release_date_precision),artists(name),uri))'
        all_items = []

        results = self._sp.playlist_items(playlist_id=playlist['id'], limit=50, fields=fields)
        while True:
            all_items.extend(results['items'])

            results = self._sp.next(results)
            if results is None:
                break

        return [SpotipyUtils.to_track(item) for item in all_items]

    def num_tracks_in_playlist(self, playlist) -> Optional[int]:
        """
        Returns the number of tracks in this playlist
        """

        playlist = self.search_playlist_in_current_user_library(playlist['name'])
        if playlist is None:
            return None
        return len(self.retrieve_all_tracks_for_playlist(playlist))

    # TODO: have a class to represent playlist?
    def search_playlist_in_current_user_library(self, playlist_name: str):
        """
        Searches for a playlist within the current user's library with the given name
        (case insensitive)
        (I don't think Spotify API offers the ability to search for a playlist within
        a user's library yet. See note section here:
        https://developer.spotify.com/documentation/web-api/reference/search/search/)
        """

        batch_results = self._sp.current_user_playlists(limit=50)
        while True:
            for playlist in batch_results['items']:
                if playlist['name'].lower() == playlist_name.lower():
                    return playlist

            batch_results = self._sp.next(batch_results)

            if batch_results is None:
                break

        return None

    def create_temp_playlist(self):
        """
        Creates a temp playlist (named "temp") in the user library.
        If temp already exists, delete all tracks
        """

        playlist = self.search_playlist_in_current_user_library("temp")
        if playlist is None:
            user_id = self._sp.current_user()['id']
            self._sp.user_playlist_create(user_id, "temp")

        return self.search_playlist_in_current_user_library("temp")

    @staticmethod
    def _list_of_uris_helper(playlist, tracks: List[Track], spotify_method):
        """
        Helpers for functions that take in a list of Tracks
        """
        playlist_id = playlist['id']
        curr = 0
        offset = 100
        uris = [track.uri for track in tracks]

        while curr < len(tracks):
            spotify_method(playlist_id, uris[curr: curr + offset])
            curr += offset

    @staticmethod
    def to_album_release_date(release_date: str, release_date_precision: str):
        if release_date_precision is None or release_date is None:
            return None

        pad_date = {
            'day': lambda date: date,
            'month': lambda date: f'{date}-01',
            'year': lambda date: f'{date}-01-01'
        }
        return datetime.datetime.strptime(
            pad_date[release_date_precision](release_date),
            '%Y-%m-%d'
        )

    @staticmethod
    def to_track(sp_result):
        sp_result = sp_result['track']
        artist = sp_result['artists'][0]['name']
        uri = sp_result['uri']
        album_release_date = SpotipyUtils.to_album_release_date(
            release_date=sp_result['album']['release_date'],
            release_date_precision=sp_result['album']['release_date_precision']
        )

        return Track(
            album_release_date=album_release_date,
            artist=artist,
            uri=uri,
            name=sp_result['name']
        )
