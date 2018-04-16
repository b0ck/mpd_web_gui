import mpd

client = mpd.MPDClient(use_unicode=True)


def connect():
    client.connect("localhost", 6600)


def stop():
    connect()
    client.stop()
    client.disconnect()


def pause():
    connect()
    client.pause()
    client.disconnect()


def play():
    connect()
    client.play()
    client.disconnect()


def play_song(song):
    connect()
    client.clear()
    client.add(song)
    client.play()
    client.disconnect()


def add_to_playlist(song):
    pass


def get_random_song():
    pass


def get_playlist():
    pass


def get_artists():
    connect()
    artists = client.list('artist')
    client.disconnect()
    return artists


# def get_albums(artist):
#     connect()
#     albums = client.list('album', 'artist', artist) if artist else client.list('album')
#     client.disconnect()
#     return albums


def get_albums(artist):
    connect()
    songs = client.find('albumartist', artist)
    client.disconnect()
    return songs


def get_songs(artist, album):
    connect()
    songs = client.find('albumartist', artist, 'album', album)
    client.disconnect()
    return songs


def get_titles():
    pass


def get_status():
    connect()
    status = client.status()
    client.disconnect()
    return status


def get_current_song():
    connect()
    song = client.currentsong()
    client.disconnect()
    return song
