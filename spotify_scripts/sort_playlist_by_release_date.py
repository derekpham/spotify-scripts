from sqlitedict import SqliteDict
from spotify_scripts.property_constants import *
from spotipy import SpotifyOAuth, Spotify
from core import spotipy_utils
import datetime


class Song:
    def __init__(self, album_release_date: datetime, artist: str, uri: str):
        self.album_release_date = album_release_date
        self.artist = artist
        self.uri = uri

    def __repr__(self):
        return f'<Song ' \
               f'album_release_date:{self.album_release_date} ' \
               f'artists:{self.artist} ' \
               f'uri:{self.uri}'

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
    def to_song(sp_result):
        sp_result = sp_result['track']
        artist = sp_result['artists'][0]['name']
        uri = sp_result['uri']
        album_release_date = Song.to_album_release_date(
            release_date=sp_result['album']['release_date'],
            release_date_precision=sp_result['album']['release_date_precision']
        )
        return Song(album_release_date=album_release_date, artist=artist, uri=uri)


def __main__():
    properties = SqliteDict(PROPERTY_FILE)
    sp = Spotify(auth_manager=SpotifyOAuth(client_id=properties[CLIENT_ID],
                                           client_secret=properties[CLIENT_SECRET],
                                           redirect_uri='https://localhost:8000',
                                           scope='playlist-modify-public,playlist-modify-private'))
    playlist_name = input('Enter the name of the playlist you want to sort: ')
    playlist = spotipy_utils.search_playlist_in_current_user_library(sp, playlist_name)
    if playlist is None:
        print(f"Playlist {playlist_name} doesn't exist within this user's library")

    songs = [Song.to_song(sp_song) for sp_song in spotipy_utils.retrieve_all_tracks_for_playlist(
        sp,
        playlist,
        fields='items(track(album(release_date,release_date_precision),artists(name),uri))'
    )]
    songs.sort(key=lambda x: (x.album_release_date, x.artist))

    print('Sorting your playlist ...')
    print(f'Playlist ~{playlist_name}~ length: {len(songs)}')
    print(f'Sorting your playlist ...')
    spotipy_utils.delete_all_tracks(sp, playlist, [song.uri for song in songs])
    spotipy_utils.add_all_tracks(sp, playlist, [song.uri for song in songs])
    print(f'Done!')
    print(f'Playlist ~{playlist_name}~ length: {spotipy_utils.playlist_size(sp, playlist_name)}')


if __name__ == '__main__':
    __main__()
