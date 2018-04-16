import sys
from flask import Flask, render_template, request, jsonify
from api import mpd_api
from mpd_helper import parse_albums_from_mpd, parse_songs_from_mpd

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/player")
def player():
    artists = mpd_api.get_artists()
    return render_template('player.html', artists=artists)


@app.route("/albums")
def albums():
    mpd_albums = mpd_api.get_albums(request.args.get('artist'))
    albums = parse_albums_from_mpd(mpd_albums)
    return jsonify(albums)


@app.route("/songs")
def songs():
    mpd_songs = mpd_api.get_songs(
        request.args.get('artist'),
        request.args.get('album'),
    )
    songs = parse_songs_from_mpd(mpd_songs)
    return jsonify(songs)


@app.route("/play")
def play():
    mpd_api.play_song(request.args.get('file'))
    return "Song should now be playing!"


@app.route("/control")
def control():
    cmd = request.args.get('cmd')
    if cmd == 'pause':
        mpd_api.pause()
    elif cmd == 'stop':
        mpd_api.stop()
    elif cmd == 'play':
        mpd_api.play()
    return "Command executed!"


@app.route("/current")
def current():
    return jsonify(mpd_api.get_current_song())


# TODO: merge with current so we only need one request
@app.route("/status")
def status():
    return jsonify(mpd_api.get_status())


if __name__ == "__main__":
    app.run(host= '0.0.0.0')
