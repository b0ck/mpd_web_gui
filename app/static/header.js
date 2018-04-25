var state = 'unknown';
var volume_state = 100;
var slider_lock = false;
var slider_value = 0;
var duration = 0;
var playButton, content, socket, cur_length, length, slider;

function refreshPlayerStatus(data){
    cur_length = makeLengthReadable(data['elapsed']);
    state = data['state'];
    volume_state = parseInt(data['volume']);

    switchPlayButton();
    playButton.removeClass('disabled');

    if(!slider_lock){
        duration = data['duration'];
        $('#title_cur_length').text(cur_length);
        slider_value = (data['elapsed'] / duration) * 100;
        $('#durationSlider').val(slider_value);
        $('#title_length').text(makeLengthReadable(duration));
    }
}

function refreshSongInformation(data){
    $('#title').text(data['title']);
    $('#artist').text(data['artist']);
    $('#album').text(data['album']);
    $('#track').text(data['track']);
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

    $('#durationSlider').mousedown(function () {
        slider_lock = true;
    });

    $('#durationSlider').mouseup(function () {
        slider_value = $('#durationSlider').val();
        seek((duration / 100) * slider_value);
        slider_lock = false;
    });

    slider = document.getElementById('durationSlider');
    slider.oninput = function() {
        $('#title_cur_length').text(
            makeLengthReadable((duration / 100 )*this.value)
        );
    };

    connectSocket();
});