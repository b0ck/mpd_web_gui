"""
Tool for converting the mpd song info json in
formats with which we can better work in our gui.
"""


class Album:
    def __init__(self):
        self.year = 0
        self.title = ''
        self.length = 0


class Song:
    def __init__(self):
        self.track = 0
        self.title = ''
        self.length = 0
        self.file = ''


def get_or_append_album(albums, album):
    """ returns the album from the list if we already
     know it or adds it """
    for a in albums:
        if a.title == album.title and a.year == album.year:
            return a

    albums.append(album)
    return album


def parse_albums_from_mpd(data):
    albums = []
    albums_json = []

    for song_data in data:
        album = Album()
        album.year = song_data['date']
        album.title = song_data['album']
        album = get_or_append_album(albums, album)
        album.length += float(song_data['duration'])

    for album in albums:
        album.length = int(album.length)
        albums_json.append(album.__dict__)

    return albums_json


def parse_songs_from_mpd(data):
    songs_json = []
    for song_data in data:
        song = Song()
        song.track = song_data['track']
        song.title = song_data['title']
        song.length = song_data['time']
        song.file = song_data['file']
        songs_json.append(song.__dict__)

    return songs_json
