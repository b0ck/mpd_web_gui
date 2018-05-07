var state = 'unknown';
var volume_state = 0;
var slider_lock = false;
var slider_value = 0;
var duration = 0;
var socket = io.connect('//'+document.domain + ':' + location.port);
var playButton, current_list, content, cur_length, length, slider;

function refreshPlaylist(data) {
    current_list.empty();
    $.each(data, function() {
        current_list.append(buildSongCurrent(this));
    });
}

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
    }
}

function refreshSongInformation(data){
    $('#title').text(data['title']);
    $('#artist').text(data['artist']);
    $('#album').text(data['album']);
    $('#track').text(data['track']);
    $('#title_length').text(makeLengthReadable(data['duration']));
}

function switchPlayButton() {
    content = state === 'play' ? '<i class="fas fa-pause">' : '<i class="fas fa-play">';
    playButton.html(content);
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

function prepareSocket(){
    socket.on('set player status', function(data){
        refreshPlayerStatus(data);
    });
    socket.on('set song info', function(data){
        refreshSongInformation(data)
    });
    socket.on('set current play list', function(data){
        refreshPlaylist(data)
    });
    socket.emit('reload');
}

function initDurationSlider(){
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
}

$(function(){
    playButton = $("#playback-btn");
    playButton.click(function() {
        play();
    });
    current_list = $('#current-songs');

    $('#fast-backward-btn').click(function() {
        socket.emit('command', {'cmd':'next'});
    });

    $('#fast-forward-btn').click(function() {
        socket.emit('command', {'cmd':'previous'});
    });
    initDurationSlider();
    prepareSocket();
});