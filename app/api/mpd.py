import mpd
import logging
import subprocess


class MpdApi(object):

    def __init__(self):
        self.client = mpd.MPDClient(use_unicode=True)
        self.host = "localhost"
        self.port = 6600
        self.logger = logging.getLogger('player')

    def _execute(self, cmd):
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        out, err = p.communicate()
        out = out.decode('utf-8') if out else ''
        if err:
            if out:
                out += '\n'
            out += 'Stderr: ' + err.decode('utf-8')
        self.logger.debug('>>> %s', cmd)
        self.logger.debug('code: %s | %s', p.returncode, out)
        return p.returncode == 0, out

    def _start_mpd(self):
        self._execute(['mpd'])

    def _exit_mpd(self):
        self._execute(['mpd', '--kill'])

    def cleanup(self):
        if self.client._sock:
            self.client.disconnect()
        self._exit_mpd()

    def connect(self):
        try:
            self.client.connect(self.host, self.port)

        except ConnectionRefusedError:
            self._start_mpd()
            self.client.connect(self.host, self.port)
            pass

        except ConnectionError as ex:
            print(ex)
            pass
        
    def check_and_connect(self):
        if not self.client._sock:
            self.connect()

    def stop(self):
        self.check_and_connect()
        self.client.stop()

    def pause(self):
        self.check_and_connect()
        self.client.pause()

    def play(self):
        self.check_and_connect()
        self.client.play()

    def play_song(self, song):
        self.check_and_connect()
        self.client.clear()
        self.client.add(song)
        self.client.play()

    def add_to_playlist(song):
        pass

    def get_random_song(self):
        pass

    def get_playlist(self):
        pass

    def get_artists(self):
        self.check_and_connect()
        artists = self.client.list('artist')
        return artists

    def get_albums(self, artist):
        self.check_and_connect()
        songs = self.client.find('albumartist', artist)
        return songs

    def get_songs(self, artist, album):
        self.check_and_connect()
        songs = self.client.find('albumartist', artist, 'album', album)
        return songs

    def get_titles(self):
        pass

    def set_volume(self, value):
        self.check_and_connect()
        self.client.set_vol(value)

    def seek(self, value):
        self.check_and_connect()
        self.client.seek(value)

    def next_song(self):
        self.check_and_connect()
        self.client.next()

    def previous_song(self):
        self.check_and_connect()
        self.client.previous()

    def get_status(self):
        self.check_and_connect()
        status = self.client.status()
        return status

    def get_current_song(self):
        self.check_and_connect()
        song = self.client.currentsong()
        return song
