import datetime


class Track:
    def __init__(
            self,
            album_release_date: datetime,
            artist: str,
            uri: str,
            name: str
    ):
        self.album_release_date = album_release_date
        self.artist = artist
        self.uri = uri
        self.name = name

    def __repr__(self):
        return f'<Song ' \
               f'name:{self.name} ' \
               f'artists:{self.artist} ' \
               f'album_release_date:{self.album_release_date} '\
               f'uri:{self.uri} '
