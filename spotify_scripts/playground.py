from sqlitedict import SqliteDict
from pprint import pprint

from spotify_scripts.property_constants import *
from core.spotipy_utils import SpotipyUtils


def __main__():
    properties = SqliteDict(PROPERTY_FILE)
    sp_utils = SpotipyUtils(client_id=properties[CLIENT_ID],
                            client_secret=properties[CLIENT_SECRET],
                            redirect_uri='https://localhost:8000',
                            scope='playlist-modify-public,playlist-modify-private')

    mad_men_playlist = sp_utils.search_playlist_in_current_user_library("mad men")
    assert mad_men_playlist is not None

    print(sp_utils.num_tracks_in_playlist(mad_men_playlist))
    all_tracks = sp_utils.retrieve_all_tracks_for_playlist(mad_men_playlist)
    print(len(all_tracks))
    pprint(sp_utils.retrieve_all_tracks_for_playlist(mad_men_playlist))

    assert sp_utils.num_tracks_in_playlist(mad_men_playlist) == 19

    temp_playlist = sp_utils.create_temp_playlist()
    sp_utils.delete_all_tracks(temp_playlist)
    sp_utils.add_all_tracks(
        temp_playlist,
        sp_utils.retrieve_all_tracks_for_playlist(mad_men_playlist)
    )
    assert len(sp_utils.retrieve_all_tracks_for_playlist(temp_playlist)) == 19

    sp_utils.delete_all_tracks(temp_playlist)
    pop_playlist = sp_utils.search_playlist_in_current_user_library('mad men')
    sp_utils.add_all_tracks(temp_playlist, sp_utils.retrieve_all_tracks_for_playlist(pop_playlist))


if __name__ == '__main__':
    __main__()
