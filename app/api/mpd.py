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
        self._exit_mpd()

    def connect(self):
        try:
            self.client.connect(self.host, self.port)

        except ConnectionRefusedError:
            self._start_mpd()
            self.client.connect(self.host, self.port)
            pass

        except ConnectionError:
            pass

    def stop(self):
        self.connect()
        self.client.stop()
        self.client.disconnect()

    def pause(self):
        self.connect()
        self.client.pause()
        self.client.disconnect()

    def play(self):
        self.connect()
        self.client.play()
        self.client.disconnect()

    def play_song(self, song):
        self.connect()
        self.client.clear()
        self.client.add(song)
        self.client.play()
        self.client.disconnect()

    def add_to_playlist(song):
        pass

    def get_random_song(self):
        pass

    def get_playlist(self):
        pass

    def get_artists(self):
        self.connect()
        artists = self.client.list('artist')
        self.client.disconnect()
        return artists

    def get_albums(self, artist):
        self.connect()
        songs = self.client.find('albumartist', artist)
        self.client.disconnect()
        return songs

    def get_songs(self, artist, album):
        self.connect()
        songs = self.client.find('albumartist', artist, 'album', album)
        self.client.disconnect()
        return songs

    def get_titles(self):
        pass

    def get_status(self):
        self.connect()
        status = self.client.status()
        self.client.disconnect()
        return status

    def get_current_song(self):
        self.connect()
        song = self.client.currentsong()
        self.client.disconnect()
        return song
