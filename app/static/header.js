var state = 'unknown';

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
        const content = state === 'play' ? '<i class="fas fa-pause">' : '<i class="fas fa-play">';
        const playBtn = $("#playback-btn");
        playBtn.html(content);
        playBtn.removeClass('disabled')
    });
}

$(document).ready(function(){
    $('#playback-btn').click(function() {
        if (state !== 'unknown') {
            const cmd = state === 'play' ? 'pause' : 'play';
            $.get('/control', {'cmd': cmd});
            updateStatus();
        }
    });

    updateStatus();
    // setInterval(updateStatus, 1000);
});