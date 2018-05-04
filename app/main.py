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
    'previous': 'previous_song'
}


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


@app.route("/play")
def play():
    api.play_song(request.args.get('file'))

    return jsonify(api.get_current_song())


@app.route("/volume")
def volume():
    value = request.args.get('value')
    api.set_volume(value=value)

    return "Command executed!"


@app.route("/seek")
def seek():
    value = request.args.get('value')
    api.seek(value=value)

    return "Command executed!"


@app.route("/control/<cmd>")
def control(cmd):
    if cmd in command_dict.keys():
        method = getattr(api, command_dict.get(cmd))
        method()

    return "Command executed!"


@app.route("/current")
def current():
    return jsonify(api.get_current_song())


###################
# SOCKET COMMANDS #
###################
@socketio.on('connect')
def handle_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=start_sender)
    return ''


def start_sender():
    while True:
        try:
            socketio.emit('set status', data=api.get_status(), json=True)
            socketio.emit('current', data=api.get_current_song(), json=True)
            time.sleep(1)
        except Exception as ex:
            print(ex)
            pass


def start_server():
    socketio.run(app, host=Config.SERVER_HOST, port=Config.SERVER_PORT, debug=Config.SERVER_DEBUG_MODE)


start_server()
atexit.register(api.cleanup)
