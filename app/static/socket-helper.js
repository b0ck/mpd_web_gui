var state = 'unknown';
var socket = io.connect('//'+document.domain + ':' + location.port);

function playPos(pos) {
    socket.emit('command', {'cmd':'play_pos', 'data':{'pos':pos}});
}

function playSong(file) {
    socket.emit('command', {'cmd':'play_song', 'data':{'song':file}});
}

function addSong(file) {
    socket.emit('command', {'cmd':'add_song', 'data':{'song':file}});
}

function deleteSong(pos) {
    socket.emit('command', {'cmd':'delete_song', 'data':{'pos':pos}});
}

function play() {
    if (state !== 'unknown') {
        const cmd = state === 'play' ? 'pause' : 'play';
        socket.emit('command', {'cmd':cmd});
    }
}

function setVolume(vol_value) {
    socket.emit('command', {'cmd':'volume', 'data':{'value':vol_value}});
}

function seek(seek_value){
    socket.emit('command', {'cmd':'seek', 'data':{'value':seek_value}});
}

function playNext() {
    socket.emit('command', {'cmd':'next'});
}

function playPrevious() {
    socket.emit('command', {'cmd':'previous'});
}