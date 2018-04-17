var state = 'unknown';
var mute_state = false;
var volume_state = 100;
var playButton, muteButton, content, volume_value;

function updateStatus() {
    $.getJSON('/current', function(data) {
        $('#title').text(data['title']);
        $('#artist').text(data['artist']);
        $('#album').text(data['album']);
        $('#track').text(data['track']);
        const length = makeLengthReadable(data['time']);
        $('#length').text(length);
    });

    $.getJSON('/status', function(data) {
        state = data['state'];
        volume_state = parseInt(data['volume']);
        content = state === 'play' ? '<i class="fas fa-pause">' : '<i class="fas fa-play">';
        playButton.html(content);
        playButton.removeClass('disabled');
    });
}
function play() {
    if (state !== 'unknown') {
        const cmd = state === 'play' ? 'pause' : 'play';
        $.get('/control', {'cmd': cmd});
        updateStatus();
    }
}

function fastForward() {
    if (state !== 'unknown') {
        $.get('/control', {'cmd': 'next'});
        updateStatus();
    }
}

function fastBackward() {
    if (state !== 'unknown') {
        $.get('/control', {'cmd': 'previous'});
        updateStatus();
    }
}

function setVolume(vol_value) {
    $.get('/volume', {'value': vol_value});
    updateStatus();
}

function seek(seek_value){
    $.get('/seek', {'value': seek_value});
    updateStatus();
}

$(document).ready(function(){
    playButton = $("#playback-btn");
    playButton.click(function() {
        play();
    });
    $('#fast-forward-btn').click(function() {
        fastForward();
    });
    $('#fast-backward-btn').click(function() {
        fastBackward();
    });
    updateStatus();
    // setInterval(updateStatus, 1000);
});