import atexit

from flask import Flask, render_template, request, jsonify
from mpd_helper import parse_albums_from_mpd, parse_songs_from_mpd

from api import MpdApi

DEBUG_MODE = True
app = Flask(__name__)
api = MpdApi()


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
    return "Song should now be playing!"


@app.route("/control")
def control():
    cmd = request.args.get('cmd')
    if cmd == 'pause':
        api.pause()
    elif cmd == 'stop':
        api.stop()
    elif cmd == 'play':
        api.play()
    return "Command executed!"


@app.route("/current")
def current():
    return jsonify(api.get_current_song())


# TODO: merge with current so we only need one request
@app.route("/status")
def status():
    return jsonify(api.get_status())


app.run(host='0.0.0.0', debug=DEBUG_MODE)

atexit.register(api.cleanup)
