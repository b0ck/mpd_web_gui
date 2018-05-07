import atexit
import time

from threading import Lock
from flask import Flask, render_template, request, jsonify
from mpd_helper import parse_albums_from_mpd, parse_songs_from_mpd
from flask_socketio import SocketIO
from config import Config

from api import MpdApi

app = Flask(__name__)
app.config['SECRET_KEY'] = ''
socketio = SocketIO(app)
api = MpdApi(host=Config.MPD_CLIENT_HOST, port=Config.MPD_CLIENT_PORT, use_unicode=Config.MPD_CLIENT_USE_UNICODE)
thread = None
thread_lock = Lock()
command_dict = {
    'pause': 'pause',
    'play': 'play',
    'stop': 'stop',
    'next': 'next_song',
    'previous': 'previous_song',
    'seek': 'seek',
    'volume': 'set_volume',
    'play_song': 'play_song',
    'play_pos': 'play',
    'add_song': 'add_song_to_current_playlist',
    'delete_song': 'delete_song_from_current_playlist'
}

last_song = None
last_status = None
last_play_list = None


@app.route("/")
def player():
    artists = api.get_artists()

    return render_template('player.html', artists=artists)


@app.route("/albums")
def albums():
    mpd_albums = api.get_albums(request.args.get('artist'))
    albums = parse_albums_from_mpd(mpd_albums)

    return jsonify(albums)


@app.route("/songs")
def songs():
    mpd_songs = api.get_songs(
        request.args.get('artist'),
        request.args.get('album'),
    )
    songs = parse_songs_from_mpd(mpd_songs)

    return jsonify(songs)


###################
# SOCKET COMMANDS #
###################
@socketio.on('command')
def handle_command(data):
    if isinstance(data, dict):
        if 'cmd' in data.keys():
            if data['cmd'] in command_dict.keys():
                method = getattr(api, command_dict.get(data['cmd']))
                if 'data' in data.keys():
                    method(**data['data'])
                else:
                    method()


@socketio.on('reload')
def handle_reload():
    socketio.emit('set player status', data=last_status, json=True)
    socketio.emit('set song info', data=last_song, json=True)
    socketio.emit('set current play list', data=last_play_list, json=True)


@socketio.on('connect')
def handle_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=start_sender)


def start_sender():
    global last_song
    global last_status
    global last_play_list
    global api
    current_song = None
    current_status = None
    current_play_list = None

    while True:
        try:
            current_status = api.get_status()
            if last_status != current_status:
                socketio.emit('set player status', data=current_status, json=True)
                last_status = current_status

            current_song = api.get_current_song()
            if last_song != current_song:
                socketio.emit('set song info', data=current_song, json=True)
                last_song = current_song

            current_play_list = parse_songs_from_mpd(api.get_current_list())
            if last_play_list != current_play_list:
                socketio.emit('set current play list', data=current_play_list, json=True)
                last_play_list = current_play_list
            time.sleep(1)

        except Exception as ex:
            print(ex)
            pass


def start_server():
    socketio.run(app, host=Config.SERVER_HOST, port=Config.SERVER_PORT, debug=Config.SERVER_DEBUG_MODE)

api._start_mpd()
start_server()
atexit.register(api.cleanup)
