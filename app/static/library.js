function updateSelection(item, list) {
    $(list).children().removeClass('active');
    $(item).addClass('active');
}

function appendAlbum(album) {
    return '' +
        '<a href="#" class="list-group-item list-group-item-action justify-content-between align-items-center d-flex">' +
            '<span>' +
                '<span class="badge badge-secondary prefix">' + album.year + '</span>' +
                '<span class="title">' + album.title + '</span>'+
            '</span>' +
            '<span class="badge badge-primary badge-pill">' + makeLengthReadable(album.length) + '</span>' +
        '</a>'
}

function appendSong(song) {
    return '' +
        '<li class="list-group-item list-group-item-action justify-content-between align-items-center d-flex">' +
            '<span>' +
                '<button type="button" class="btn btn-primary btn-sm play" file="' + song.file+ '"><i class="fas fa-play"></i></button>' +
                '<span class="badge badge-secondary prefix">#' + song.track + '</span>' +
                '<span class="title">' + song.title + '</span>'+
            '</span>' +
            '<span class="badge badge-primary badge-pill">' + makeLengthReadable(song.length) + '</span>' +
        '</li>'
}

function updateList(url, param, list, appendFnct, finishFnct) {
    $.getJSON(url, param, function(data) {
        list.empty();
        $.each(data, function(key, val) {
            list.append(appendFnct(val));
        });
        finishFnct();
    });
}

function playSong(file) {
    $.get('/play', {'file': file});
}

function initPlayButtonClickListener() {
    $('.btn.play').click(function() {
        var item = $(this).parent().parent();
        updateSelection(item, '#songs');
        playSong($(this).attr('file'));
    })
}

function initAlbumClickListener() {
    $('#albums').children().click(function() {
        updateSelection(this, '#albums');

        const param = {
            'artist': $('#artists .active').text(),
            'album': $(this).find('.title').text()
        };

        updateList(
            '/songs',
            param, $('#songs'),
            appendSong,
            initPlayButtonClickListener);
    });
}

function initArtistClickListener() {
    $('#artists').children().click(function() {
        updateSelection(this, '#artists');

        const param = {
            'artist': $(this).text()
        };

        $('#songs').empty();

        updateList(
            '/albums',
            param, $('#albums'),
            appendAlbum,
            initAlbumClickListener);
    });
}

$(document).ready(function(){
    initArtistClickListener();
});