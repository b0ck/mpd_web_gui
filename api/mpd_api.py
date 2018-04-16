import mpd
import logging
import subprocess


class MPDAPI(object):

    client = mpd.MPDClient(use_unicode=True)
    host = "localhost"
    port = 6600
    logger = logging.getLogger('player')

    def _execute(self, cmd):
        """

        :param cmd:
        :return:
        """

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
        """

        :return:
        """

        self._execute(['mpd'])

    def _exit_mpd(self):
        """

        :return:
        """

        self._execute(['mpd', '--kill'])

    def connect(self, host="localhost", port=6600):
        """

        :param host:
        :param port:
        :return:
        """

        try:
            self.client.connect(host, port)

        except ConnectionRefusedError:
            self._start_mpd()
            self.client.connect(host, port)
            pass

        except ConnectionError:
            pass

    def stop(self):
        """

        :return:
        """

        self.connect(host=self.host, port=self.port)
        self.client.stop()
        self.client.disconnect()

    def pause(self):
        self.connect(host=self.host, port=self.port)
        self.client.pause()
        self.client.disconnect()

    def play(self):
        """

        :return:
        """

        self.connect(host=self.host, port=self.port)
        self.client.play()
        self.client.disconnect()

    def play_song(self, song):
        """

        :param song:
        :return:
        """

        self.connect(host=self.host, port=self.port)
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
        """

        :return:
        """

        self.connect(host=self.host, port=self.port)
        artists = self.client.list('artist')
        self.client.disconnect()
        return artists

    # def get_albums(artist):
    #     connect()
    #     albums = client.list('album', 'artist', artist) if artist else client.list('album')
    #     client.disconnect()
    #     return albums

    def get_albums(self, artist):
        """

        :param artist:
        :return:
        """

        self.connect(host=self.host, port=self.port)
        songs = self.client.find('albumartist', artist)
        self.client.disconnect()
        return songs

    def get_songs(self, artist, album):
        """

        :param artist:
        :param album:
        :return:
        """

        self.connect(host=self.host, port=self.port)
        songs = self.client.find('albumartist', artist, 'album', album)
        self.client.disconnect()
        return songs

    def get_titles(self):
        pass

    def get_status(self):
        """

        :return:
        """

        self.connect(host=self.host, port=self.port)
        status = self.client.status()
        self.client.disconnect()
        return status

    def get_current_song(self):
        """

        :return:
        """

        self.connect(host=self.host, port=self.port)
        song = self.client.currentsong()
        self.client.disconnect()
        return song
