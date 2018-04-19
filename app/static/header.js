var state = 'unknown';
var volume_state = 100;
var playButton, content, socket;

function refreshPlayerStatus(data){
    state = data['state'];
    volume_state = parseInt(data['volume']);
    content = state === 'play' ? '<i class="fas fa-pause">' : '<i class="fas fa-play">';
    playButton.html(content);
    playButton.removeClass('disabled');
}

function refreshSongInformation(data){
    $('#title').text(data['title']);
    $('#artist').text(data['artist']);
    $('#album').text(data['album']);
    $('#track').text(data['track']);
    const length = makeLengthReadable(data['time']);
    $('#length').text(length);
}

function switchPlayButton() {
    content = state === 'play' ? '<i class="fas fa-pause">' : '<i class="fas fa-play">';
    playButton.html(content);
}

function play() {
    if (state !== 'unknown') {
        const cmd = state === 'play' ? 'pause' : 'play';
        $.get('/control/'+cmd);
        state = cmd;
        switchPlayButton();
    }
}

function setVolume(vol_value) {
    $.get('/volume', {'value': vol_value});
}

function seek(seek_value){
    $.get('/seek', {'value': seek_value});
}

function connectSocket(){
    socket = io.connect('//'+document.domain + ':' + location.port);
    socket.on('connect', function() {
        socket.on('set status', function(data){
            refreshPlayerStatus(data);
        });
        socket.on('current', function(data){
            refreshSongInformation(data)
        });
    });
}

$(document).ready(function(){
    playButton = $("#playback-btn");
    playButton.click(function() {
        play();
    });

    $('#fast-backward-btn').click(function() {
        $.get('/control/next');
    });

    $('#fast-forward-btn').click(function() {
        $.get('/control/previous');
    });

    connectSocket();
});