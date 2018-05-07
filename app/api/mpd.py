import mpd
import logging
import subprocess


class MpdApi(object):

    def __init__(self, host='localhost', port=6600, use_unicode=True):
        self.client = mpd.MPDClient(use_unicode=use_unicode)
        self.host = host
        self.port = port
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

    def _send_command(self, name, data=None, *args):
        if not self.client._sock:
            self.client.connect(self.host, self.port)
        method = getattr(self.client, name)
        if data:
            result = method(data)
        elif args:
            result = method(*args)
        else:
            result = method()
        self.client.disconnect()
        return result

    def cleanup(self):
        self._exit_mpd()

    def stop(self):
        self._send_command(name='stop')

    def pause(self):
        self._send_command(name='pause')

    def play(self, pos=None):
        self._send_command(name='play', data=pos)

    def add_song_to_current_playlist(self, song):
        self._send_command(name='add', data=song)

    def delete_song_from_current_playlist(self, pos):
        self._send_command(name='delete', data=pos)

    def play_song(self, song):
        self._send_command(name='clear')
        self.add_song_to_current_playlist(song=song)
        self.play()

    def get_current_list(self):
        return self._send_command(name='playlistinfo')

    def add_to_playlist(self, name, song):
        self._send_command('playlistadd', None, name, song)

    def get_random_song(self):
        pass

    def get_artists(self):
        return self._send_command(name='list', data='artist')

    def get_albums(self, artist):
        return self._send_command('find', None, 'albumartist', artist)

    def get_songs(self, artist, album):
        return self._send_command('find', None, 'albumartist', artist, 'album', album)

    def get_titles(self):
        pass

    def set_volume(self, value):
        self._send_command(name='setvol', data=value)

    def seek(self, value):
        self._send_command(name='seekcur', data=value)

    def next_song(self):
        self._send_command(name='next')

    def previous_song(self):
        self._send_command(name='previous')

    def get_status(self):
        return self._send_command(name='status')

    def get_current_song(self):
        return self._send_command(name='currentsong')
