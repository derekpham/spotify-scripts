from sqlitedict import SqliteDict

from spotify_scripts.property_constants import *
from core.spotipy_utils import SpotipyUtils


def __main__():
    properties = SqliteDict(PROPERTY_FILE)
    sp_utils = SpotipyUtils(client_id=properties[CLIENT_ID],
                            client_secret=properties[CLIENT_SECRET],
                            redirect_uri='https://localhost:8000',
                            scope='playlist-modify-public, playlist-modify-private')

    playlist_name = input('Enter the name of the playlist you want to sort: ')
    playlist = sp_utils.search_playlist_in_current_user_library(playlist_name)
    print(playlist)
    if playlist is None:
        print(f"Playlist {playlist_name} doesn't exist within this user's library")
        return

    tracks = sp_utils.retrieve_all_tracks_for_playlist(playlist)
    tracks.sort(key=lambda x: (x.album_release_date, x.artist))

    print('Sorting your playlist ...')
    print(f'Playlist ~{playlist_name}~ length: {len(tracks)}')
    print(f'Sorting your playlist ...')
    sp_utils.delete_all_tracks(playlist)
    sp_utils.add_all_tracks(playlist, tracks)
    print(f'Done!')
    print(f'Playlist ~{playlist_name}~ length: {sp_utils.num_tracks_in_playlist(playlist)}')


if __name__ == '__main__':
    __main__()
